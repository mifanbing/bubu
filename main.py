import cv2
import math
import numpy as np

inputImage = cv2.imread("yier.jpeg")
canny_low = 100
canny_high = 200
    
# Convert image to grayscale        
image_gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
# Apply Canny Edge Dection
edges = cv2.Canny(image_gray, canny_low, canny_high)
edges = cv2.dilate(edges, None)
edges = cv2.erode(edges, None)
# get the contours and their areas
# hierarchy:4 elements
# 0, 1: next and previous contours at the same hierarchical level, 
# the first child contour 
# the parent contour,

_, inputContours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

#print(hierarchy)
  
inputHeight = len(inputImage)
inputWidth = len(inputImage[0])
workImage = np.zeros((inputHeight, inputWidth, 3), dtype = np.uint8)
for h in range(inputHeight):
    for w in range(inputWidth):
        workImage[h, w] = (255, 255, 255)
        

# Assume head is biggest contour

goodContours = []
for contour in inputContours:
    area = cv2.contourArea(contour[:, 0, :])

    if area < 20:
        continue
    
    # for point in contour[:, 0, :]:
    #     ww, hh = point
    #     workImage[hh, ww] = (0, 0, 255)
    
    if len(goodContours) == 0:
        goodContours.append(contour[:, 0, :])
        continue
    
    if area < cv2.contourArea(goodContours[-1]):
        goodContours.append(contour[:, 0, :])
        continue    
    
    for i in range(len(goodContours)):
        if area > cv2.contourArea(goodContours[i]):
            goodContours.insert(i, contour[:, 0, :])
            break
        
# head
for point in goodContours[14]:
    ww, hh = point
    workImage[hh, ww] = (0, 0, 255)



hMin = inputHeight
hMax = -1
for point in goodContours[14]:
    ww, hh = point
    if hh < hMin:
        hMin = hh
    if hh > hMax:
        hMax = hh
        
for h in range(hMin, hMax):
    wMin = inputWidth
    wMax = -1
    
    for point in goodContours[14]:
        w, hTemp = point
        if abs(hTemp - h) < 3:
            if w < wMin:
                wMin = w
            if w > wMax:
                wMax = w
                
    for w in range(wMin, wMax):
        color = inputImage[h, w]
        if color[0] > 240 and color[1] > 240 and color[2] > 240:
            workImage[h, w] = (140, 166, 220)
        else:
            workImage[h, w] = inputImage[h, w]
            
#5: left eye
#7: right eye    

cv2.imshow('', workImage)
cv2.waitKey(0)
