from src.converter import Converter
from src.enums import FORMAT, RENDER_MODE, SAMPLING

### GPU ###

# # Convert to mercator
Converter.convert(
    input="./img/equi.png",
    output="./output/equi_to_merc_GPU_LINEAR.png",
    format=FORMAT.TO_MERCATOR)

Converter.convert(
    input="./img/equi.png",
    output="./output/equi_to_merc_GPU_NEAREST.png",
    format=FORMAT.TO_MERCATOR,
    sampling=SAMPLING.NEAREST)

# Convert to equirectangular
Converter.convert(
    input="./img/merc.jpg",
    output="./output/merc_to_equi_GPU_LINEAR.jpg",
    format=FORMAT.TO_EQUIRECTANGULAR)

Converter.convert(
    input="./img/merc.jpg",
    output="./output/merc_to_equi_GPU_NEAREST.jpg",
    format=FORMAT.TO_EQUIRECTANGULAR,
    sampling=SAMPLING.NEAREST)

### CPU ###

# Convert to mercator
Converter.convert(
    input="./img/equi.png",
    output="./output/equi_to_merc_CPU.png",
    format=FORMAT.TO_MERCATOR,
    mode=RENDER_MODE.CPU)

# Convert to equirectangular
Converter.convert(
    input="./img/merc.jpg",
    output="./output/merc_to_equi_CPU.jpg",
    format=FORMAT.TO_EQUIRECTANGULAR,
    mode=RENDER_MODE.CPU)