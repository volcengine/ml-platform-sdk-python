import json
import os

import numpy as np
import requests
from PIL import Image

END_POINT = "inference-demo.byted.org/s-20210803143929-vfspk/rest"
CLASSES = [
    "pink primrose",
    "hard-leaved pocket orchid",
    "canterbury bells",
    "sweet pea",
    "wild geranium",
    "tiger lily",
    "moon orchid",
    "bird of paradise",
    "monkshood",
    "globe thistle",  # 00 - 09
    "snapdragon",
    "colt's foot",
    "king protea",
    "spear thistle",
    "yellow iris",
    "globe-flower",
    "purple coneflower",
    "peruvian lily",
    "balloon flower",
    "giant white arum lily",  # 10 - 19
    "fire lily",
    "pincushion flower",
    "fritillary",
    "red ginger",
    "grape hyacinth",
    "corn poppy",
    "prince of wales feathers",
    "stemless gentian",
    "artichoke",
    "sweet william",  # 20 - 29
    "carnation",
    "garden phlox",
    "love in the mist",
    "cosmos",
    "alpine sea holly",
    "ruby-lipped cattleya",
    "cape flower",
    "great masterwort",
    "siam tulip",
    "lenten rose",  # 30 - 39
    "barberton daisy",
    "daffodil",
    "sword lily",
    "poinsettia",
    "bolero deep blue",
    "wallflower",
    "marigold",
    "buttercup",
    "daisy",
    "common dandelion",  # 40 - 49
    "petunia",
    "wild pansy",
    "primula",
    "sunflower",
    "lilac hibiscus",
    "bishop of llandaff",
    "gaura",
    "geranium",
    "orange dahlia",
    "pink-yellow dahlia",  # 50 - 59
    "cautleya spicata",
    "japanese anemone",
    "black-eyed susan",
    "silverbush",
    "californian poppy",
    "osteospermum",
    "spring crocus",
    "iris",
    "windflower",
    "tree poppy",  # 60 - 69
    "gazania",
    "azalea",
    "water lily",
    "rose",
    "thorn apple",
    "morning glory",
    "passion flower",
    "lotus",
    "toad lily",
    "anthurium",  # 70 - 79
    "frangipani",
    "clematis",
    "hibiscus",
    "columbine",
    "desert-rose",
    "tree mallow",
    "magnolia",
    "cyclamen ",
    "watercress",
    "canna lily",  # 80 - 89
    "hippeastrum ",
    "bee balm",
    "pink quill",
    "foxglove",
    "bougainvillea",
    "camellia",
    "mallow",
    "mexican petunia",
    "bromelia",
    "blanket flower",  # 90 - 99
    "trumpet creeper",
    "blackberry lily",
    "common tulip",
    "wild rose",
]


def request_demo():
    try:
        headers = {"content-type": "application/json"}
        test_img_path = np.os.path.join(
            os.path.dirname(__file__),
            "test_sample/34.jpg",
        )
        image = np.array(Image.open(test_img_path))
        data = json.dumps(
            {"signature_name": "serving_default", "inputs": [image.tolist()]},
        )
        json_response = requests.post(
            f"http://{END_POINT}/v1/models/default:predict",
            data=data,
            headers=headers,
        )
        return json_response.json()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    rv = request_demo()
    preds = np.argmax(rv["outputs"], axis=-1)[0]
    print(CLASSES[preds])
