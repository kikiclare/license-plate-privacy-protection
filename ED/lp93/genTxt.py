from PIL import Image
import os
import argparse
import matplotlib.pyplot as plt

def getAllPath(dirpath, *suffix):
    PathArray = []
    for r, ds, fs in os.walk(dirpath):
        for fn in fs:
            if os.path.splitext(fn)[1] in suffix:
                fname = os.path.join(r, fn)
                PathArray.append(fname)
    return PathArray


if __name__ == '__main__':
    
    for i in  getAllPath('./images/k1', '.jpg', '.JPG'):
        with open('lp93.txt', 'a') as f:
            f.write(i + '\n')


    