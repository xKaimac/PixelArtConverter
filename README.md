# Pixel Art Converter!

A simple tool that turns most image formats (including GIFs) into pixel art.

## How it works

1. Each image gets initial processing by passing an $n^2$ convolution kernel over the image, such that $n = 2m-1$ for any integer $m$.
   - This kernel will condense each pixel to have the same value as the $n^2-1$ surrounding pixels, effectively blurring the image.
2. This new image is saved into a temp folder for further processing
3. The image is then split up into $k^2$ pixel chunks, where $k$ is the minimum value from the height or width of the image multiplied by a scale of 0 to 1, where 1 gives the largest chunk size.
4. These chunks are passed over to find the most frequently occuring pixel value, colouring every pixel inside that chunk to the found value.
5. In the case of GIFs, this process is completed for each individual frame of the GIF individually, retaining the original framerate at the end.

## How to use it

1. Clone the project into your desired location with `git clone https://www.github.com/xKaimac/PixelArtConverter.git`
   - **NOTE:** It is highly recommended to use a virtual environment for this, like all Python projects. This project was tested on Python 3.13.
3. Install the dependencies by running `pip install -r requirements.txt` from the root directory of the project.
4. Move your desired input files into `$PROJECT_ROOT/assets/input/`
   - By default, this program will convert all files in the given folder, if you only want to change one image, passing through the path to that single file also works.
5. Run the program with `python main.py`
   - Other arguments can be found under [Arguments](#Arguments)
6. Find your new pixel art files in `$PROJECT_ROOT/assets/output/`

## Arguments
#### All arguments can be ran with `python main.py -$ARG` or `python main.py --$ARGUMENT`

- -h, --help
  - Shows the help menu and exits
- -k _FILEPATH_, --kernel_dimensions _FILEPATH_
  - The x dimension (integer) of the convolutional kernel. This is always square so just pass through one odd integer value. Higher value is a more condensed starting image.
- -s _SCALE_FACTOR_, --scale_factor _SCALE_FACTOR_
  - Floating point number from 0 to 1. The larger the value the more pixelated the image at the end.

### TODO
- Look at mapping the pixel values to the closest 256 value colour palette for a more retro look
- Try to find a magic number for scaling
- Get gifs to loop infinitely
- if the given directory isn't "input", just create an output folder in the passed directory to work with files anywhere
