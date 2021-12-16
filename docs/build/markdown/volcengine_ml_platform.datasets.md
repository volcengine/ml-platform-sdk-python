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


## volcengine_ml_platform.datasets.dataset_util module

## volcengine_ml_platform.datasets.image_dataset module


### class volcengine_ml_platform.datasets.image_dataset.ImageDataset(dataset_id: str = '', annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None)
Bases: `volcengine_ml_platform.datasets.dataset._Dataset`

ImageDataset创建函数 `ImageDataset` ，需要提供于 ml_engine 交互的基本信息，方便传输下载内容


* **Parameters**

    
    * **dataset_id** (*str*) – ml_engine 创建时提供的 dataset_id


    * **annotation_id** (*str**, **None*) – ml_engine 创建时提供的 注释集 annotation_id


    * **local_path** (*str*) – 数据下载到本地的目录


    * **tos_source** (*str**, **None*) – 数据集的manifest文件的 tos url，一般可不设置



#### download(local_path: str = 'ImageDataset', limit=- 1)
把数据集从 TOS 下载到本地


* **Parameters**

    
    * **local_path** (*str*) – 设置下载目录


    * **limit** (*int**, **optional*) – 设置最大下载数据条目



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
## volcengine_ml_platform.datasets.inner_dataset module


### class volcengine_ml_platform.datasets.inner_dataset.InnerDataset(dataset_type, dataset_id: str = '', annotation_id: Optional[str] = None, local_path: str = '.', tos_source: Optional[str] = None, target_user_id=None, target_account_id=None)
Bases: `volcengine_ml_platform.datasets.tabular_dataset.TabularDataset`


#### download(local_path: str = 'InnerDataset', limit=- 1)
把数据集从 TOS 下载到本地


* **Parameters**

    **local_path** (*str*) – 设置下载目录



#### get_target_account_id()

#### get_target_user_id()

#### set_target_account_id(target_account_id)

#### set_target_user_id(target_user_id)

#### split(dataset_type, training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
把数据集分割成两个数据集对象（测试集合训练集）


* **Parameters**

    
    * **training_dir** (*str*) – 训练集输出目录


    * **testing_dir** (*str*) – 测试集输出目录


    * **ratio** (*float**, **optional*) – 训练集数据所占比例，默认为 0.8


    * **random_state** (*int**, **optional*) – 随机数种子



* **Returns**

    返回两个数据集，第一个是训练集


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



#### split_init(training_dir: str, testing_dir: str)

#### split_tabular(training_dir: str, testing_dir: str, ratio=0.8, random_state=0)
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
## Module contents

下载不同种类数据集，可进行 split 操作
