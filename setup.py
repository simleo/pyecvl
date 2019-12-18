from distutils.core import setup, Extension

import pybind11


EXTRA_COMPILE_ARGS = ['-std=c++17', '-fvisibility=hidden', '-DECVL_WITH_DICOM']
OPENCV_LIBS = [
    "opencv_aruco",
    "opencv_bgsegm",
    "opencv_bioinspired",
    "opencv_calib3d",
    "opencv_ccalib",
    "opencv_core",
    "opencv_datasets",
    "opencv_dpm",
    "opencv_face",
    "opencv_features2d",
    "opencv_flann",
    "opencv_freetype",
    "opencv_fuzzy",
    "opencv_hdf",
    "opencv_highgui",
    "opencv_imgcodecs",
    "opencv_imgproc",
    "opencv_line_descriptor",
    "opencv_ml",
    "opencv_objdetect",
    "opencv_optflow",
    "opencv_phase_unwrapping",
    "opencv_photo",
    "opencv_plot",
    "opencv_reg",
    "opencv_rgbd",
    "opencv_saliency",
    "opencv_shape",
    "opencv_stereo",
    "opencv_stitching",
    "opencv_structured_light",
    "opencv_superres",
    "opencv_surface_matching",
    "opencv_text",
    "opencv_video",
    "opencv_videoio",
    "opencv_videostab",
    "opencv_viz",
    "opencv_ximgproc",
    "opencv_xobjdetect",
    "opencv_xphoto",
]
DICOM_LIBS = [
    "dcmdata",
    "dcmimage",
    "dcmimgle",
    "dcmjpeg",
    "i2d",
    "ijg8",
    "ijg12",
    "ijg16",
    "oflog",
    "ofstd",
]
ECVL_LIBS = ["ecvl_eddl", "dataset_parser", "ecvl_core"]
OTHER_LIBS = ["stdc++fs", "eddl", "openslide", "yaml-cpp"]
ALL_LIBS = ECVL_LIBS + OPENCV_LIBS + DICOM_LIBS + OTHER_LIBS


ext = Extension(
    "pyecvl._core",
    sources=["src/_core.cpp"],
    include_dirs=[
        "src",
        pybind11.get_include(),
        pybind11.get_include(user=True)
    ],
    libraries=ALL_LIBS,
    extra_compile_args=EXTRA_COMPILE_ARGS,
)


setup(
    name="pyecvl",
    packages=["pyecvl"],
    ext_modules=[ext]
)