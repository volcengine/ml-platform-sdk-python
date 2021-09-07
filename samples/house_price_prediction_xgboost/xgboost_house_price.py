import argparse
import warnings
from io import StringIO

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

import volcengine_ml_platform
from volcengine_ml_platform import constant
from volcengine_ml_platform.io import tos
from volcengine_ml_platform.util import cache_dir

warnings.filterwarnings(action="ignore", category=UserWarning)

volcengine_ml_platform.init()
client = tos.TOSClient()
BUCKET = constant.get_public_examples_readonly_bucket()
CACHE_DIR = cache_dir.create("price_prediction/xgboost")

zero_list = [
    "MasVnrArea",
    "GarageCars",
    "GarageArea",
    "BsmtHalfBath",
    "BsmtFullBath",
]
na_list = [
    "PoolQC",
    "MiscFeature",
    "Alley",
    "Fence",
    "GarageFinish",
    "GarageQual",
    "GarageCond",
    "GarageType",
    "BsmtQual",
    "BsmtCond",
    "BsmtExposure",
    "BsmtFinType1",
    "BsmtFinType2",
    "FireplaceQu",
]
na_values = [
    "Electrical",
    "Functional",
    "Utilities",
    "Exterior2nd",
    "Exterior1st",
    "KitchenQual",
    "SaleType",
    "MSZoning",
    "MasVnrType",
    "BsmtHalfBath",
    "BsmtFullBath",
    "TotalBsmtSF",
    "BsmtUnfSF",
    "BsmtFinSF2",
    "BsmtFinSF1",
]

csv_string_train = (
    client.get_object(bucket=BUCKET, key="house-price-prediction/dataset/train.csv")
    .read()
    .decode("utf-8")
)
train = pd.read_csv(StringIO(csv_string_train))

csv_string_test = (
    client.get_object(bucket=BUCKET, key="house-price-prediction/dataset/test.csv")
    .read()
    .decode("utf-8")
)
test = pd.read_csv(StringIO(csv_string_test))

test_ids = test.Id

train.drop(["Id"], axis=1, inplace=True)
train_tmp = train.drop(["SalePrice"], axis=1)
test = test.drop(["Id"], axis=1)

total = pd.concat([train_tmp, test]).reset_index(drop=True)


def fill_zero_values(zero_list):
    global train, test, test_ids, total
    for elem in zero_list:
        total[elem] = total[elem].fillna(0)
        train[elem] = train[elem].fillna(0)
        test[elem] = test[elem].fillna(0)


def fill_na_values(na_list):
    global train, test, test_ids, total
    for elem in na_list:
        total[elem] = total[elem].fillna("NA")
        train[elem] = train[elem].fillna("NA")
        test[elem] = test[elem].fillna("NA")


def replace_with_mode(na_values):
    global train, test, test_ids, total
    for elem in na_values:
        total[elem] = total[elem].fillna(total[elem].mode()[0])
        train[elem] = train[elem].fillna(train[elem].mode()[0])
        test[elem] = test[elem].fillna(test[elem].mode()[0])


def replace_with_linear_regression():
    # execute a linear regression to replace the null values
    global train, test, test_ids, total
    total_lot = total[
        (pd.notna(total.LotFrontage))
        & (total.LotFrontage < 200)
        & (total.LotArea < 100000)
    ][["LotFrontage", "LotArea", "BsmtHalfBath"]]
    regressor = LinearRegression()
    regressor.fit(total_lot.LotArea.to_frame(), total_lot.LotFrontage)

    lot_nan_total = total[pd.isnull(total.LotFrontage)].LotArea
    lot_nan_train = train[pd.isnull(train.LotFrontage)].LotArea
    lot_nan_test = test[pd.isnull(test.LotFrontage)].LotArea

    lot_pred_total = regressor.predict(lot_nan_total.to_frame())
    lot_pred_train = regressor.predict(lot_nan_train.to_frame())
    lot_pred_test = regressor.predict(lot_nan_test.to_frame())

    total.loc[total.LotFrontage.isnull(), "LotFrontage"] = lot_pred_total
    train.loc[train.LotFrontage.isnull(), "LotFrontage"] = lot_pred_train
    test.loc[test.LotFrontage.isnull(), "LotFrontage"] = lot_pred_test


