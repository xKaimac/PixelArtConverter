from src.PixelArtConverter import PixelArtConverter

def main():
    cat = "../assets/test images/input/cat.avif"
    converter = PixelArtConverter(image_filepath=cat, scale_factor=0.02)

    converter.convert()

main()