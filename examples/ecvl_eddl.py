"""\
ECVL-EDDL interaction.
"""

import argparse
import os
import sys

import pyecvl._core.ecvl as ecvl
import pyeddl._core.eddlT as eddlT


def main(args):
    # FIXME: why isn't std::invalid_argument being converted to a Python error?
    if not os.path.isfile(args.in_img):
        raise RuntimeError("%s does not exist or is not a file" % args.in_img)
    img = ecvl.Image()
    ecvl.ImRead(args.in_img, img)
    print("Executing ImageToTensor")
    t = ecvl.ImageToTensor(img)
    eddlT.div_(t, 128)
    print("Executing TensorToImage")
    img = ecvl.TensorToImage(t)
    print("Executing TensorToView")
    ecvl.TensorToView(t)

    batch_size = 64
    print("Creating a DLDataset")
    d = ecvl.DLDataset(args.in_ds, batch_size, "training", ecvl.ColorType.GRAY)
    size = [28, 28]
    print("Create x_train and y_train")
    x_train = eddlT.create([batch_size, d.n_channels_, size[0], size[1]])
    y_train = eddlT.create([batch_size, len(d.classes_)])

    # Load a batch of d.batch_size_ images into x_train and corresponding
    # labels in y_train. Images are resized to the dimensions specified in size
    print("Executing LoadBatch")
    ecvl.LoadBatch(d, size, x_train, y_train)

    # Load test images in x_test and corresponding labels in y_test
    print("Executing TestToTensor")
    x_test, y_test = ecvl.TestToTensor(d, size, ecvl.ColorType.GRAY)
    print("x_test info:")
    eddlT.info(x_test)
    print("y_test info:")
    eddlT.info(y_test)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_img", metavar="INPUT_IMAGE")
    parser.add_argument("in_ds", metavar="INPUT_DATASET")
    main(parser.parse_args(sys.argv[1:]))