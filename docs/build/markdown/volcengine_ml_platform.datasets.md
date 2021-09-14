# volcengine_ml_platform.datasets package

## Submodules

## volcengine_ml_platform.datasets.dataset module

提供数据集下载，分裂操作


### volcengine_ml_platform.datasets.dataset.dataset_copy_file(metadata, source_dir, destination_dir)
复制文件夹


* **Parameters**

    
    * **metadata** (*dict*) – 一个 manifest 文件读取的 dict


    * **source_dir** (*str*) – 源文件夹


    * **destination_dir** (*str*) – 目标文件夹


## volcengine_ml_platform.datasets.image_dataset module

## volcengine_ml_platform.datasets.tabular_dataset module


### class volcengine_ml_platform.datasets.tabular_dataset.TabularDataset(dataset_id: str = '', annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`

TabularDataset创建函数同 `ImageDataset`


#### download(local_path: str = 'TabularDataset')
把数据集从 TOS 下载到本地


* **Parameters**

    **local_path** (*str*) – 设置下载目录



#### split(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
把数据集分割成两个数据集对象（测试集合训练集）


* **Parameters**

    
    * **training_dir** (*str*) – 训练集输出目录


    * **testing_dir** (*str*) – 测试集输出目录


    * **ratio** (*float**, **optional*) – 训练集数据所占比例，默认为 0.8


    * **random_state** (*int**, **optional*) – 随机数种子



* **Returns**

    返回两个数据集，第一个是训练集


## volcengine_ml_platform.datasets.text_dataset module


### class volcengine_ml_platform.datasets.text_dataset.TextDataset(dataset_id: str = '', annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`

TextDataset创建函数同 `ImageDataset`


#### download(local_path: str = 'TextDataset', limit=- 1)
把数据集从 TOS 下载到本地


* **Parameters**

    
    * **local_path** (*str*) – 设置下载目录


    * **limit** (*int**, **optional*) – 设置最大下载数据条目



#### split(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
把数据集分割成两个数据集对象（测试集合训练集）


* **Parameters**

    
    * **training_dir** (*str*) – 训练集输出目录


    * **testing_dir** (*str*) – 测试集输出目录


    * **ratio** (*float**, **optional*) – 训练集数据所占比例，默认为 0.8


    * **random_state** (*int**, **optional*) – 随机数种子



* **Returns**

    返回两个数据集，第一个是训练集


## volcengine_ml_platform.datasets.video_dataset module


### class volcengine_ml_platform.datasets.video_dataset.VideoDataset(dataset_id: str = '', annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`

VideoDataset创建函数同 `ImageDataset`


#### download(local_path: str = 'VideoDataset', limit=- 1)
把数据集从 TOS 下载到本地


* **Parameters**

    
    * **local_path** (*str*) – 设置下载目录


    * **limit** (*int**, **optional*) – 设置最大下载数据条目



#### split(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
把数据集分割成两个数据集对象（测试集合训练集）


* **Parameters**

    
    * **training_dir** (*str*) – 训练集输出目录


    * **testing_dir** (*str*) – 测试集输出目录


    * **ratio** (*float**, **optional*) – 训练集数据所占比例，默认为 0.8


    * **random_state** (*int**, **optional*) – 随机数种子



* **Returns**

    返回两个数据集，第一个是训练集


## Module contents

下载不同种类数据集，可进行 split 操作
