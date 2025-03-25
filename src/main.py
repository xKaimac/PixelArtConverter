import os

from numpy import require

from PixelArtConverter import PixelArtConverter
import argparse

def main():
    parser = argparse.ArgumentParser(description="Pixel Art Converter")

    # Command line argument setup
    parser.add_argument('-f', '--filepath', help='Filepath to the image or directory.', default='../assets/input/')
    parser.add_argument('-k', '--kernel_dimensions', help='The x dimension (integer) of the convolutional kernel. This is always square so just pass through one odd integer value. Higher value is a more condensed starting image.', default=9)
    parser.add_argument('-s', '--scale_factor', help='Floating point number from 0 - 1. The larger the value the more pixelated the image at the end.', default=0.05)

    args = parser.parse_args()

    # Take values from the user, else default
    image_filepath = args.filepath
    kernel_dimensions = (int(args.kernel_dimensions), int(args.kernel_dimensions))
    scale_factor = float(args.scale_factor)

    print(image_filepath, kernel_dimensions, scale_factor)

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
