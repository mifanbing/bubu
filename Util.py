import math

# b g r
BUBUCHEEK = [125, 191, 249]
YIERCHEEK = [190, 195, 255]
BUBUBODY = [140, 166, 220]
YIERBODY = [255, 255, 255]

DIFFTHRESHHOLD = 25

def isBuBuCheek(color):
    diff = 0
    for i in range(3):
        diff = diff + abs(color[i] - BUBUCHEEK[i])
    return diff < DIFFTHRESHHOLD

def isYiErCheek(color):
    diff = 0
    for i in range(3):
        diff = diff + abs(color[i] - YIERCHEEK[i])
    return diff < DIFFTHRESHHOLD

def isBuBuBody(color):
    diff = 0
    for i in range(3):
        diff = diff + abs(color[i] - BUBUBODY[i])
    return diff < DIFFTHRESHHOLD

def isYiErBody(color):
    diff = 0
    for i in range(3):
        diff = diff + abs(color[i] - YIERBODY[i])
    return diff < DIFFTHRESHHOLD

def findTopParent(hierarchy, index):
    while True:
        _, _, _, parent = hierarchy[index]
        if parent == -1:
            return index
        else:
            index = parent
    

def findAllParents(hierarchy):
    allParents = []
    
    for index in range(len(hierarchy)):
        _, _, _, parent = hierarchy[index]
        if parent == -1:
            allParents.append(index)
        
    return allParents

