# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:36:40 2020

@author: bdwoo
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 18:03:13 2019

@author: bdwoo
"""
import cv2
import numpy as np
import sys

#TODO: 
#   Order resistor colour codes
#   Calc average V and use to adjust V for lighting intensity
#   Locate resistor based on contour or tan/blue colour

#Resources
"""
https://sites.google.com/site/ohmcalcucsb/
https://github.com/windmill-cloud/AndroidEmb/blob/master/OhmCalcBase/app/src/main/java/edu/ucsb/ece/ece150/ohmcalcbase/OhmCalcImageProcessor.java

https://hackaday.com/2015/05/14/reading-resistors-with-opencv/
https://github.com/thegouger/ResistorScanner
"""


class ColourCode:
    def __init__(self, rVal):
        self.name = rVal
        self.prev = None
        self.prevVal = None
        self.next = None
        self.nextVal = None
        
    def __str__(self):
        return self.name
    
    def getName(self):
        return self.name
    def getPrev(self):
        return self.prev
    def getNext(self):
        return self.next
    
    def setName(self, name):
        self.name = str(name)
    def setPrev(self, prev):
        self.prev = prev
    def setNext(self, next):
        self.next = next
        
class ColourCodeSort:
    def __init__(self, rValList):
        self.rValList = rValList
        self.distances = []
        self.rValCodes = []
        
        
    def __str__(self):
        return rValList

#Update global threshold values on trackbar callback
#Safety to ensure min is always smaller than max
def updateHmin1(val):
    global thresh
    thresh['hMin'] = min(thresh['hMax']-1, val)
    cv2.setTrackbarPos('H1 min', 'Threshold', thresh['hMin'])
def updateHmax1(val):
    global thresh
    thresh['hMax'] = max(thresh['hMin']+1, val)
    cv2.setTrackbarPos('H1 max', 'Threshold', thresh['hMax'])
def updateSmin1(val):
    global thresh
    thresh['sMin'] = min(thresh['sMax']-1, val)
    cv2.setTrackbarPos('S1 min', 'Threshold', thresh['sMin'])
def updateSmax1(val):
    global thresh
    thresh['sMax'] = max(thresh['sMin']+1, val)
    cv2.setTrackbarPos('S1 max', 'Threshold', thresh['sMax'])
def updateVmin1(val):
    global thresh
    thresh['vMin'] = min(thresh['vMax']-1, val)
    cv2.setTrackbarPos('V1 min', 'Threshold', thresh['vMin'])
def updateVmax1(val):
    global thresh
    thresh['vMax'] = max(thresh['vMin']+1, val)
    cv2.setTrackbarPos('V1 max', 'Threshold', thresh['vMax'])
    

#Select a subregion of the image where the resistor is
def getResistorLoc(hsvFrame, thresh, text):
    global rValList
    
    #filter out colours in range using the values from the trackbars
    mask = cv2.inRange(hsv, (thresh['hMin'], thresh['sMin'], thresh['vMin']), (thresh['hMax'], thresh['sMax'], thresh['vMax']))
    
    #Opening consists of eroding, then dilating
    #erode to remove false positive noise
    mask = cv2.erode(mask, kernel, iterations=1)
    #dilate to undo the effect of erode on our object, and remove false negative noise
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
   
    height, width, _ = hsvFrame.shape
    minX = width
    minY = height
    maxX = 0
    maxY = 0
    
    for c in contours:
        moment = cv2.moments(c)
        area = moment['m00']
        
        if area > 250:
            #Find the bounds for the ROI rectangle
            (cX,cY,w,h) = cv2.boundingRect(c)
            minX, maxX = min(cX, minX), max(cX+w, maxX)
            minY, maxY = min(cY, minY), max(cY+h, maxY)
            
            x = int(moment['m10']/area)
            y = int(moment['m01']/area)
            
            cv2.circle(frame, (x,y), 3, (255,0,0), 2)
            write(frame, text, x, y)
            
            #input image, contours array, contours to draw, colour to draw with, line width (if -ve, interiour of contour filled)
            cv2.drawContours(frame, c, -1, (0, 255, 0), 2)
    print('minX:' + str(minX) + ' maxX' + str(maxX) + '  minY:' + str(minY) + ' maxY' + str(maxY))
    cv2.rectangle(hsv, (minX,minY), (maxX,maxY), (0,0,255), 2)
    
    return frame[minY:maxY, minX:maxX]


def write(frame, text, x, y):
    cv2.putText(
     frame, #numpy array on which text is written
     text, #text
     (int(x), int(y)), #position at which writing has to start
     cv2.FONT_HERSHEY_SIMPLEX, #font family
     1, #font size
     (255, 0, 0)) #font color

    
#Create the kernel to be used for eroding. Be sure to use numpy, or it will be slow
kernel = np.ones((5, 5), np.uint8)

#Create the list to store the values and locations of resistor colour codes
rValList = []

tanThresh = {'hMin' : 0, 'hMax' : 20, 'sMin' : 70, 'sMax' : 144, 'vMin' : 53, 'vMax' : 181}
bUmberThresh  ={'hMin' : 0, 'hMax' : 190, 'sMin' : 70, 'sMax' : 144, 'vMin' : 53, 'vMax' : 181}

orangeThresh = {'hMin' : 0, 'hMax' : 20, 'sMin' : 44, 'sMax' : 144, 'vMin' : 53, 'vMax' : 181}
yellowThresh = {'hMin' : 21, 'hMax' : 38, 'sMin' : 78, 'sMax' : 255, 'vMin' : 129, 'vMax' : 232}

orangeThreshLowLight = {'hMin' : 0, 'hMax' : 10, 'sMin' : 140, 'sMax' : 255, 'vMin' : 72, 'vMax' : 174}
yellowThreshLowLight = {'hMin' : 21, 'hMax' : 38, 'sMin' : 133, 'sMax' : 255, 'vMin' : 29, 'vMax' : 133}


thresh = bUmberThresh

video = cv2.VideoCapture(0)

cv2.namedWindow('Threshold')
cv2.createTrackbar('H1 min', 'Threshold', thresh['hMin'], 255, updateHmin1)
cv2.createTrackbar('H1 max', 'Threshold', thresh['hMax'], 255, updateHmax1)
cv2.createTrackbar('S1 min', 'Threshold', thresh['sMin'], 255, updateSmin1)
cv2.createTrackbar('S1 max', 'Threshold', thresh['sMax'], 255, updateSmax1)
cv2.createTrackbar('V1 min', 'Threshold', thresh['vMin'], 255, updateVmin1)
cv2.createTrackbar('V1 max', 'Threshold', thresh['vMax'], 255, updateVmax1)


ret, frame = video.read()
width, height = frame.shape[:2]


while True:
    ret, frame = video.read()
    
    #Clear rValList so it only holds the resistor values for this frame
    rValList = []
    
    #Flip the frame so it isn't backwards
    frame = cv2.flip(frame, 1)

    #Convert to HSV colourspace, which is better for colour detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    roi = getResistorLoc(hsv, thresh, "Orange")
    
    height, width, _ = roi.shape
    
    if height > 0 and width > 0:
        cv2.imshow("Contours", roi)
    

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
