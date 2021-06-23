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

import io
import os
import pytest

import pyecvl._core.ecvl as ecvl_core
import pyecvl.ecvl as ecvl_py


DATASET = """\
name: Foo
description: FooDesc
classes:
- '0'
- '1'
- '2'
images:
- location: foo_0.png
  label: 2
- location: foo_1.png
  label: 0
- location: foo_2.png
  label: 1
split:
  training:
  - 0
  - 1
  test:
  - 2
"""


@pytest.mark.parametrize("ecvl", [ecvl_core, ecvl_py])
def test_load(ecvl, tmp_path):
    fn = str(tmp_path / "foo.yml")
    with io.open(fn, "wt") as f:
        f.write(DATASET)
    d = ecvl.Dataset(fn)
    assert d.name_ == "Foo"
    assert d.description_ == "FooDesc"
    assert d.classes_ == ["0", "1", "2"]
    assert not d.features_
    assert len(d.samples_) == 3
    with pytest.raises(RuntimeError):
        d.samples_[0].LoadImage()
    locations = [os.path.basename(_.location_[0]) for _ in d.samples_]
    assert locations == ["foo_0.png", "foo_1.png", "foo_2.png"]
    assert d.task_ == ecvl.Task.classification
    split_map = {_.split_name_: _ for _ in d.split_}
    assert set(split_map) == {"training", "test"}
    assert split_map["training"].split_type_ == ecvl.SplitType.training
    assert set(split_map["training"].samples_indices_) == {0, 1}
    assert set(d.GetSplit("training")) == {0, 1}
    assert split_map["test"].split_type_ == ecvl.SplitType.test
    assert set(split_map["test"].samples_indices_) == {2}
    assert set(d.GetSplit("test")) == {2}
    for t in "training", "test":
        d.SetSplit(t)
        assert d.GetSplit(-1) == split_map[t].samples_indices_
    for i, s in enumerate(d.split_):
        d.SetSplit(i)
        assert d.GetSplit(-1) == d.split_[i].samples_indices_
        assert d.GetSplit() == d.split_[i].samples_indices_


@pytest.mark.parametrize("ecvl", [ecvl_core, ecvl_py])
def test_load_nonexistent(ecvl):
    with pytest.raises(RuntimeError):
        ecvl.Dataset("/not/existing.yml")
