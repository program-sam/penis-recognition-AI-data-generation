import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
from PIL import Image
import random
import os

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

def createImage(pp, tile, destination):
    pp = np.array(Image.open(pp), dtype=np.float)
    map = np.array(Image.open(tile), dtype=np.float)
    alpha = (pp[:,:,3] / 255) * (map[:,:,3] / 255)
    alpha = np.rot90(alpha, int(random.random() * 5))
    if random.random() > 0.5: alpha = 1 - alpha
    # random color pp
    r = 0.5 + random.random() * alpha * 1.3
    g = 0.5 + random.random() * alpha * 1.3
    b = 0.5 + random.random() * alpha * 1.3
    a = np.zeros((256, 256), dtype=np.float) + 1

    overlay = np.stack([r, g, b, a], 2)

    # # Generate Gaussian noise
    # gauss = np.random.normal(0,0.2,overlay.shape)
    # gauss = gauss/5 + 1
    # gauss[:,:,3] = 1
    
    # # Add the Gaussian noise to the image
    # overlay = overlay * gauss

    new = np.zeros((256, 256, 4), dtype=np.float)
    new = (map * overlay)
    if np.average(new) < 90: return
    new *= 255.0/new.max()
    new = np.array(np.round(new),dtype=np.uint8)

    out=Image.fromarray(new, mode="RGBA")
    out.save(destination)
   
# ppfiles = getListOfFiles('png/pp')
# print('there are ' + str(len(ppfiles)) + ' ppfiles')
# noppfiles = getListOfFiles('png/no pp')
# print('there are ' + str(len(noppfiles)) + ' noppfiles')
# tiles = getListOfFiles('tiles')
# print('there are ' + str(len(tiles)) + ' tiles')

import pickle

# pickle_out = open('ppfiles.pickle', 'wb')
# pickle.dump(ppfiles, pickle_out)
# pickle_out.close

# pickle_out = open('noppfiles.pickle', 'wb')
# pickle.dump(noppfiles, pickle_out)
# pickle_out.close()

# pickle_out = open('tiles.pickle', 'wb')
# pickle.dump(tiles, pickle_out)
# pickle_out.close()

ppfiles = pickle.load(open('ppfiles.pickle', 'rb'))
noppfiles = pickle.load(open('noppfiles.pickle', 'rb'))
tiles = pickle.load(open('tiles.pickle', 'rb'))


def createPP(array, tiles):
    n = 0
    for pp in array:
        for i in range(4):
            n += 1
            if n % 100 == 0: print('Starting the ' + str(n) + 'th pp image')
            createImage(pp, random.choice(tiles), 'training/pp/' + str(n) + '.png')

def createNoPP(array, tiles):
    n = 0
    for nopp in array:
        for i in range(4):
            n += 1
            if n % 100 == 0: print('Starting the ' + str(n) + 'th no pp image')
            createImage(nopp, random.choice(tiles), 'training/no pp/' + str(n) + '.png')

if __name__ == '__main__':
    p1 = Process(target=createPP, args=(ppfiles, tiles))
    p2 = Process(target=createNoPP, args=(noppfiles, tiles))
    p1.start()
    p2.start()
    p1.join()
    p2.join()