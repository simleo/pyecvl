import numpy as np


class Evaluator:
    def __init__(self):
        self.eps = 1e-06
        self.buf = []

    def ResetEval(self):
        self.buf = []

    def BinaryIoU(self, a, b, thresh=0.5):
        intersection = np.logical_and(a >= thresh, b >= thresh).sum()
        union = np.logical_or(a >= thresh, b >= thresh).sum()
        rval = (intersection + self.eps) / (union + self.eps)
        self.buf.append(rval)
        return rval

    def MIoU(self):
        if not self.buf:
            return 0
        return sum(self.buf) / len(self.buf)

    MeanMetric = MIoU


def ImageSqueeze(img):
    k = img.dims_.index(1)
    img.dims_ = [_ for i, _ in enumerate(img.dims_) if i != k]
    img.strides_ = [_ for i, _ in enumerate(img.strides_) if i != k]
    k = img.channels_.find("z")
    img.channels_ = "".join([_ for i, _ in enumerate(img.channels_) if i != k])
