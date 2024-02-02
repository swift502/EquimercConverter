from src.converter import Converter

# Convert equirectangular to mercator
Converter.convert(
    input="./data/equi.png",
    output="./data/equi_to_merc.png",
    mode=Converter.MODE.TO_MERCATOR)

# Convert mercator to equirectangular
Converter.convert(
    input="./data/merc.jpg",
    output="./data/merc_to_equi.jpg",
    mode=Converter.MODE.TO_EQUIRECTANGULAR)