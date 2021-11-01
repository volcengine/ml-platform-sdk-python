# volcengine_ml_platform.io package

## Submodules

## volcengine_ml_platform.io.tos module

提供对 TOS 储存的上传、下载、删除、查询功能


### class volcengine_ml_platform.io.tos.TOSClient()
Bases: `object`

自动配置环境变量中的用户信息，与TOS 进行交互


#### bucket_exists(bucket_name)
查询用户的 bucket 是否存在


* **Parameters**

    **bucket_name** (*str*) – 用户创建bucket 对应的桶名



* **Returns**

    返回一个 Bool 变量，代表桶是否存在



* **Raises**

    **ClientError** – 创建时发生错误



#### clear_bucket_objects(bucket)
删除桶的中所有内容


* **Parameters**

    **bucket** (*str*) – 创建时的桶名



#### create_bucket(bucket_name, region='')
创建一个 bucket


* **Parameters**

    
    * **bucket_name** (*str*) – 桶名


    * **region** (*str*) – 制定创建桶所在的地域



* **Returns**

    返回 bool，表示创建是否成功



* **Raises**

    **ClientError** – 创建时发生错误



#### delete_bucket(bucket)
删除桶


* **Parameters**

    **bucket** (*str*) – 创建时的桶名



* **Returns**

    返回一个 bool ，表示删除是否成功



* **Raises**

    **ClientError** – 删除发生错误



#### delete_object(bucket, key)
删除桶的对象，或者说文件


* **Parameters**

    
    * **bucket** (*str*) – 创建时的桶名


    * **key** (*str*) – 上传对象的 key



#### download_file(bucket: str = '', key: str = '', tos_url: str = '', target_file_path: str = '', target_dir_path: str = '', max_concurrence: int = 10)
下载TOS对象到本地

要下载对象的目标地址，两种方式选择其一：
- 通过 `bucket + key` 下载：:

```
download_file(bucket="xxx", key="xxx", ...)
```


* 通过 `tos_url` 下载：:

```
download_file(tos_url="tos://bucket.[xxxxx]/key", ...)
```

下载的文件保存到本地目标路径有两种方式： target_file_path 或


* 通过 `target_file_path` 指定


* 通过 `target_dir_path` 指定，实际保存的文件名为key 或者 tos_url.substringAfterLast(“/”)


* **Parameters**

    
    * **bucket** (*str*) – bucket 名


    * **key** (*str*) – object 的 key，比如 key=\`\`put/you/path/xxxx/yyy\`\`


    * **tos_url** (*str*) – 对象的 tos 链接


    * **file_path** (*str*) – 本地保存的目标文件路径


    * **dir_path** (*str*) – 本地保存的目标目录路径


    * **max_concurrence** (*int*) – 最大并发数量，控制下载速度



* **Returns**

    返回下载文件路径



* **Raises**

    **ValueError** – 参数填写错误



#### download_files(bucket: str = '', keys: list = [], tos_urls: list = [], target_file_paths: list = [], target_dir_path: str = '', parallelism=1)
下载多个TOS对象到本地

要下载的源文件有两种指定方式：
- 通过 `bucket + keys` 指定：:

```
download_files(bucket="your_bucket_name", keys=["xxx","yyy", ...], ...)
```


* 通过 `tos_urls` 指定：:

```
download_files(tos_urls=["tos://you_bucket_name]/xxx", "tos://you_bucket_name]/yyy", ....], ...)
```

下载的文件保存到本地目标路径有两种方式：


* 通过 target_file_paths\` 指定，需要和要下载的源对象列表长度一致


* 通过 `target_dir_path` 指定，所有文件保存到该目录下，，实际保存的文件名为对应的key 或者 对应的tos_url.substringAfterLast(“/”)


* **Parameters**

    
    * **bucket** (*str*) – bucket 名


    * **keys** (*list*) – object 的 key，比如 key=”put/you/path/xxxx/yyy”


    * **tos_urls** (*list*) – 对象的 tos 链接集合


    * **target_file_paths** (*list*) – 本地保存的目标路径的列表，与 keys 或者 tos_urls 一一对应


    * **target_dir_path** (*str*) – 本地保存的目标目录


    * **parallelism** (*int*) – 并发数量，控制下载速度



* **Returns**

    返回下载文件集路径的 list



* **Raises**

    **ValueError** – 参数填写错误



#### get_object(bucket, key)
获取 bucket 一个对象


* **Parameters**

    
    * **bucket** (*str*) – bucket 名


    * **key** (*str*) – 对应 object 的 key



* **Returns**

    返回一个下载结果的 dict



#### list_buckets()
列出用户的所有桶


* **Returns**

    返回一个 `list[str]` , 每个元素都是一个桶名。



#### list_objects(bucket, max_keys, marker='', delimiter='', encoding_type='url', prefix='')
列出桶里的对象, 最多一次列出 1000 个


* **Parameters**

    
    * **bucket** (*str*) – 创建时的桶名


    * **delimiter** (*str*) – 分组 key 的 一个字符


    * **encoding_type** (*str*) – key 的编码形式，比如 encoding_type = “uft-8” 或者 “url”


    * **marker** (*str*) – 设置 key 的遍历起点，可用于大量对象的分段查询


    * **max_keys** (*int*) – 返回 key 数量上限


    * **prefix** (*str*) – 限制返回对象的 key 前缀



* **Returns**

    返回一个 dict 对象，包含返回对象
    比如：:

    ```
    {
        'IsTruncated': True|False,
        'Marker': 'string',
        'NextMarker': 'string',
        'Contents': [
            {
                'Key': 'string',
                'LastModified': datetime(2015, 1, 1),
                'ETag': 'string',
                'Size': 123,
                'StorageClass': 'STANDARD'|'REDUCED_REDUNDANCY'|'GLACIER'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'DEEP_ARCHIVE'|'OUTPOSTS',
                'Owner': {
                    'DisplayName': 'string',
                    'ID': 'string'
                }
            },
        ],
        'Name': 'string',
        'Prefix': 'string',
        'Delimiter': 'string',
        'MaxKeys': 123,
        'CommonPrefixes': [
            {
                'Prefix': 'string'
            },
        ],
        'EncodingType': 'url'
    }
    ```




#### put_object(bucket, key, body)
上传对象到 bucket

大小不应该超过 5MB；更推荐用 `upload_file`


* **Parameters**

    
    * **bucket** (*str*) – 上传 bucket 的名


    * **key** (*str*) – 上传 object 的 key，比如 key=\`\`put/you/path/xxxx/yyy\`\`


    * **body** (*str*) – file-like object, 比如 `with open(flie, "rb") as f`



* **Returns**

    返回一个上传结果的 dict



#### upload_file(file_path, bucket, key=None, part_size=20971520)
上传文件到 bucket


* **Parameters**

    
    * **file_path** (*str*) – 上传文件的路径


    * **bucket** (*str*) – 上传 bucket 名


    * **key** (*str*) – 上传 object 的 key，比如 key=”put/you/path/xxxx/yyy”


    * **part_size** (*str*) – 切片上传的 size



#### upload_file_low_level(file_path, bucket, key=None, part_size=20971520)
相比 upload_file，更精细化的上传文件方式


* **Parameters**

    
    * **file_path** (*str*) – 上传文件的路径


    * **bucket** (*str*) – 上传 bucket 名


    * **key** (*str*) – 上传 object 的 key


    * **part_size** (*str*) – 切片上传的 size


## volcengine_ml_platform.io.tos_dataset module

## Module contents
