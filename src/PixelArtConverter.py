"""
The class that the user will interact with. This class manages the kernel
"""
import cv2

from ImageHandler import ImageHandler
from Kernel import Kernel

class PixelArtConverter:
    _image_handler_ = None
    _kernel_ = None
    _image_filepath_ = None
    _kernel_dimensions_ = None
    _pixel_image_ = None
    _image_format_ = None

    def __init__(
            self,
            image_filepath=None,
            kernel_dimensions=(9,9),
            scale_factor=1
    ):
        self._image_handler_ = ImageHandler(image_filepath=image_filepath)
        self._image_format_ = self._image_handler_.get_image_format()
        self._image_filepath_ = self._image_handler_.get_image_filepath()
        self._kernel_dimensions_ = kernel_dimensions

        image_height, image_width, channels = self._image_handler_.get_image_shape()

        chunk_size = int(min(image_width, image_height) * scale_factor)

        self._kernel_ = Kernel(
            image=self._image_handler_.get_image(),
            kernel_dimensions=self._kernel_dimensions_,
            image_filepath=self._image_filepath_,
            chunk_size=chunk_size
        )

    def convert(self):
        image = self._kernel_.sweep()

        self._image_handler_.save_image(
            image=image,
            image_filepath=self._image_filepath_
        )
