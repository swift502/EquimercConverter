from src.converter import Converter
from src.enums import CONVERSION, DEVICE, SAMPLING

### GPU ###

# Convert to mercator
Converter.convert(
    input="./img/equi.png",
    output="./output/equi_to_merc_GPU_LINEAR.png",
    conversion=CONVERSION.TO_MERCATOR)

# Nearest sampling
Converter.convert(
    input="./img/equi.png",
    output="./output/equi_to_merc_GPU_NEAREST.png",
    conversion=CONVERSION.TO_MERCATOR,
    sampling=SAMPLING.NEAREST)

# Convert to equirectangular
Converter.convert(
    input="./img/merc.jpg",
    output="./output/merc_to_equi_GPU_LINEAR.jpg",
    conversion=CONVERSION.TO_EQUIRECTANGULAR)

# Nearest sampling
Converter.convert(
    input="./img/merc.jpg",
    output="./output/merc_to_equi_GPU_NEAREST.jpg",
    conversion=CONVERSION.TO_EQUIRECTANGULAR,
    sampling=SAMPLING.NEAREST)

### CPU ###

# Convert to mercator
Converter.convert(
    input="./img/equi.png",
    output="./output/equi_to_merc_CPU.png",
    conversion=CONVERSION.TO_MERCATOR,
    mode=DEVICE.CPU)

# Convert to equirectangular
Converter.convert(
    input="./img/merc.jpg",
    output="./output/merc_to_equi_CPU.jpg",
    conversion=CONVERSION.TO_EQUIRECTANGULAR,
    mode=DEVICE.CPU)