// Copyright (c) 2019-2021 CRS4
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#pragma once

#include <pybind11/pybind11.h>
#include <ecvl/dataset_generator.h>

template <typename type_, typename... options>
void generatesegmentationdataset_addons(pybind11::class_<type_, options...> &cl) {
    cl.def(pybind11::init([](const std::string& dataset_root_directory) {
      return new ecvl::GenerateSegmentationDataset(dataset_root_directory);
    }));
    cl.def(pybind11::init([](const std::string& dataset_root_directory, std::string suffix) {
      return new ecvl::GenerateSegmentationDataset(dataset_root_directory, suffix);
    }));
    cl.def(pybind11::init([](const std::string& dataset_root_directory, std::string suffix, std::string gt_name) {
      return new ecvl::GenerateSegmentationDataset(dataset_root_directory, suffix, gt_name);
    }));
}
