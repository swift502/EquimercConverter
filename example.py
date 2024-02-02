from src.converter import Converter, ConversionType

# Convert equirectangular to mercator
Converter.convert(
    input="./data/equi.png",
    output="./data/equi_to_merc.png",
    mode=ConversionType.TO_MERCATOR)

# Convert mercator to equirectangular
Converter.convert(
    input="./data/merc.png",
    output="./data/merc_to_equi.png",
    mode=ConversionType.TO_EQUIRECTANGULAR)