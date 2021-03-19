#   Copyright 2021 Dan Crepeau
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from PIL import Image

diverge_threshold = 200
diverge_pixel_normalize = 254 / (diverge_threshold - 1)

# function to determine Mandelbrot divergence.  Uses equation:
# Z = z^2 + c
# if magnitude is greater than 2.0, then it is assumed the function will
# diverge.  The return value is the number of iterations before divergence.
# Positive return values will always be integers in the range of 0 to 254.
def calc_diverge(c):
    counter = 0
    z = complex(0, 0)
    while counter < diverge_threshold:
        z = (z * z) + c
        if abs(z) > 2.0:
            return round(counter * diverge_pixel_normalize)
        counter = counter + 1
		
    return -1

# set pixels
image_size_x = 4000
image_size_y = 4000

img = Image.new('RGB', (image_size_x, image_size_y), "white")
pixels = img.load()

# define complex plane boundary for image_size
# these were determined by trial-and-error

# good overview of Mandelbrot set
x_range_min = -2
x_range_max = 1
y_range_min = -1.5
y_range_max = 1.5

# seahorse valley
#x_range_min = -.778
#x_range_max = -.738
#y_range_min = .08
#y_range_max = .12

# one seahorse
#x_range_min = -.751
#x_range_max = -.742
#y_range_min = .098
#y_range_max = .107

# one seahorse left side
#x_range_min = -.773
#x_range_max = -.764
#y_range_min = .1015
#y_range_max = .1105

# determine amount of range each pixel represents
x_delta = (x_range_max - x_range_min) / image_size_x
y_delta = (y_range_max - y_range_min) / image_size_y

# generate bitmap image, calculating one pixel at a time.
for i in range(img.size[0]):
    for j in range(img.size[1]):
        c_pixel = complex(x_range_min + i * x_delta, y_range_min + j * y_delta)
        diverge_num = calc_diverge(c_pixel)

        # reverse rows, since origin for pixels in PIL is upper-left
        if diverge_num == -1:
            pixels[i, image_size_y - j - 1] = (0, 0, 0)
        else:
            pixels[i, image_size_y - j - 1] = (255 - diverge_num, 255 - diverge_num, 255 - diverge_num)
            #pixels[i, image_size_y - j - 1] = (int(255 - diverge_num), 128, 128)
            #pixels[i, image_size_y - j - 1] = (255, 255, 255)

# display bitmap image
img.show()
