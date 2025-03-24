"""This class handles the uploading and reading of image files """
import os
import warnings

import cv2
import imageio
import numpy as np
import pillow_avif # Must import before PIL for the plugin to work
from PIL import Image


class ImageHandler:
    SUPPORTED_FORMATS = [
        '.jpg', '.jpeg', '.png', '.bmp', '.dib', '.jp2',
        '.webp', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm',
        '.sr', '.ras', '.tiff', '.tif', '.exr', 'hdr',
        '.pic', '.gif'
    ]
    _image_filepath_ = None
    _image_ = None
    _root_directory_ = os.path.dirname(__file__)

    def __init__(self, image_filepath = None):
        if image_filepath is not None:
            self.set_image_filepath(image_filepath)

        self._read_image()

    def _read_image(self):
        """
        Read image using OpenCV2
        """
        if self.get_image_format() == '.gif':
            gif = cv2.VideoCapture(self._image_filepath_)
            frames = []
            ret, frame = gif.read()
            frames.append(frame)

            while ret:
                ret, frame = gif.read()
                if not ret:
                    break
                frames.append(frame)

            self._image_ = frames
        else:
            self._image_ = cv2.imread(self._image_filepath_)

        if self._image_ is None:
            raise FileNotFoundError("Image file not found")

    def get_image_shape(self):
        """:returns the image dimensions"""
        if self.get_image_format() == '.gif':
            return self._image_[0].shape

        return self._image_.shape

    def get_image_format(self):
        """:returns the file extension of the image"""
        return self._image_filepath_[self._image_filepath_.rfind('.'):]

    def show_image(self):
        """Opens the image in a new window"""
        cv2.imshow('image', self._image_)
        cv2.waitKey(0)

    def _find_image_directory_(self, image_filepath):
        """
        Determines the type of slashes in the file path,
        then returns the directory that the file is contained in.

        :param image_filepath: The path to the image file
        :return The directory that the image is contained in
        """
        forward_slash = image_filepath.find('/') != -1

        if forward_slash:
            return image_filepath[0:image_filepath.rfind('/')]
        else:
            return image_filepath[0:image_filepath.rfind('\\')]

    def set_image_filepath(self, image_filepath):
        """
        Checks the passed filepath for validity, then sets the value
        """
        filepath_is_absolute = os.path.isabs(image_filepath)

        if image_filepath is not None:
            image_filename = image_filepath.split('\\')[-1]
            image_format = image_filename[image_filename.rfind('.'):]

            if image_format not in self.SUPPORTED_FORMATS:
                if image_format == '.avif':
                    image_filepath = self.convert_avif_to_jpg(
                        image_filename=image_filename,
                        image_filepath=image_filepath if filepath_is_absolute
                            else os.path.join(
                                self._root_directory_,
                                image_filepath
                        )
                    )
                else:
                    warnings.warn(f"WARNING: Unsupported image format for {image_filename}")
        else:
            raise Exception("Invalid filepath provided. Unable to locate image.")

        if filepath_is_absolute:
            self._image_filepath_ = image_filepath
        else:
            self._image_filepath_ = os.path.join(
                self._root_directory_,
                image_filepath
            )

    def save_image(self, image, image_filepath):
        """
        Saves the given image to the output directory within the project.

        :param image: The blurred image, created by self._condense_pixel_values_()
        :param image_filepath: The path to the original image file, used to get the image name
        """
        directory, filename = os.path.split(image_filepath)
        new_filename = f"../output/pixelated_{filename}"
        new_filepath = os.path.join(directory, new_filename)

        print(f"Saving image to {new_filepath}")

        if self.get_image_format() == '.gif':
            if isinstance(image, np.ndarray):
                frames = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB)]
            elif isinstance(image, list):
                frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in image]

            imageio.mimsave(new_filepath, frames, format="GIF")
        else:
            cv2.imwrite(new_filepath, image)

    def get_image_filepath(self):
        """:returns the filepath of the image"""
        return self._image_filepath_

    def get_image(self):
        """:returns the image as a numpy array"""
        return self._image_

    def convert_avif_to_jpg(self, image_filename, image_filepath):
        """
        Converts a .avif file to .jpg

        :param image_filename: name of the image file with no directory information
        :param image_filepath: path to the image file including the filename
        :return The filepath of the converted file

        The usage of this function gets the filename prior to its calling
        """
        converted_filename = image_filename.split('.')[0] + '.jpg'
        image_directory = self._find_image_directory_(image_filepath)
        converted_filepath = os.path.join(image_directory, converted_filename)

        img = Image.open(image_filepath)
        img.save(converted_filepath)

        return converted_filepath
