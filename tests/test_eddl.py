# Copyright (c) 2020 CRS4
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

import pytest

import pyecvl._core.ecvl as ecvl_core
import pyecvl.ecvl as ecvl_py
tensor = pytest.importorskip("pyeddl.tensor")


@pytest.mark.parametrize("ecvl", [ecvl_core, ecvl_py])
def test_ImageToTensor(ecvl):
    dims = [20, 30, 3]
    img = ecvl.Image(dims, ecvl.DataType.uint8, "xyc", ecvl.ColorType.BGR)
    t = ecvl.ImageToTensor(img)
    t.max()
    assert t.shape == [dims[2], dims[1], dims[0]]


@pytest.mark.parametrize("ecvl", [ecvl_core, ecvl_py])
def test_TensorToImage(ecvl):
    # 3D
    shape = [3, 30, 20]
    t = tensor.Tensor(shape)
    img = ecvl.TensorToImage(t)
    assert img.dims_ == [shape[2], shape[1], shape[0]]
    # 4D
    shape = [5, 3, 30, 20]
    t = tensor.Tensor(shape)
    img = ecvl.TensorToImage(t)
    assert img.dims_ == [shape[3], shape[2], shape[0] * shape[1]]


@pytest.mark.parametrize("ecvl", [ecvl_core, ecvl_py])
def test_TensorToView(ecvl):
    # 3D
    shape = [3, 30, 20]
    t = tensor.Tensor(shape)
    view = ecvl.TensorToView(t)
    assert view.dims_ == [shape[2], shape[1], shape[0]]
    # 4D
    shape = [5, 3, 30, 20]
    t = tensor.Tensor(shape)
    view = ecvl.TensorToView(t)
    assert view.dims_ == [shape[3], shape[2], shape[0] * shape[1]]
