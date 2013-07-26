'''The MNIST dataset 
'''
from decaf.layers.data import ndarraydata
import numpy as np
import os

class MNISTDataLayer(ndarraydata.NdarrayDataLayer):
    NUM_TRAIN = 60000
    NUM_TEST = 10000
    IMAGE_DIM = (28,28)
    
    def __init__(self, **kwargs):
        """Initialize the mnist dataset."""
        is_training = kwargs.get('is_training', True)
        rootfolder = kwargs['rootfolder']
        dtype = kwargs.get('dtype', np.float64)
        self._load_mnist(rootfolder, is_training, dtype)
        ndarraydata.NdarrayDataLayer.__init__(
            self, sources=[self._data, self._label], **kwargs)

    def _load_mnist(self, rootfolder, is_training, dtype):
        if is_training:
            self._data = self._read_byte_data(
                    os.path.join(rootfolder,'train-images-idx3-ubyte'), 
                    16, (MNISTDataLayer.NUM_TRAIN,) + \
                            MNISTDataLayer.IMAGE_DIM).astype(dtype)
            self._label = self._read_byte_data(
                    os.path.join(rootfolder,'train-labels-idx1-ubyte'),
                    8, [MNISTDataLayer.NUM_TRAIN]).astype(np.int)
        else:
            self._data = self._read_byte_data(
                    os.path.join(rootfolder,'t10k-images-idx3-ubyte'),
                    16, (MNISTDataLayer.NUM_TEST,) + \
                            MNISTDataLayer.IMAGE_DIM).astype(dtype)
            self._label = self._read_byte_data(
                    os.path.join(rootfolder,'t10k-labels-idx1-ubyte'),
                    8, [MNISTDataLayer.NUM_TEST]).astype(np.int)

    def _read_byte_data(self, filename, skipbytes, shape):
        fid = open(filename, 'rb')
        fid.seek(skipbytes)
        nbytes = np.prod(shape)
        rawdata = fid.read(nbytes)
        fid.close()
        #convert rawdata to data
        data = np.zeros(nbytes)
        for i in range(nbytes):
            data[i] = ord(rawdata[i])
        data.resize(shape)
        return data