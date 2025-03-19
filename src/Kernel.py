"""
This class represents the Kernel that will be passing over images to condense pixel values.
"""
import os
import cv2
import numpy as np

class Kernel:
    _image_ = None
    _kernel_dimensions_ = None
    _temp_image_filepath_ = None
    _image_filepath_ = None
    _chunk_size_ = None

    def __init__(self,
                 image,
                 image_filepath,
                 kernel_dimensions=(3, 3),
                 chunk_size=50
        ):
        self._image_ = image
        self._kernel_dimensions_ = kernel_dimensions
        self._image_filepath_ = image_filepath
        self._chunk_size_ = chunk_size

    def sweep(self):
        self._condense_pixel_values_()

        return  self._image_to_chunks_()

    def _condense_pixel_values_(self):
        """
        Blurs a given image by passing an n*n convolutional filter over the image
        such that n = 2m - 1 for any integer m
        :param filepath: the path to the image file
        """
        condensed_image = cv2.blur(self._image_, self._kernel_dimensions_)
        self._save_temp_image_(
            condensed_image=condensed_image,
            image_filepath=self._image_filepath_
        )

    def _image_to_chunks_(self):
        """
        Applies a pixelation effect by dividing an image into chunk
        and colouring each chunk with its most common colour.

        :param chunk_size: Size of each chunk (e.g., 10 means 10x10 chunks)
        :return: Pixelated image
        """
        image = cv2.imread(self._temp_image_filepath_)

        h, w = image.shape[:2]
        output = np.zeros_like(image)

        for y in range(0, h, self._chunk_size_):
            for x in range(0, w, self._chunk_size_):
                # Extract chunk
                chunk = image[y:y + self._chunk_size_, x:x + self._chunk_size_]

                # Get most common colour
                dominant_colour = self._get_most_common_colour_(chunk=chunk)

                # Fill chunk with dominant colour
                output[y:y + self._chunk_size_, x:x + self._chunk_size_] = dominant_colour

        return output

    def _get_most_common_colour_(self, chunk):
        """
        Finds the most common colour in a given image chunk.

        :param chunk: A sub-array (image chunk)
        :return: Most frequent colour in the chunk
        """
        # Flatten chunk to (N, 3)
        reshaped = chunk.reshape(-1, 3)

        # Count unique colour
        colours, counts = np.unique(reshaped, axis=0, return_counts=True)

        # Get the most frequent colour
        return colours[np.argmax(counts)]

    def _save_temp_image_(self, condensed_image, image_filepath):
        """
        Saves the condensed image to the temp directory within the project.

        :param condensed_image: The blurred image, created by self._condense_pixel_values_()
        :param image_filepath: The path to the original image file, used to get the image name
        """
        directory, filename = os.path.split(image_filepath)
        root_directory = os.path.dirname(__file__)
        new_filename = f"condensed_{filename}"
        new_filepath = os.path.join(
            root_directory,
            "assets",
            "temp",
            new_filename
        )
        cv2.imwrite(new_filepath, condensed_image)
        self._temp_image_filepath_ = new_filepath