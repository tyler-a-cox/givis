import numpy as np
import matplotlib.pyplot as plt
import glob
from PIL import Image
import os
from multiprocessing import Pool

def main(f):
    """
    """
    img = Image.open(f)
    arr = np.array(img)
    masked_arr = np.ma.masked_array(arr, mask=arr[:, :, :] == [140, 140, 140, 0], fill_value=[0, 0, 0, 255])
    img = Image.fromarray(masked_arr.filled())
    img.save(f)

if __name__ == '__main__':
    fs = glob.glob('render/*png')
    fs.sort()
    pool = Pool(processes=4)
    _ = pool.map(main, fs)
