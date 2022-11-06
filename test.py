import cv2
import Util
import numpy as np

inputImage = cv2.imread("yier3.png")
inputHeight = len(inputImage)
inputWidth = len(inputImage[0])

workImage = np.zeros((inputHeight, inputWidth, 3), dtype = np.uint8)
for h in range(inputHeight):
    for w in range(inputWidth):
        workImage[h, w] = (0, 0, 0 )
        
wMin = inputWidth
wMax = -1
# draw black line
for w in range(inputWidth):
    for h in range(inputHeight - 5, inputHeight):
        #workImage[h, w] = inputImage[h, w]
        if inputImage[h, w][0] < 80 and inputImage[h, w][1] < 80 and inputImage[h, w][2] < 80:
            if w < wMin:
                wMin = w
            if w > wMax:
                wMax = w
        
        
print(wMin)
print(wMax)        
        
# cv2.imshow('', workImage)
# cv2.waitKey(0)
