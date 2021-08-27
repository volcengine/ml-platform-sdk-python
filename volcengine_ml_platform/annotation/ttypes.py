class AnnotationTemplate:
    TextClassification = 1
    TextEntity = 2
    ImageClassification = 3
    ImageDetection = 4
    ImageSegmentation = 5
    VideoClassification = 6
    TabularPrediction = 101
    TimeSeriesPrediction = 102

    _VALUES_TO_NAMES = {
        1: 'TextClassification',
        2: 'TextEntity',
        3: 'ImageClassification',
        4: 'ImageDetection',
        5: 'ImageSegmentation',
        6: 'VideoClassification',
        101: 'TabularPrediction',
        102: 'TimeSeriesPrediction',
    }

    _NAMES_TO_VALUES = {
        'TextClassification': 1,
        'TextEntity': 2,
        'ImageClassification': 3,
        'ImageDetection': 4,
        'ImageSegmentation': 5,
        'VideoClassification': 6,
        'TabularPrediction': 101,
        'TimeSeriesPrediction': 102,
    }


class AnnotationDataType:
    SingleSelector = 1
    MultipleSelector = 2
    BlankFilling = 3

    _VALUES_TO_NAMES = {
        1: 'SingleSelector',
        2: 'MultipleSelector',
        3: 'BlankFilling',
    }

    _NAMES_TO_VALUES = {
        'SingleSelector': 1,
        'MultipleSelector': 2,
        'BlankFilling': 3,
    }


class AnnotationStatus:
    Init = 1
    Marked = 2
    Invalid = 3

    _VALUES_TO_NAMES = {
        1: 'Init',
        2: 'Marked',
        3: 'Invalid',
    }

    _NAMES_TO_VALUES = {
        'Init': 1,
        'Marked': 2,
        'Invalid': 3,
    }


class Data:
    """
    Attributes:
     - ImageURL
     - VideoURL
     - TextURL
     - FilePath
    """

    def __init__(
        self,
        ImageURL=None,
        VideoURL=None,
        TextURL=None,
        FilePath=None,
    ):
        self.ImageURL = ImageURL
        self.VideoURL = VideoURL
        self.TextURL = TextURL
        self.FilePath = FilePath


class TextSelector:
    """
    Attributes:
     - Pos
     - Len
    """

    def __init__(
        self,
        Pos=None,
        Len=None,
    ):
        self.Pos = Pos
        self.Len = Len


class AnnotationData:
    """
    Attributes:
     - Type
     - Options
     - Label
     - Labels
    """

    def __init__(
        self,
        Type=None,
        Options=None,
        Label=None,
        Labels=None,
    ):
        self.Type = Type
        self.Options = Options
        self.Label = Label
        self.Labels = Labels


class AnnotationResult:
    """
    Attributes:
     - Bbox
     - Segmentation
     - Text
     - Data
    """

    def __init__(
        self,
        Bbox=None,
        Segmentation=None,
        Text=None,
        data=None,
    ):
        self.Bbox = Bbox
        self.Segmentation = Segmentation
        self.Text = Text
        self.Data = data


class Annotation:
    """
    Attributes:
     - Type
     - ItemID
     - Result
     - Status
    """

    def __init__(
        self,
        Type=None,
        ItemID=None,
        Result=None,
        Status=None,
    ):
        self.Type = Type
        self.ItemID = ItemID
        self.Result = Result
        self.Status = Status


class Resolution:
    """
    Attributes:
     - Width
     - Height
    """

    def __init__(
        self,
        Width=None,
        Height=None,
    ):
        self.Width = Width
        self.Height = Height


class ImagePayload:
    """
    Attributes:
     - TOSURL
     - MimeType
     - ContentURL
     - ThumbnailURL
     - Resolution
    """

    def __init__(
        self,
        TOSURL=None,
        MimeType=None,
        ContentURL=None,
        ThumbnailURL=None,
        resolution=None,
    ):
        self.TOSURL = TOSURL
        self.MimeType = MimeType
        self.ContentURL = ContentURL
        self.ThumbnailURL = ThumbnailURL
        self.Resolution = resolution


class VideoPayload:
    """
    Attributes:
     - TOSURL
     - MimeType
     - ContentURL
     - ThumbnailURL
     - duration
     - Resolution
    """

    def __init__(
        self,
        TOSURL=None,
        MimeType=None,
        ContentURL=None,
        ThumbnailURL=None,
        duration=None,
        resolution=None,
    ):
        self.TOSURL = TOSURL
        self.MimeType = MimeType
        self.ContentURL = ContentURL
        self.ThumbnailURL = ThumbnailURL
        self.duration = duration
        self.Resolution = resolution


class TextPayload:
    """
    Attributes:
     - TOSURL
     - TrucatedContent
    """

    def __init__(
        self,
        TOSURL=None,
        TrucatedContent=None,
    ):
        self.TOSURL = TOSURL
        self.TrucatedContent = TrucatedContent


class Payload:
    """
    Attributes:
     - Image
     - Video
     - Text
    """

    def __init__(
        self,
        Image=None,
        Video=None,
        Text=None,
    ):
        self.Image = Image
        self.Video = Video
        self.Text = Text


class FileLine:
    """
    Attributes:
     - Data
     - Annotation
     - Payload
    """

    def __init__(
        self,
        data=None,
        annotation=None,
        payload=None,
    ):
        self.Data = data
        self.Annotation = annotation
        self.Payload = payload
