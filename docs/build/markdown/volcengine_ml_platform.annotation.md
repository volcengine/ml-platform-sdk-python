# volcengine_ml_platform.annotation package

## Submodules

## volcengine_ml_platform.annotation.annotation module


### class volcengine_ml_platform.annotation.annotation.Annotation(manifest_file: Optional[str] = None)
Bases: `object`

annotation object


#### extract(index)
get annotation of the index line
:param index of annotation_data:


* **Returns**

    content of image/text
    annotation of data, diff data has diff struct



#### extract_annotation(manifest_line)

#### extract_annotation_with_data(manifest_line)
get content and annotation
:param manifest line data:


* **Returns**

    content of image/text
    annotation of data, diff data has diff struct



#### get_by_label(label)

### volcengine_ml_platform.annotation.annotation.get_annotation_section(annotation_line)

### volcengine_ml_platform.annotation.annotation.get_content(annotation_line)

### volcengine_ml_platform.annotation.annotation.get_data_section(annotation_line)
## volcengine_ml_platform.annotation.image_classification_annotation module


### class volcengine_ml_platform.annotation.image_classification_annotation.ImageClassificationAnnotation(manifest_file: Optional[str] = None)
Bases: `volcengine_ml_platform.annotation.annotation.Annotation`


#### extract_annotation(manifest_line)
## volcengine_ml_platform.annotation.image_detection_annotation module


### class volcengine_ml_platform.annotation.image_detection_annotation.ImageDetectionAnnotation(manifest_file: Optional[str] = None)
Bases: `volcengine_ml_platform.annotation.annotation.Annotation`


#### extract_annotation(manifest_line)
## volcengine_ml_platform.annotation.image_segmentation_annotation module


### class volcengine_ml_platform.annotation.image_segmentation_annotation.ImageSegmentationAnnotation(manifest_file: Optional[str] = None)
Bases: `volcengine_ml_platform.annotation.annotation.Annotation`


#### extract_annotation(manifest_line)
## volcengine_ml_platform.annotation.text_classification_annotation module


### class volcengine_ml_platform.annotation.text_classification_annotation.TextClassificationAnnotation(manifest_file: Optional[str] = None)
Bases: `volcengine_ml_platform.annotation.annotation.Annotation`


#### extract_annotation(manifest_line)
## volcengine_ml_platform.annotation.text_entity_annotation module


### class volcengine_ml_platform.annotation.text_entity_annotation.TextEntitySetAnnotation(manifest_file: Optional[str] = None)
Bases: `volcengine_ml_platform.annotation.annotation.Annotation`


#### extract_annotation(manifest_line)
## volcengine_ml_platform.annotation.ttypes module


### class volcengine_ml_platform.annotation.ttypes.Annotation(Type=None, ItemID=None, Result=None, Status=None)
Bases: `object`


### - Type()

### - ItemID()

### - Result()

### - Status()

### class volcengine_ml_platform.annotation.ttypes.AnnotationData(Type=None, Options=None, Label=None, Labels=None)
Bases: `object`


### - Type()

### - Options()

### - Label()

### - Labels()

### class volcengine_ml_platform.annotation.ttypes.AnnotationDataType()
Bases: `object`


#### BlankFilling( = 3)

#### MultipleSelector( = 2)

#### SingleSelector( = 1)

### class volcengine_ml_platform.annotation.ttypes.AnnotationResult(Bbox=None, Segmentation=None, Text=None, data=None)
Bases: `object`


### - Bbox()

### - Segmentation()

### - Text()

### - Data()

### class volcengine_ml_platform.annotation.ttypes.AnnotationStatus()
Bases: `object`


#### Init( = 1)

#### Invalid( = 3)

#### Marked( = 2)

### class volcengine_ml_platform.annotation.ttypes.AnnotationTemplate()
Bases: `object`


#### ImageClassification( = 3)

#### ImageDetection( = 4)

#### ImageSegmentation( = 5)

#### TabularPrediction( = 101)

#### TextClassification( = 1)

#### TextEntity( = 2)

#### TimeSeriesPrediction( = 102)

#### VideoClassification( = 6)

### class volcengine_ml_platform.annotation.ttypes.Data(ImageURL=None, VideoURL=None, TextURL=None, FilePath=None)
Bases: `object`


### - ImageURL()

### - VideoURL()

### - TextURL()

### - FilePath()

### class volcengine_ml_platform.annotation.ttypes.FileLine(data=None, annotation=None, payload=None)
Bases: `object`


### - Data()

### - Annotation()

### - Payload()

### class volcengine_ml_platform.annotation.ttypes.ImagePayload(TOSURL=None, MimeType=None, ContentURL=None, ThumbnailURL=None, resolution=None)
Bases: `object`


### - TOSURL()

### - MimeType()

### - ContentURL()

### - ThumbnailURL()

### - Resolution()

### class volcengine_ml_platform.annotation.ttypes.Payload(Image=None, Video=None, Text=None)
Bases: `object`


### - Image()

### - Video()

### - Text()

### class volcengine_ml_platform.annotation.ttypes.Resolution(Width=None, Height=None)
Bases: `object`


### - Width()

### - Height()

### class volcengine_ml_platform.annotation.ttypes.TextPayload(TOSURL=None, TrucatedContent=None)
Bases: `object`


### - TOSURL()

### - TrucatedContent()

### class volcengine_ml_platform.annotation.ttypes.TextSelector(Pos=None, Len=None)
Bases: `object`


### - Pos()

### - Len()

### class volcengine_ml_platform.annotation.ttypes.VideoPayload(TOSURL=None, MimeType=None, ContentURL=None, ThumbnailURL=None, duration=None, resolution=None)
Bases: `object`


### - TOSURL()

### - MimeType()

### - ContentURL()

### - ThumbnailURL()

### - duration()

### - Resolution()
## Module contents


### class volcengine_ml_platform.annotation.Annotation(manifest_file: Optional[str] = None)
Bases: `object`

annotation object


#### extract(index)
get annotation of the index line
:param index of annotation_data:


* **Returns**

    content of image/text
    annotation of data, diff data has diff struct



#### extract_annotation(manifest_line)

#### extract_annotation_with_data(manifest_line)
get content and annotation
:param manifest line data:


* **Returns**

    content of image/text
    annotation of data, diff data has diff struct



#### get_by_label(label)

### class volcengine_ml_platform.annotation.ImageClassificationAnnotation(manifest_file: Optional[str] = None)
Bases: `volcengine_ml_platform.annotation.annotation.Annotation`


#### extract_annotation(manifest_line)
