"""\
MNIST batch training.
"""

import argparse
import random
import sys

import pyecvl._core.ecvl as ecvl
import pyeddl._core.eddl as eddl
import pyeddl._core.eddlT as eddlT


TRMODE = 1


def LeNet(in_layer, num_classes):
    x = in_layer
    x = eddl.MaxPool(
        eddl.Activation(eddl.Conv(x, 20, [5, 5]), "relu"), [2, 2], [2, 2]
    )
    x = eddl.MaxPool(
        eddl.Activation(eddl.Conv(x, 50, [5, 5]), "relu"), [2, 2], [2, 2]
    )
    x = eddl.Reshape(x, [-1])
    x = eddl.Activation(eddl.Dense(x, 500), "relu")
    x = eddl.Activation(eddl.Dense(x, num_classes), "softmax")
    return x


def main(args):
    num_classes = 10
    size = [28, 28]  # size of images
    ctype = ecvl.ColorType.GRAY

    in_ = eddl.Input([1, size[0], size[1]])
    out = LeNet(in_, num_classes)
    net = eddl.Model([in_], [out])
    eddl.build(
        net,
        eddl.sgd(0.001, 0.9),
        ["soft_cross_entropy"],
        ["categorical_accuracy"],
        eddl.CS_GPU([1]) if args.gpu else eddl.CS_CPU(4)
    )
    print(eddl.summary(net))

    d = ecvl.DLDataset(args.in_ds, args.batch_size, "training", ctype)
    x_train = eddlT.create([args.batch_size, d.n_channels_, size[0], size[1]])
    y_train = eddlT.create([args.batch_size, len(d.classes_)])
    eddl.resize_model(net, args.batch_size)
    eddl.set_mode(net, TRMODE)
    total_loss = [0]
    total_metric = [0]
    num_samples = len(d.GetSplit())
    num_batches = num_samples // args.batch_size
    indices = list(range(args.batch_size))

    for i in range(args.epochs):
        total_loss[0] = 0.0
        total_metric[0] = 0.0
        s = d.GetSplit()
        random.shuffle(s)
        d.split_.training_ = s
        d.current_batch_ = 0
        for j in range(num_batches):
            print("Epoch %d/%d (batch %d/%d)" %
                  (i + 1, args.epochs, j + 1, num_batches))
            ecvl.LoadBatch(d, size, x_train, y_train)
            x_train.div_(255.0)
            tx, ty = [x_train], [y_train]
            eddl.train_batch(net, tx, ty, indices)
            p = 0
            for k in range(len(ty)):
                total_loss[k] += net.fiterr[p]
                total_metric[k] += net.fiterr[p + 1]
                print("%s(%s=%.3f, %s=%.3f)" % (
                    net.lout[k].name,
                    "soft_cross_entropy",  # net.losses[k].name
                    total_loss[k] / (args.batch_size * (j + 1)),
                    "categorical accuracy",  # net.metrics[k].name
                    total_metric[k] / (args.batch_size * (j + 1))
                ))
                net.fiterr[p] = net.fiterr[p + 1] = 0.0
                p += 2
            d.current_batch_ += 1

    eddl.save(net, "mnist_checkpoint.bin")
    del(x_train)
    del(y_train)

    d.SetSplit("test")
    x_test, y_test = ecvl.TestToTensor(d, size, ctype)
    x_test.div_(255.0)
    eddl.evaluate(net, [x_test], [y_test])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_ds", metavar="INPUT_DATASET")
    parser.add_argument("--epochs", type=int, metavar="INT", default=5)
    parser.add_argument("--batch-size", type=int, metavar="INT", default=64)
    parser.add_argument("--gpu", action="store_true")
    main(parser.parse_args(sys.argv[1:]))