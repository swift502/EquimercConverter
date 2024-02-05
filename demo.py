from src.converter import Converter

# Convert equirectangular to mercator
Converter.convert(
    input="./data/Height.png",
    output="./data/Height_out.png",
    mode=Converter.MODE.TO_MERCATOR)