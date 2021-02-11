#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pytesseract
from pytesseract import Output
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import re
import os 
os.chdir('D:\Semester 6\Jai Kisan')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r"D:\Semester 6\Jai Kisan\Release-21.01.0\poppler-21.01.0\Library\bin\pdfimages.exe"
# laplacian
# FFT


# In[28]:


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
def thresholding(image):
    return cv2.threshold(image, 90, 215, cv2.THRESH_BINARY)[1] # pehle 60 tha


# In[5]:


pip install pdf2image


# In[4]:


date_pattern = '^(19|20)\d\d/(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])'
Pan_number_pattern = '^([A-Z][A-Z][A-Z][A-Z][A-Z][1-9][1-9][1-9][1-9][A-Z])'


# In[9]:


from pdf2image import convert_from_path
images = convert_from_path("PAN Card Printed.pdf" , poppler_path = r"D:\Semester 6\Jai Kisan\Release-21.01.0\poppler-21.01.0\Library\bin")
for i in range(len(images)):
    # Save pages as images in the pdf
    images[i].save('PAN'+ str(i) +'.jpg', 'JPEG')


# ## Find the DoB

# In[119]:


custom_config = r'--oem 1 --psm 6'
img = cv2.imread('Aadhaar_2.jpg')
img_gray = grayscale(img)
str1 = pytesseract.image_to_data(img_gray, config=custom_config)
str2 = str1.split()

for i in range(len(str1.split())):
    match = re.match(date_pattern , str2[i])
    if(match!= None):
        print(str2[i])


# ## Find the PAN Number

# In[18]:


custom_config = r'--oem 3 --psm 8'
img = cv2.imread('Text2.jpg')
img_gray = get_grayscale(img)
#img_gray = thresholding(img_gray)
#img_gray = dilate(img_gray)
#img_gray = erode(img_gray)
str1 = pytesseract.image_to_string(img, config=custom_config)
str1


# In[20]:


custom_config = r'--oem 3 --psm 8'
img = cv2.imread('Text6.jpg')
img_gray = get_grayscale(img)
#img_gray = thresholding(img_gray)
#img_gray = dilate(img_gray)
#img_gray = erode(img_gray)
str1 = pytesseract.image_to_string(img, config=custom_config)
str1


# ## My Pan Card text

# In[41]:


custom_config = r'--oem 3 --psm 8'
img = cv2.imread('Text14.jpg')
img_gray = get_grayscale(img)
#img_gray = thresholding(img_gray)
#img_gray = dilate(img_gray)
#img_gray = erode(img_gray)
str1 = pytesseract.image_to_string(img_gray, config=custom_config)
str1


# In[43]:


custom_config = r'--oem 3 --psm 8'
img = cv2.imread('Text6.jpg')
img_gray = get_grayscale(img)
#img_gray = thresholding(img_gray)
#img_gray = dilate(img_gray)
#img_gray = erode(img_gray)
str1 = pytesseract.image_to_string(img_gray, config=custom_config)
str1


# In[40]:


custom_config = r'--oem 3 --psm 8'
img = cv2.imread('Text15.jpg')
img_gray = get_grayscale(img)
#img_gray = thresholding(img_gray)
#img_gray = dilate(img_gray)
#img_gray = erode(img_gray)
str1 = pytesseract.image_to_string(img_gray, config=custom_config)
str1


# In[42]:


custom_config = r'--oem 3 --psm 8'
img = cv2.imread('Text7.jpg')
img_gray = get_grayscale(img)
#img_gray = thresholding(img_gray)
#img_gray = dilate(img_gray)
#img_gray = erode(img_gray)
str1 = pytesseract.image_to_string(img_gray, config=custom_config)
str1


# ## End of PAN Card
