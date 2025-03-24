import os

import cv2

from src.PixelArtConverter import PixelArtConverter
import sys

def main():
    image_filepath = r"/Users/kaimac/Downloads/w3c_home_animation.gif"
    absolute_path = os.path.abspath(image_filepath)
    gif = cv2.VideoCapture(absolute_path)
    ret, frame = gif.read()

    frames = []

    if ret:
        frames.append(frame)

    while ret:
        ret, frame = gif.read()
        if not ret:
            break
        frames.append(frame)
        print(frame.shape)

    print(len(frames))

main()

