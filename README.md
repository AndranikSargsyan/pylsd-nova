pylsd-nova
=============

### 1. Introduction

pylsd-nova is a python binding for [LSD - Line Segment Detector](http://www.ipol.im/pub/art/2012/gjmr-lsd/).

This is a fork from original [pylsd binding](https://github.com/primetang/pylsd/). This fork works for Python 3 and adds the ability to change lsd parameters from python call. 

### 2. Install

This package uses distutils, which is the default way of installing python modules. For installing by cloning the repository you can run the following commands:
```
git clone https://github.com/AndranikSargsyan/pylsd-nova.git
cd pylsd-nova
pip install .
```

Or install directly through `pip`:
```
pip install pylsd-nova
```

### 3. Usage

You can use the package by importing like  `from pylsd import lsd`, and calling `segments = lsd(img)` by optionally passing other lsd parameters mentioned below. `img` is a Grayscale Image (`H x W` numpy.ndarray), and the return value `segments` contains detected line segments.

`segments` is an `N x 5` numpy.ndarray. Each row represents a straight line. The 5-dimensional row format is:

```
[point1.x, point1.y, point2.x, point2.y, width]
```

These are the parameters of lsd, which can be changed through keyword arguments of lsd call:


* `scale (float)`: Scale the image by Gaussian filter to 'scale'.

* `sigma_scale (float)`: Sigma for Gaussian filter is computed as `sigma = sigma_scale / scale`.

* `quant (float)`: Bound to the quantization error on the gradient norm.

* `ang_th (float)`: Gradient angle tolerance in degrees.

* `eps (float)`: Detection threshold, `-log10(NFA)`.

* `density_th (float)`: Minimal density of region points in rectangle.

* `n_bins (int)`: Number of bins in pseudo-ordering of gradient modulus.

* `max_grad (float)`: Gradient modulus in the highest bin. The default value corresponds to the highest gradient modulus on images with gray levels in [0,255].


You can use it just like the following code ([here is the link to examples](https://github.com/AndranikSargsyan/pylsd-nova/tree/master/example)):

* by using cv2 module

```python
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
```

* by using PIL(Image) module

```python
import numpy as np
import os
from PIL import Image, ImageDraw
from pylsd import lsd

full_name = 'house.png'
folder, img_name = os.path.split(full_name)
img = Image.open(full_name)
img_gray = np.asarray(img.convert('L'))

segments = lsd(img_gray, scale=0.5)

draw = ImageDraw.Draw(img)
for i in range(segments.shape[0]):
    pt1 = (int(segments[i, 0]), int(segments[i, 1]))
    pt2 = (int(segments[i, 2]), int(segments[i, 3]))
    width = segments[i, 4]
    draw.line((pt1, pt2), fill=(0, 0, 255), width=int(np.ceil(width / 2)))

img.save(os.path.join(folder, 'PIL_' + img_name.split('.')[0] + '.jpg'))
```

The following is the result:

* car.jpg by using cv2 module

![](https://github.com/AndranikSargsyan/pylsd-nova/blob/master/example/car.jpg)

![](https://github.com/AndranikSargsyan/pylsd-nova/blob/master/example/cv2_car.jpg)

* house.png by using PIL(Image) module

![](https://github.com/AndranikSargsyan/pylsd-nova/blob/master/example/house.png)

![](https://github.com/AndranikSargsyan/pylsd-nova/blob/master/example/PIL_house.jpg)
