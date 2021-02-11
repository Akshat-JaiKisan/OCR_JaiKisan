# -*- coding: utf-8 -*-
"""EAST_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xikBcgEfVxdFy1o-p1FfurH0C_OYZIlR
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
print(H,W) # (2000,4000)
image = cv2.resize(image , (3200 , 3200))
layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"] # last two layers of the pretrained model

print("East Text Detector is starting ...")
model = cv2.dnn.readNet("frozen_east_text_detection.pb") # read the pretrained model 


blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),(123.68, 116.78, 103.94), swapRB=True, crop=False) # the tuple is the mean derived from tensorflow hub 
  #scaling of the images is not being done here...
  # The mean value is beyond me

start = time.time()
model.setInput(blob)
(scores, geometry) = model.forward(layerNames) # from tensorflow website

print("Shape of the score volume is ...") # (1,1,80,80) (number of images , value associated , row , cols)
print(scores.shape)
print('Geometry that we get is ....')
print(geometry.shape) # (1,5,80,80) (number of images , tensor associated , row , cols)
(numR, numC) = scores.shape[2:4]

coords = []
alphas = []
for y in range(0, numR): # will go up vertically na so it is the y coordinate of your rectangles....

    
  scoresData = scores[0, 0, y]
  print("scoresData shape is..")
  print(scoresData.shape) # (80,) for a particular y the xs
  x0 = geometry[0, 0, y]
  x1 = geometry[0, 1, y]
  x2 = geometry[0, 2, y]
  x3 = geometry[0, 3, y]
  theta = geometry[0, 4, y]

  for x in range(0, numC):
        # if our score does not have sufficient probability, ignore it
      if scoresData[x] < 0.5:
          continue
            
      newX , newY = (x * 4.0, y * 4.0) # according to the paper
      angle = theta[x]
      cos = np.cos(angle)
      sin = np.sin(angle)

      h = x0[x] + x2[x]
      w = x1[x] + x3[x]

      endX = int(newX + (cos * x1[x]) + (sin * x2[x])) # from tensorflow
      endY = int(newY - (sin * x1[x]) + (cos * x2[x])) # from tensorflow
      startX = int(endX - w)
      startY = int(endY - h)

      coords.append((startX, startY, endX, endY))
      alphas.append(scoresData[x])
        
# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
boxes = non_max_suppression(np.array(coords), probs=alphas)

# loop over the bounding boxes
i = 0
for (startX, startY, endX, endY) in boxes:

  cv2.imwrite("Text_{}.jpg".format(i+1) , orig[startY-padding_y:endY + padding_y , startX-padding_x:endX+padding_y]) # padding gives some leeway 
  cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
  i = i+1
  end = time.time()
#print('Time Taken for data number{} is ..'.format(pan))
print(end-start)
cv2_imshow(orig)