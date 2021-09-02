# volcengine_ml_platform.datasets package

## Submodules

## volcengine_ml_platform.datasets.dataset module

数据集抽象实现


### volcengine_ml_platform.datasets.dataset.dataset_copy_file(metadata, source_dir, destination_dir)
复制文件夹


* **Parameters**

    
    * **metadata** (*dict*) – 一个 manifest 文件读取的 dict


    * **source_dir** (*str*) – 源文件夹


    * **destination_dir** (*str*) – 目标文件夹


## volcengine_ml_platform.datasets.image_dataset module


### class volcengine_ml_platform.datasets.image_dataset.ImageDataset(dataset_id: Optional[str] = None, annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`


#### download(local_path: str = 'ImageDataset', limit=- 1)
download datasets from source


* **Parameters**

    **limit** (*int**, **optional*) – download size. Defaults to -1 (no limit).



#### init_torch_dataset(transform: Optional[collections.abc.Callable] = None, target_transform: Optional[collections.abc.Callable] = None)

#### load_as_np(offset=0, limit=- 1)
load images as numpy array


* **Parameters**

    
    * **offset** (*int**, **optional*) – num of images to skip. Defaults to 0.


    * **limit** (*int**, **optional*) – num of images to load. Defaults to -1.



* **Returns**

    np array of images
    list of annotations



#### parse_image_manifest(manifest_file_path)

#### split(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
split datasets and return two datasets objects


* **Parameters**

    
    * **training_dir** (*str*) – [output directory of training data]


    * **testing_dir** (*str*) – [output directory of testing data]


    * **ratio** (*float**, **optional*) – [training set split ratio].
    Defaults to 0.8.


    * **random_state** (*int**, **optional*) – [random seed]. Defaults to 0.



* **Returns**

    two datasets, first one is the training set


## volcengine_ml_platform.datasets.tabular_dataset module


### class volcengine_ml_platform.datasets.tabular_dataset.TabularDataset(dataset_id: Optional[str] = None, annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`


#### download(local_path: str = 'TabularDataset')

#### split(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
split dataset and return two dataset objects


* **Parameters**

    
    * **training_dir** (*str*) – output directory of training data


    * **testing_dir** (*str*) – output directory of testing data


    * **ratio** (*float**, **optional*) – training set split ratio.
    Defaults to 0.8.


    * **random_state** (*int**, **optional*) – random seed. Defaults to 0.



* **Returns**

    two datasets, first one is the training set


## volcengine_ml_platform.datasets.text_dataset module


### class volcengine_ml_platform.datasets.text_dataset.TextDataset(dataset_id: Optional[str] = None, annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`


#### download(local_path: str = 'TextDataset', limit=- 1)
download datasets from source


* **Parameters**

    **limit** (*int**, **optional*) – download size. Defaults to -1 (no limit).



#### split(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
split datasets and return two datasets objects


* **Parameters**

    
    * **training_dir** (*str*) – [output directory of training data]


    * **testing_dir** (*str*) – [output directory of testing data]


    * **ratio** (*float**, **optional*) – [training set split ratio].
    Defaults to 0.8.


    * **random_state** (*int**, **optional*) – [random seed]. Defaults to 0.



* **Returns**

    two datasets, first one is the training set


## volcengine_ml_platform.datasets.video_dataset module


### class volcengine_ml_platform.datasets.video_dataset.VideoDataset(dataset_id: Optional[str] = None, annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`


#### download(local_path: str = 'VideoDataset', limit=- 1)
download datasets from source


* **Parameters**

    **limit** (*int**, **optional*) – download size. Defaults to -1 (no limit).



#### split(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
split datasets and return two datasets objects


* **Parameters**

    
    * **training_dir** (*str*) – [output directory of training data]


    * **testing_dir** (*str*) – [output directory of testing data]


    * **ratio** (*float**, **optional*) – [training set split ratio].
    Defaults to 0.8.


    * **random_state** (*int**, **optional*) – [random seed]. Defaults to 0.



* **Returns**

    two datasets, first one is the training set


## Module contents

下载不同种类数据集，可进行 split 操作
