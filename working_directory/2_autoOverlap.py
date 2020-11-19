import os.path
import time
import numpy as np
import math
import cv2 as cv
import matplotlib.pyplot as plt

fullList = [];

def forOne(standard, comparison):
    #if im1 = comparison, then you get precision, if im1 = standard, then you get recall
    def measure(im1, im2):
        mask = cv.inRange(im1, (0, 255, 0), (255, 255, 255))
        contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        total = 0
        number = 0
        if len(contours) > 20:
            return 0
        for c in contours:
            x,y,w,h = cv.boundingRect(c)
            for i in range(y, y+h):#+1):
                for j in range(x, x+w):#+1):
                    if np.all(im1[i][j] == (0, 255, 0)):
                        total += 1
                        if np.all(im2[i][j] == (0, 255, 0)):
                            number += 1
        print("number = "+str(number)+", total = "+str(total))
        if total == 0:
            value = 0
        else:
            value = float(number)/float(total)
        return(value)
        
    def calculateF1(standard, comparison):
        precision = measure(comparison, standard)
        recall = measure(standard, comparison)
        if precision == 0 or recall == 0:
            F1 = 0
        else:
            F1 = 2 / ((1/recall)+(1/precision))
        return F1
        
    def calculatePrecision(standard, comparison):
        return measure(comparison, standard)
    
    F1 = calculateF1(standard, comparison)     
    #precision = calculatePrecision(standard, comparison)
    if F1 < 0.70:
        return False
    return True


def forImage(image_name):
    header = image_name + "\n"
    txt_name = 'success_' + image_name + '.txt'
    f = open(txt_name, 'a')
    f.write(header)
    f.close()

    def oneLine(grid, radius, thresh, area):
        f = open(txt_name, 'a')
        content = str(grid)+" "+str(radius)+' '+str(thresh)+' '+str(area)+'\n'
        f.write(content)
        fullList.append(content)
        f.close()

    standard = cv.imread(image_name + "_standard.png")
    image_directory = image_name + "/"
    for grid_dir in os.listdir(image_directory):
        grid = grid_dir[grid_dir.find("grid")+5:]
        for thresh_dir in os.listdir(image_directory + grid_dir):
            if os.path.isdir(image_directory + grid_dir + "/" + thresh_dir):
                print(thresh_dir)
                radius = thresh_dir[thresh_dir.find("rad")+4:thresh_dir.find("rad")+5]
                thresh = thresh_dir[thresh_dir.find("thresh")+7:]
                new_directory = image_directory + grid_dir + "/" + thresh_dir
                for image in os.listdir(new_directory):
                    if "area" in image:
                        area = image[image.find("area")+5:-4]
                        imageLoc = image_directory + grid_dir + "/" + thresh_dir + '/' + image
                        print(imageLoc)
                        comparison = cv.imread(imageLoc)
                        if forOne(standard, comparison):
                            oneLine(grid, radius, thresh, area)


forImage("0024")
forImage("0025_0116")
forImage("0026")
forImage("0027")
forImage("0028")
#forImage("0029")

with open("fullList_file.txt", 'w') as f:
    for s in fullList:
        f.write(str(s))



