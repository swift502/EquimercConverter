from enum import Enum

class CONVERSION(Enum):
    TO_MERCATOR = 1
    TO_EQUIRECTANGULAR = 2

class DEVICE(Enum):
    GPU = 1
    CPU = 2

class SAMPLING(Enum):
    LINEAR = 1
    NEAREST = 2