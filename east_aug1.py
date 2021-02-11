# -*- coding: utf-8 -*-
"""EAST_AUG1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1inDrJ5OozXvQOVzW8gBz4QTqRfbQ2vPN
"""

# import the necessary packages

from imutils.object_detection import non_max_suppression # no idea how this works

import numpy as np
import argparse
import time
import cv2
from google.colab.patches import cv2_imshow # change this to cv2.imshow if its not running on colab
import tensorflow as tf
from tensorflow.keras import layers
#tf.keras.preprocessing.image.random_rotation
#FLAGS = tf.app.flags.FLAGS

# Define necessary FLAGS


padding_x = 5
padding_y = 5

data_augmentation = tf.keras.Sequential([layers.experimental.preprocessing.RandomRotation(0.02)])

image = cv2.imread('Text_Augmented4.jpg')

orig = image.copy()
(H, W) = image.shape[:2]
print(H,W)
(newW, newH) = (320, 320) # multiples of 320

rW = W / float(newW)
rH = H / float(newH)

  # resize the image and grab the new image dimensions
image = cv2.resize(image, (newW, newH))
(H, W) = image.shape[:2] 
layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"] # last two layers of the pretrained model

print("East Text Detector is starting ...")
model = cv2.dnn.readNet("frozen_east_text_detection.pb") # read the pretrained model 
  # construct a blob from the image and then perform a forward pass of
# the model to obtain the two output layer sets


blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),(123.68, 116.78, 103.94), swapRB=True, crop=False) # the tuple is the mean derived from tensorflow hub 
  #scaling of the images is not being done here...

start = time.time()
model.setInput(blob)
(scores, geometry) = model.forward(layerNames) # from tensorflow website

print("Shape of the score volume is ...") # (1,1,80,80)
print(scores.shape)
print('Geometry that we get is ....')
print(geometry.shape) # (1,5,80,80) (number of images , tensor associated , row , cols)
(numRows, numCols) = scores.shape[2:4]

rects = []
confidences = []
for y in range(0, numRows):

    
  scoresData = scores[0, 0, y]
  print("scoresData shape is..")
  print(scoresData.shape) # (80,) for a particular y the xs
  xData0 = geometry[0, 0, y]
  xData1 = geometry[0, 1, y]
  xData2 = geometry[0, 2, y]
  xData3 = geometry[0, 3, y]
  anglesData = geometry[0, 4, y]

  for x in range(0, numCols):
        # if our score does not have sufficient probability, ignore it
      if scoresData[x] < 0.5:
          continue
            
      (offsetX, offsetY) = (x * 4.0, y * 4.0) # according to the paper
      angle = anglesData[x]
      cos = np.cos(angle)
      sin = np.sin(angle)


      h = xData0[x] + xData2[x]
      w = xData1[x] + xData3[x]


      endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
      endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
      startX = int(endX - w)
      startY = int(endY - h)

      rects.append((startX, startY, endX, endY))
      confidences.append(scoresData[x])
        
# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
boxes = non_max_suppression(np.array(rects), probs=confidences)

# loop over the bounding boxes
i = 0
for (startX, startY, endX, endY) in boxes:
  startX = int(startX * rW)
  startY = int(startY * rH)
  endX = int(endX * rW)
  endY = int(endY * rH)

  cv2.imwrite("Text_{}.jpg".format(i+1) , orig[startY-padding_y:endY + padding_y , startX-padding_x:endX+padding_y])
  cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    
  i = i+1
  end = time.time()
#print('Time Taken for data number{} is ..'.format(pan))
print(end-start)
cv2_imshow(orig)
image = tf.expand_dims(image, 0)
image = data_augmentation(image)[0]
image = np.array(image) # number of times data augmentation shall be applied on the given image