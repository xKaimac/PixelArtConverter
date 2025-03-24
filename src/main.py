import os

from src.PixelArtConverter import PixelArtConverter
import sys

def main():
    image_filepath = "/Users/kaimac/PycharmProjects/PixelArtConverter/assets/input/test.gif"
    kernel_dimensions = (9, 9)
    scale_factor=0.02

    if len(sys.argv) > 1:
        image_filepath = sys.argv[1]

    if len(sys.argv) > 2:
        kernel_dimensions = sys.argv[2]

    if len(sys.argv) > 3:
        scale_factor = float(sys.argv[3])

    filepath_is_directory = os.path.isdir(image_filepath)

    if filepath_is_directory:
        for file in os.listdir(image_filepath):
            try:
                filepath = os.path.join(image_filepath, file)
                converter = PixelArtConverter(
                    image_filepath=filepath,
                    kernel_dimensions=kernel_dimensions,
                    scale_factor=scale_factor,
                )
                converter.convert()
            except Exception as e:
                print(e)
                continue
    else:
        converter = PixelArtConverter(
            image_filepath=image_filepath,
            kernel_dimensions=kernel_dimensions,
            scale_factor=scale_factor,
        )
        converter.convert()

main()
