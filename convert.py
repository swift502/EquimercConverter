import argparse
from src.enums import FORMAT, RENDER_MODE, SAMPLING
from src.converter import Converter

def main():
    parser = argparse.ArgumentParser(description="Copy content from one file to another.")
    parser.add_argument('input', help="Path to the input file")
    parser.add_argument('output', help="Path to the output file")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose mode")
    # parser.add_argument('--color', choices=[Color.RED, Color.BLUE], help="Specify the color (red or blue)")

    args = parser.parse_args()


if __name__ == "__main__":
    main()