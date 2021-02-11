# -*- coding: utf-8 -*-
"""Bird's Eye View.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18nrYKFo5eg20ty9XgyglwODzgU-wyMSl
"""

cd /content/drive/MyDrive/TextDetection

!pip install imutils

from imutils.object_detection import non_max_suppression # no idea how this works

import numpy as np
import argparse
import time
import cv2
import imutils
from google.colab.patches import cv2_imshow # change this to cv2.imshow if its not running on colab
import tensorflow as tf
from tensorflow.keras import layers

image = cv2.imread("Akshat_white.jpg")
orig = image.copy()
orig = cv2.cvtColor(orig , cv2.COLOR_BGR2GRAY)
cv2_imshow(orig)

# First step is to find contours, use canny edge detection 

image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
high_thresh, thresh_im = cv2.threshold(orig, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Before canny edge do thresholding then 
print(high_thresh , thresh_im)
image = cv2.Canny(image ,50, 136) 
cv2_imshow(image)

image_copy = image.copy()

edges = cv2.findContours(image_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
edges = imutils.grab_contours(edges)
edges = sorted(edges, key = cv2.contourArea, reverse = True)[0]

# loop over the contours and try finding the contour with the largest area . That will be our boundary
coords = []

for con in edges:
  perim = cv2.arcLength(con , True)
  poly = cv2.approxPolyDP(con , 0.0015*perim , True)

  if len(poly) == 4: # if the contour has 4 edges it might be our card
    coords.append(poly)
    break

print(coords)
# now the coords contain the coordinates of the corners of the contour
# Its length is 8 because of the number of coordinates
coords = np.array(coords) # make it an array so that reshaping becomes easy
coord = coords.reshape(4,2)

sum_of_points = coord.sum(axis = 1) # take sum of the coordinates 
# largest sum would be top right
# smallest sum would be bottom left

top_right_coord = coord[np.argmax(sum_of_points)]
bottom_left_coord = coord[np.argmin(sum_of_points)]

diff_of_points = coord.diff(axis = 1)
top_left_coord = coord[np.argmin(diff_of_points)]
bottom_right_coord = coord[np.argmax(diff_of_points)]


# create destination points for the warp perspective

# we begin by making the top left corner to be 0,0.. change of the 

# subtract this from all the coordinates to apply change of axes transformation 
sub = top_left_coord
ordered_coords = np.zeros(4 , 2)

ordered_coords[0] = top_left_corner
ordered_coords[1] = top_right_corner
ordered_coords[2] = bottom_right_corner
ordered_coords[3] = bottom_left_corner

W = np.sqrt((top_left_corner[0] - top_right_corner[0]) **2 + (top_left_corner[1] - top_right_corner[1]) **2)
H = np.sqrt((top_left_corner[0] - bottom_left_corner[0]) **2 + (top_left_corner[1] - bottom_left_corner[1]) **2)

destination_points = [[0 , 0 ] , top_right_coord-sub , bottom_right_coord-sub , bottom_left_coord-sub].toarray()

matrix = cv2.getPerspectiveTransform(ordered_coords, destination_points)
warp = cv2.warpPerspective(image_copy, matrix, (W , H))

# Just convert the warped image into a grayscale image. It will be easier for the model to extract images

bird_view_image_gray = cv.cvtColor(warp , cv2.color_BGR2GRAY)