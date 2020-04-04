#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
import os
import sys
import numpy as np
from tempfile import NamedTemporaryFile

from .bindings.lsd_ctypes import lsdlib


def lsd(
    img,
    scale=0.8,
    sigma_scale=0.6,
    ang_th=22.5,
    quant=2.0,
    eps=0.0,
    density_th=0.7,
    n_bins=1024,
    max_grad=255.0
):
    """Detects line segments in the provided image.

    Args:
        img (numpy.ndarray): Grayscale image.

        scale (float): Scale the image by Gaussian filter to 'scale'.

        sigma_scale (float):Sigma for Gaussian filter is computed as sigma = sigma_scale/scale.

        quant (float): Bound to the quantization error on the gradient norm.

        ang_th (float): Gradient angle tolerance in degrees.

        eps (float): Detection threshold, -log10(NFA).

        density_th (float): Minimal density of region points in rectangle.

        n_bins (int): Number of bins in pseudo-ordering of gradient modulus.

        max_grad (float): Gradient modulus in the highest bin. The default value corresponds to
            the highest gradient modulus on images with gray levels in [0,255].

    Returns:
        (2D numpy.ndarray): Detected line segments in format:
            [[point1.x, point1.y, point2.x, point2.y, width]]
    """
    rows, cols = img.shape
    img = img.reshape(1, rows * cols).tolist()[0]

    lens = len(img)
    img = (ctypes.c_double * lens)(*img)

    with NamedTemporaryFile(prefix='pylsd-', suffix='.ntl.txt', delete=False) as fp:
        fname = fp.name
        fname_bytes = bytes(fp.name) if sys.version_info < (3, 0) else bytes(fp.name, 'utf8')

    lsdlib.lsdGet(img, ctypes.c_int(rows), ctypes.c_int(cols), fname_bytes,
                 ctypes.c_double(scale), ctypes.c_double(sigma_scale),
                 ctypes.c_double(ang_th), ctypes.c_double(quant), ctypes.c_double(eps),
                 ctypes.c_double(density_th), ctypes.c_int(n_bins), ctypes.c_double(max_grad))

    with open(fname, 'r') as fp:
        output = fp.read()
        cnt = output.strip().split(' ')
        count = int(cnt[0])
        dim = int(cnt[1])
        segments = np.array([float(each) for each in cnt[2:]])
        segments = segments.reshape(count, dim)

    os.remove(fname)
    return segments

