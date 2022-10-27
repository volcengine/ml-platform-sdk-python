# Volcano Engine ML Platform Tracking Python SDK

## import and initialize
``` python
from volcengine_ml_platform import tracking as tk
tk.init(experiment_name="test_exp", trial_name="test_trial", trial_description="blabla")
```

## set config and summary
``` python
tk.config.alpha = 1
tk.config.update({"update": True})

tk.summary.acc = 1
tk.summary.update({"loss": 0.1})
```

## log

``` python
# log scalar
for i in range(10):
    tk.log({"loss": random.random()}, step=i)

# log table
table = tk.Table(columns=['pic', 'score'], column_type={"pic": tk.Image})
for i in range(10):
    h = 10 + i * 10
    w = h
    arr = np.arange(h * w).reshape((h, w)) / (h * w)
    image = tk.Image(arr)
    t.add_row(image, random.random())

tk.log({"table_test": t}, commit=True)
```