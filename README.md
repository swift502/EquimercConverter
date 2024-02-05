![](img/preview.png)

# Equirectangular-Mercator Projection Converter

Bi-directional image projection converter. Converts images between equirectangular and mercator projections. Expands the image to new aspect ratio and fills in missing pixels using nearest sampling.

Features a fast GPU and a slower CPU conversion implementations:

- The GPU version uses [moderngl](https://github.com/moderngl/moderngl) to transform the image using shaders and then saves it using Pillow.
- The CPU version simply uses [Pillow](https://github.com/python-pillow/Pillow) to modify every pixel individually.

## Setup

1. Install [Python 3.11+](https://www.python.org/downloads/)

1. Install requirements
    ```
    pip install -r requirements.txt
    ```

## Usage

### CLI

#### Usage:
```shell
python convert.py input output {m,e} [--nearest] [--cpu]
```

#### Examples:

Convert equi.png (equirectangular) to merc.png (mercator)

```shell
python convert.py equi.png merc.png m
```

Convert equi.png (equirectangular) to merc.png (mercator)

```shell
python convert.py equi.png merc.png m
```

| Arguments | Description |
| --: | :-- |
| input | The input file path |
| output | The output file path |
| {m,e} | Projection to convert the image to: "m" for mercator, "e" for equirectangular. |
| -h, --help | Show help |
| --nearest | Use nearest sampling for the stretching that will occur due to change of aspect ratio. Only used for GPU rendering. |
| --cpu | Use CPU for rendering. Much slower and doesn't support linear sampling. |

### Python

You can use the Converter class directly in Python. Check out the [demo script](demo.py) to see how to run conversions in code.

## Limitations

The conversion process can't handle longitude angles of 85+ degress well. Converted images may display issues around the top and bottom borders.

## Python package

If anyone wants to transform this into a functional, publishable package, feel free to fork the project and publish it. I don't have enough experience doing that and can't imagine many people will use this thing to make the extra hassle worthwhile.