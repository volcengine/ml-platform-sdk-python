from volcengine_ml_platform.datasets.image_dataset import ImageDataset
from volcengine_ml_platform.datasets.text_dataset import TextDataset
from volcengine_ml_platform.datasets.video_dataset import VideoDataset


dataset_dict = {
    TextDataset: "TextURL",
    VideoDataset: "VideoURL",
    ImageDataset: "ImageURL",
}
