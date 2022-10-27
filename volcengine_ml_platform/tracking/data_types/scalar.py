from volcengine_ml_platform.tracking.data_types.base import Base


class Scalar(Base):

    __TYPE__ = "scalar"

    def __init__(self, value):
        self.value = value

    @property
    def step_item(self):
        return {
            "Type": self.__TYPE__,
            "Scalar": {
                "Value": self.value
            }
        }
