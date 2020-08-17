#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
from pylsd import lsd

full_name = 'car.jpg'
folder, img_name = os.path.split(full_name)
img = cv2.imread(full_name, cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

segments = lsd(img_gray, scale=0.5)

for i in range(segments.shape[0]):
    pt1 = (int(segments[i, 0]), int(segments[i, 1]))
    pt2 = (int(segments[i, 2]), int(segments[i, 3]))
    width = segments[i, 4]
    cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2)))

cv2.imwrite(os.path.join(folder, 'cv2_' + img_name.split('.')[0] + '.jpg'), img)
