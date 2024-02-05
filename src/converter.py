import sys
from PIL import Image
from pathlib import Path
import math

class Converter:
    def convert(input: str, output: str, mode: MODE):
        try:
            file = Path(input)

            if mode == Converter.MODE.TO_EQUIRECTANGULAR:
                print(f"\nConverting \"{file.name}\" to equirectangular.")
            else:
                print(f"\nConverting \"{file.name}\" to mercator.")

            image = Image.open(file)
            
            newImage.save(output)
            print(f"\033[32mSuccess!\033[0m")

        except Exception as e:
            print("\033[31mError:\033[0m")
            print(e)
    