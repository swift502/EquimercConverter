import argparse
from src.enums import CONVERSION, DEVICE, SAMPLING
from src.converter import Converter
import os

def append_suffix(filename, suffix):
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}{suffix}{ext}"
    return new_filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="the input file path")
    parser.add_argument('--to_mercator', action='store_true', help="convert to mercator")
    parser.add_argument('--to_equirectangular', action='store_true', help="convert to equirectangular")
    parser.add_argument('--nearest', action='store_true', help="force nearest sampling for the stretching that will occur due to change of aspect ratio")
    parser.add_argument('--cpu', action='store_true', help="convert using CPU, much slower and doesn't support linear sampling")

    args = parser.parse_args()

    if args.to_mercator:
        Converter.convert(
            input=args.input,
            output=append_suffix(args.input, "_converted_to_mercator"),
            conversion=CONVERSION.TO_MERCATOR,
            sampling=SAMPLING.NEAREST if args.nearest else SAMPLING.LINEAR,
            device=DEVICE.CPU if args.cpu else DEVICE.GPU)

    if args.to_equirectangular:
        Converter.convert(
            input=args.input,
            output=append_suffix(args.input, "_converted_to_equirectangular"),
            conversion=CONVERSION.TO_EQUIRECTANGULAR,
            sampling=SAMPLING.NEAREST if args.nearest else SAMPLING.LINEAR,
            device=DEVICE.CPU if args.cpu else DEVICE.GPU)

    if not args.to_mercator and not args.to_equirectangular:
        print("\033[31mError:\033[0m No conversion specified, use the --to_mercator or --to_equirectangular arguments to specify the conversion type.\n")

if __name__ == "__main__":
    main()