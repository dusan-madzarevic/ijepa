OPENSLIDE_PATH = r'E:\openslide-bin-4.0.0.3-windows-x64\openslide-bin-4.0.0.3-windows-x64\bin'

import os
import numpy as np
with os.add_dll_directory(OPENSLIDE_PATH):
    import openslide
import os.path as osp
from pathlib import Path
import matplotlib.pyplot as plt
from skimage import measure

BASE_TRUTH_DIR = Path(r'D:\camelyon\masks')

slide_path = r'D:\camelyon\images\tumor_031.tif'
truth_path = osp.join(BASE_TRUTH_DIR, 'tumor_031_mask.tif')

# Open the slide and truth images
slide = openslide.open_slide(slide_path)
truth = openslide.open_slide(truth_path)

# Read region of the slide and mask
rgb_image = slide.read_region((0, 0), 4, slide.level_dimensions[4])
rgb_mask = truth.read_region((0, 0), 4, slide.level_dimensions[4])

# Convert the mask to grayscale
grey = np.array(rgb_mask.convert('L'))
rgb_imagenew = np.array(rgb_image)

# Find contours using skimage
contours = measure.find_contours(grey, 0.5)

# Display the original image with contours using matplotlib
fig, ax = plt.subplots()
ax.imshow(rgb_imagenew)

for contour in contours:
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2, color='red')

ax.set_title('Tumor image with mask overlayed')
plt.axis('off')
plt.show()