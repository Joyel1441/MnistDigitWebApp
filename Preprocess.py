import tensorflow as tf
import cv2
import numpy as np
import math
from scipy import ndimage
class Preprocess:
   
   def getBestShift(self,img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty
   def shift(self,img,sx,sy):
     rows,cols = img.shape
     M = np.float32([[1,0,sx],[0,1,sy]])
     shifted = cv2.warpAffine(img,M,(cols,rows))
     return shifted
   def preprocess(self,path):
    gray = cv2.imread(path, 0)
		# gray = cv2.imread(no, 0)

		# rescale it
    gray = cv2.resize(255-gray, (28, 28))
		# better black and white version
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    while np.sum(gray[0]) == 0:
        gray = gray[1:]

    while np.sum(gray[:,0]) == 0:
        gray = np.delete(gray,0,1)

    while np.sum(gray[-1]) == 0:
        gray = gray[:-1]

    while np.sum(gray[:,-1]) == 0:
        gray = np.delete(gray,-1,1)

    rows,cols = gray.shape

    if rows > cols:
        factor = 20.0/rows
        rows = 20
        cols = int(round(cols*factor))
			# first cols than rows
        gray = cv2.resize(gray, (cols,rows))
    else:
        factor = 20.0/cols
        cols = 20
        rows = int(round(rows*factor))
			# first cols than rows
        gray = cv2.resize(gray, (cols, rows))

    colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
    rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
    gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')

    shiftx,shifty = self.getBestShift(gray)
    shifted = self.shift(gray,shiftx,shifty)
    gray = shifted
		# save the processed images
    cv2.imwrite("./static/uploaded_images/preprocessed.jpeg", gray)
    return
       
