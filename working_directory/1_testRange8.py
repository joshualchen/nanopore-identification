import os.path
import time
import sys
from PIL import Image
import numpy as np
import cv2 as cv
sys.path.insert(0, '/home/joshua/Desktop/AtomicDefects/dm3reader/dm3_lib')
import _dm3_lib as dm3

images = ["0024", "0025_0116", "0026", "0027", "0028"]
grid_range = range(18, 22)
radius_range = range(3, 10)
threshold_range = range(20, 121, 4)
area_range = range(0, 50, 2)

t0 = time.time()

number_runs = len(images)*len(grid_range)*len(radius_range)*len(threshold_range)*len(area_range)

runNumber = 1

def incr():
    global runNumber
    runNumber += 1

def oneRun(im_name, img, im_cl, grid_standard, rad_standard, thresh_standard, mag_ratio, bright_ratio):
    def avg_thresh(name, image, rad_standard, thresh_standard, area_standard, mag_ratio, bright_ratio):
        image_new = image.copy()
        height, width = image.shape
        radius_real = int(round(rad_standard*mag_ratio))
        thresh_real = int(round(thresh_standard*bright_ratio))
        image_new = cv.blur(image_new,(radius_real,radius_real))
        ret, image_new = cv.threshold(image_new,thresh_real,255,cv.THRESH_BINARY_INV)
        return image_new

    rad_real = int(round(rad_standard * mag_ratio))
    thresh_real = int(round(thresh_standard * bright_ratio))

    im_dir = im_name + "/"
    cl_grid_dir = im_name+"_grid:" + str(grid_standard)+"/"  # ADDED 10/2
    avg_thresh_dir = im_name+"_rad:" + \
        str(rad_standard)+"_thresh:"+str(thresh_standard)+"/"
    avg_thresh_name = im_name+"_rad:" + \
        str(rad_standard)+"_thresh:"+str(thresh_standard)+".png"
    dir_file = im_dir + cl_grid_dir + avg_thresh_dir + avg_thresh_name

    for area_standard in area_range:
        area_real = int(round(area_standard*mag_ratio))

        if os.path.isfile(dir_file):
            im_avg = cv.imread(dir_file, 0)
        else:
            im_avg = avg_thresh(im_name, im_cl, rad_standard,
                                thresh_standard, area_standard, mag_ratio, bright_ratio)
            print(str(runNumber) + '/' + str(number_runs) + ' | File ' + im_name + '-- grid: '+str(grid_standard) +
                  ', radius: ' + str(rad_standard) + ', thresh: ' + str(thresh_standard) + ', area: ' + str(area_standard))
            avg_thresh_save = Image.fromarray(im_avg)
            if not os.path.exists(im_dir):
                os.makedirs(im_dir)
            if not os.path.exists(im_dir + cl_grid_dir):
                os.makedirs(im_dir + cl_grid_dir)
            if not os.path.exists(im_dir + cl_grid_dir + avg_thresh_dir):
                os.makedirs(im_dir + cl_grid_dir + avg_thresh_dir)
            avg_thresh_save.save(dir_file)

        mask_min = int(round(150*bright_ratio))
        mask = cv.inRange(im_avg, mask_min, 255)

        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        im = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

        def squarish(contour):
            rect = cv.minAreaRect(contour)
            width = rect[1][0]
            height = rect[1][1]
            if height < 3 * width and width < 3 * height:
                return True
            return False

        for c in contours:
            if cv.contourArea(c) > area_real and cv.contourArea(c) < 100000 and squarish(c):
                cv.drawContours(im, [c], -1, (0, 255, 0), -1)

        im_final = Image.fromarray(im)
        im_final_name = im_name+"_grid:" + str(grid_standard) + "_rad:" + str(
            rad_standard)+"_thresh:"+str(thresh_standard) + "_area:"+str(area_standard)+".png"
        im_final.save(im_dir + cl_grid_dir + avg_thresh_dir + im_final_name)
        incr()


def forOne(imName):
    dm3f = dm3.DM3(imName + ".dm3")

    img_data = dm3f.imagedata
    im_save = img_data.copy()
    im_save = (im_save - np.min(im_save)) / float(np.max(im_save) - np.min(im_save))
    img_png = Image.fromarray(np.uint8(np.round(im_save * 255)))
    png_name = imName + ".png"
    img_png.save(png_name)

    img = cv.imread(png_name, 0)

    # setting up parameters
    mag = dm3f.info['mag']
    mag_ratio = float(mag) / 10000000.0
    bright = np.median(img)
    bright_ratio = float(bright) / 88.0

    for grid in grid_range:  
        clahe = cv.createCLAHE(clipLimit=40, tileGridSize=(int(round(grid*mag_ratio)), int(round(grid*mag_ratio))))
        cl = clahe.apply(img)

        for radius in radius_range:
            for threshold in threshold_range:
                oneRun(imName, img, cl, grid, radius, threshold, mag_ratio, bright_ratio)

for im_name in images:
    forOne(im_name)

t1 = time.time()
total_sec = t1 - t0

print("Total time elapsed: " + str(total_sec) + " seconds")
