import cv2
import Util
import numpy as np

inputImage = cv2.imread("yier3.png")
inputHeight = len(inputImage)
inputWidth = len(inputImage[0])

wMin = inputWidth
wMax = -1
# draw black line
for w in range(inputWidth):
    if inputImage[inputHeight - 1, w][0] < 100 and inputImage[inputHeight - 1, w][1] < 100 and inputImage[inputHeight - 1, w][2] < 100:
        if w < wMin:
            wMin = w
        if w > wMax:
            wMax = w
                
if wMax != -1:           
    for w in range(wMin, wMax + 1):
        inputImage[inputHeight - 1, w] = inputImage[inputHeight - 1, wMax]

#inputImage = cv2.resize(inputImage, (276, 200))
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

_, inputContours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

hierarchy = hierarchy[0]
# for i in range(len(hierarchy)):
#     print(i)
#     print(hierarchy[i])

allParents = Util.findAllParents(hierarchy)
largestParentIndex = -1
maxArea = -1

print(allParents)

for i in range(len(allParents)):
      contour = inputContours[allParents[i]][:, 0, :]
      area = cv2.contourArea(contour) 
      
      if area > maxArea:
          largestParentIndex = allParents[i]
          maxArea = area

workImage = np.zeros((inputHeight, inputWidth, 3), dtype = np.uint8)
for h in range(inputHeight):
    for w in range(inputWidth):
        workImage[h, w] = (255, 255, 255)
        
goodContours = []
goodContours.append(inputContours[largestParentIndex][:, 0, :])

for index in range(len(hierarchy)):
    contour = inputContours[index][:, 0, :]
    area = cv2.contourArea(contour)
    if area < 40:
        continue
    
    nextSibling, prevSibling, firstChild, parent = hierarchy[index]
    if parent == largestParentIndex:
        if len(goodContours) == 0:
            goodContours.append(contour)
            continue
    
        if area < cv2.contourArea(goodContours[-1]):
            goodContours.append(contour)
            continue    
        
        for i in range(len(goodContours)):
            if area > cv2.contourArea(goodContours[i]):
                goodContours.insert(i, contour)
                break
    
#for contour in goodContours:
#    for point in contour:
#        ww, hh = point
#        workImage[hh, ww] = (0, 0, 255) # b g r

# for point in inputContours[0][:, 0, :]: #24 25 31 33 34 36
#     ww, hh = point
#     workImage[hh, ww] = (0, 0, 255) # b g r
    
# for point in inputContours[2][:, 0, :]: #24 25 29 31 33 34 36
#     ww, hh = point
#     workImage[hh, ww] = (0, 255, 0) # b g r

# for point in inputContours[36][:, 0, :]: #24 25 29 31 33 34 36
#     ww, hh = point
#     workImage[hh, ww] = (255, 0, 0) # b g r
  
# draw a layer of brown inside the contour
earContour = []
thickness = 5
for point in goodContours[0]:
    w, h = point
    
    for wLayer in range(w - thickness, w + thickness):
        for hLayer in range(h - thickness, h + thickness):
            if abs(wLayer - w) > 3 or abs(hLayer - h) > 3: 
                containResult = cv2.pointPolygonTest(goodContours[0], (wLayer, hLayer), False)
                
                if containResult == 1:
                    workImage[hLayer, wLayer] = Util.BUBUBODY
                    earContour.append((hLayer, wLayer))
    

  
hMin = inputHeight
hMax = -1
for point in goodContours[0]:
    ww, hh = point
    if hh < hMin:
        hMin = hh
    if hh > hMax:
        hMax = hh
        
for h in range(hMin, hMax):
    wMin = inputWidth
    wMax = -1
    
    for point in goodContours[0]:
        w, hTemp = point
        if abs(hTemp - h) < 3:
            if w < wMin:
                wMin = w
            if w > wMax:
                wMax = w
                
    for w in range(wMin, wMax):
        containResult = cv2.pointPolygonTest(goodContours[0], (w, h), False) 
        if containResult == -1:
            continue
        
        color = inputImage[h, w]
        if Util.isYiErBody(color):
            workImage[h, w] = Util.BUBUBODY
        elif Util.isYiErCheek(color):
            workImage[h, w] = Util.BUBUCHEEK          
        else:
            if (h, w) in earContour:
                continue
            else:
                workImage[h, w] = inputImage[h, w]

cv2.imshow('', workImage)
cv2.waitKey(0)









