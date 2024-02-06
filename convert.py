import argparse
from src.enums import CONVERSION, DEVICE, SAMPLING
from src.converter import Converter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="the input file path")
    parser.add_argument('output', help="the output file path")
    parser.add_argument('conversion', choices=["m", "e"], help="projection to convert the image to: \"m\" for mercator, \"e\" for equirectangular")
    parser.add_argument('--nearest', action='store_true', help="force nearest sampling for the stretching that will occur due to change of aspect ratio")
    parser.add_argument('--cpu', action='store_true', help="convert using CPU, much slower and doesn't support linear sampling")

    args = parser.parse_args()

    if args.conversion == "m":
        conversion = CONVERSION.TO_MERCATOR
    if args.conversion == "e":
        conversion = CONVERSION.TO_EQUIRECTANGULAR

    Converter.convert(
        input=args.input,
        output=args.output,
        conversion=conversion,
        sampling=SAMPLING.NEAREST if args.nearest else SAMPLING.LINEAR,
        device=DEVICE.CPU if args.cpu else DEVICE.GPU)

if __name__ == "__main__":
    main()