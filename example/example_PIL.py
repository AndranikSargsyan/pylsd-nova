#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
from PIL import Image, ImageDraw
from pylsd import lsd

full_name = 'house.png'
folder, img_name = os.path.split(full_name)
img = Image.open(full_name)
img_gray = np.asarray(img.convert('L'))

segments = lsd(img_gray)

draw = ImageDraw.Draw(img)
for i in range(segments.shape[0]):
    pt1 = (int(segments[i, 0]), int(segments[i, 1]))
    pt2 = (int(segments[i, 2]), int(segments[i, 3]))
    width = segments[i, 4]
    draw.line((pt1, pt2), fill=(0, 0, 255), width=int(np.ceil(width / 2)))

img.save(os.path.join(folder, 'PIL_' + img_name.split('.')[0] + '.jpg'))
