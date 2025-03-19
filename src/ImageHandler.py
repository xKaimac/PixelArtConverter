"""This class handles the uploading and reading of image files """
import os
import cv2
import pillow_avif # Must import before PIL for the plugin to work
from PIL import Image

class ImageHandler:
    SUPPORTED_FORMATS = [
        '.jpg', '.jpeg', '.png', '.bmp', '.dib', '.jp2',
        '.webp', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm',
        '.sr', '.ras', '.tiff', '.tif', '.exr', 'hdr',
        '.pic'
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
        self._image_ = cv2.imread(self._image_filepath_)
        if self._image_ is None:
            raise FileNotFoundError("Image file not found")

    def get_image_shape(self):
        return self._image_.shape

    def get_image_type(self):
        return self._image_filepath_.split('.')[-1]

    def show_image(self):
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
        file_exists = False
        filepath_is_absolute = os.path.isabs(image_filepath)

        if image_filepath is not None:
            # Pass through the correct filepath depending on whether it's relative or absolute
            image_directory = os.path.join(
                "" if filepath_is_absolute else self._root_directory_,
                self._find_image_directory_(image_filepath
            ))
            image_filename = image_filepath.split('/')[-1]
            image_format = image_filename[image_filename.rfind('.'):]

            for file in os.listdir(image_directory):
                if file == image_filename:
                    file_exists = True

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
                            raise Exception("Unsupported image format supplied.")

        if not file_exists:
            raise Exception("Invalid filepath provided. Unable to locate image.")

        print("filepath before " + image_filepath)

        if filepath_is_absolute:
            self._image_filepath_ = image_filepath
        else:
            self._image_filepath_ = os.path.join(
                self._root_directory_,
                image_filepath
            )

    def save_image(self, image, image_filepath):
        directory, filename = os.path.split(image_filepath)
        new_filename = f"../output/pixelated_{filename}"
        new_filepath = os.path.join(directory, new_filename)
        cv2.imwrite(new_filepath, image)

    def get_image_filepath(self):
        return self._image_filepath_

    def get_image(self):
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