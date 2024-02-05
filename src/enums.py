from enum import Enum

class FORMAT(Enum):
    TO_EQUIRECTANGULAR = 1
    TO_MERCATOR = 2

class RENDER_MODE(Enum):
    CPU = 1
    GPU = 2

class SAMPLING(Enum):
    LINEAR = 1
    NEAREST = 2