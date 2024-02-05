from src.converter import Converter
from src.enums import FORMAT, RENDER_MODE

# Convert to mercator (GPU)
Converter.convert(
    input="./data/Height.png",
    output="./data/Height_out.png",
    format=FORMAT.TO_MERCATOR,
    mode=RENDER_MODE.GPU)

# Convert to equirectangular (CPU)
Converter.convert(
    input="./data/Height.png",
    output="./data/Height_out.png",
    format=FORMAT.TO_EQUIRECTANGULAR,
    mode=RENDER_MODE.GPU)