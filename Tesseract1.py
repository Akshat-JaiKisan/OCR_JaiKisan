#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pytesseract
from pytesseract import Output
import argparse
import cv2
import matplotlib.pyplot as plt
import os 
os.chdir('D:\Semester 6\Jai Kisan')
# make a script for python images Akshat

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path")
ap.add_argument("-c", "--min-conf", type=int, default=0,help="min_confidence")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

for i in range(0, len(results["text"])):
    # extract the bounding box coordinates of the text region from
# the current result
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]
# extract the OCR text itself along with the confidence of the
# text localization
    text = results["text"][i]
    conf = int(results["conf"][i])
if conf > args["min_conf"]:
    print("Confidence: {}".format(conf))
    print("Text: {}".format(text))
    print("")
		# strip out non-ASCII text so we can draw the text on the image
		# using OpenCV, then draw a bounding box around the text along
		# with the text itself
    text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,1.2, (0, 0, 255), 3)
# display the confidence and text to our terminal

# show the output image
#cv2.imshow("Image", image)
plt.imsave("Image.jpg", image)


# In[12]:





# In[ ]:





# In[ ]:




