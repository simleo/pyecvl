# Copyright (c) 2019-2021 CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""\
Compute image moments and draw an ellipse on the image.
"""

import argparse
import os
import sys

import numpy as np
import pyecvl.ecvl as ecvl


def main(args):
    head, ext = os.path.splitext(os.path.basename(args.in_fn))
    img = ecvl.ImRead(args.in_fn)
    origin = img.copy()
    ecvl.ChangeColorSpace(img, img, ecvl.ColorType.GRAY)
    ecvl.Threshold(img, img, 25, 1)
    print("Calculating moments")
    moments = ecvl.Image.empty()
    ecvl.Moments(img, moments, 2)

    # use moments to calculate mass/area and center of mass of the image
    rm = np.array(moments, copy=False)
    print("Raw moments:")
    print(rm)
    M00 = rm[0, 0]
    M10 = rm[1, 0]
    M01 = rm[0, 1]
    # M11 = rm[1, 1]
    # M02 = rm[0, 2]
    # M20 = rm[2, 0]

    # centroid coordinates
    x = M10 / M00
    y = M01 / M00

    # central moments
    ecvl.CentralMoments(img, moments, [x, y])
    cm = np.array(moments, copy=False)
    print("Central moments:")
    print(cm)
    u00 = cm[0, 0]
    u11 = cm[1, 1]
    u20 = cm[2, 0]
    u02 = cm[0, 2]

    # note that central moments can also be computed through the raw moments
    # u00_bis = M00
    # u11_bis = M11 - x * M01
    # u20_bis = M20 - x * M10
    # u02_bis = M02 - y * M01

    # terms of the covariance matrix
    u_20 = u20 / u00  # or M20 / M00 - (x * x)
    u_02 = u02 / u00  # or M02 / M00 - (y * y)
    u_11 = u11 / u00  # or M11 / M00 - (x * y)

    # Eigenvalues (lambda1, lambda2) and orientation of the eigenvector
    lambda1 = (u_20 + u_02) / 2 + np.sqrt(
        4 * u_11 * u_11 + (u_20 - u_02) * (u_20 - u_02)
    ) / 2
    lambda2 = (u_20 + u_02) / 2 - np.sqrt(
        4 * u_11 * u_11 + (u_20 - u_02) * (u_20 - u_02)
    ) / 2
    theta = 0.5 * np.arctan2(2 * u_11, (u_20 - u_02))  # rad

    # Eigenvalues are proportional to the square length of the eigenvector
    # axes. So the half-axes of the ellipse generated by the eigenvectors are
    # given by d/sqrt(lambda1) and d/sqrt(lambda2) where d is the proportional
    # factor. Considering that the moment M00 is the area (the image on which
    # it is calculated is binary) of the image objects we can calculate d.

    d = np.sqrt(M00 * np.sqrt(lambda1 * lambda2) / np.pi)

    # half-axes (a and b) are then
    a = d / np.sqrt(lambda1)
    b = d / np.sqrt(lambda2)

    # We can now draw the ellipses with the same moments as the image objects
    ecvl.DrawEllipse(origin, [int(x), int(y)], [int(a), int(b)],
                     theta * 180 / np.pi, [0, 0, 255], 2)

    out_path = "%s_moments%s" % (head, ext)
    print("Writing %s" % out_path)
    ecvl.ImWrite(out_path, origin)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_fn", metavar="INPUT_PATH")
    main(parser.parse_args(sys.argv[1:]))
