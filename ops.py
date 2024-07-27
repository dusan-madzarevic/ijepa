# The path can also be read from a config file, etc.
OPENSLIDE_PATH = r'E:\openslide-bin-4.0.0.3-windows-x64\openslide-bin-4.0.0.3-windows-x64\bin'

import os
import matplotlib.pyplot as plt

with os.add_dll_directory(OPENSLIDE_PATH):
    import openslide

if __name__ == '__main__':

    slide = openslide.OpenSlide(r'D:\camelyon\masks\tumor_001_mask.tif')

    region = (0, 0)
    level = 0
    size = (14000, 15000)
    region = slide.read_region(region, level, size)
    plt.figure(figsize=(200, 200))
    plt.imshow(slide.get_thumbnail((14000, 15000)))
    plt.show()
    thumbnail = slide.get_thumbnail((slide.dimensions[0] / 256, slide.dimensions[1] / 256))