def data_cleaning():
    global train, test, test_ids, total

    fill_zero_values(zero_list)
    fill_na_values(na_list)
    replace_with_mode(na_values)

    replace_with_linear_regression()

    total.GarageYrBlt = total.GarageYrBlt.fillna(total.YearBuilt)
    train.GarageYrBlt = train.GarageYrBlt.fillna(train.YearBuilt)
    test.GarageYrBlt = test.GarageYrBlt.fillna(test.YearBuilt)

    total.loc[total.GarageYrBlt > 2100, "GarageYrBlt"] = total.YearBuilt
    train.loc[train.GarageYrBlt > 2100, "GarageYrBlt"] = train.YearBuilt
    test.loc[test.GarageYrBlt > 2100, "GarageYrBlt"] = test.YearBuilt

    train.SalePrice = np.log(train.SalePrice)

    final_total = pd.get_dummies(total).reset_index(drop=True)

    y = train.SalePrice
    x_ = final_total.iloc[: len(y), :]
    test = final_total.iloc[len(y) :, :]

    return x_, y, test


if __name__ == "__main__":
    # args parser
    parser = argparse.ArgumentParser(description="XGBoost Training Example")
    parser.add_argument(
        "--learning_rate",
        type=float,
        nargs="+",
        default=[0.15, 0.2],
        help="input learning_rate for training",
    )
    parser.add_argument(
        "--colsample_bytree",
        type=float,
        nargs="+",
        default=[0.6],
        help="input colsample_bytree for training",
    )
    parser.add_argument(
        "--min_child_weight",
        type=float,
        nargs="+",
        default=[1.1, 1.3],
        help="number of min_child_weight to train",
    )
    parser.add_argument(
        "--max_depth",
        type=int,
        nargs="+",
        default=[3, 6],
        help="number of max_depth to train",
    )
    parser.add_argument(
        "--load_model",
        action="store_true",
        help="whether load model",
    )

    args = parser.parse_args()
    print("Begin to do data cleaning...")
    x_, y, test_ = data_cleaning()

    if args.load_model:
        LOADED_MODEL_PATH = CACHE_DIR.get_root_path() + "loaded_xgboost_model.pkl"
        client.download_file(
            file_path=LOADED_MODEL_PATH,
            bucket=BUCKET,
            key="house-price-prediction/models/xgboost_model.pkl",
        )
        model_xgb = joblib.load(LOADED_MODEL_PATH)
        print("model load successfully")
    else:
        model_xgb = XGBRegressor()
        parameters = {
            "colsample_bytree": args.colsample_bytree,
            "subsample": [0.9, 1],
            "gamma": [0.004],
            "min_child_weight": args.min_child_weight,
            "max_depth": args.max_depth,
            "learning_rate": args.learning_rate,
            "n_estimators": [1000],
            "reg_alpha": [0.75],
            "reg_lambda": [0.45],
            "seed": [42],
        }
        grid_search = GridSearchCV(
            estimator=model_xgb,
            param_grid=parameters,
            scoring="neg_mean_squared_error",
            cv=5,
            verbose=2,
        )

        print("Begin to fit...")
        model_xgb = grid_search.fit(x_, y)
        best_score = grid_search.best_score_
        best_parameters = grid_search.best_params_

        # save model
        MODEL_PATH = CACHE_DIR.get_root_path() + "xgboost_model.pkl"
        joblib.dump(model_xgb, MODEL_PATH)
        print("model has been uploaded successfully")
        print("best score:" + str(best_score))
        print("best parameters" + str(best_parameters))

    y_pred = model_xgb.predict(test_)
    y_pred = np.floor(np.expm1(y_pred))

    print("done!")
