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
    

    #Get the two closest contours and their distances with Pythagorean
    def calcClosestDistances(self):

        if len(self.rValList) > 1:
            self.distances = []
        
            #Loop through the rValList
            for i in range(len(self.rValList)):
                min1 = sys.maxsize
                min2 = sys.maxsize
                closest1 = None
                closest2 = None
                x = self.rValList[i][1]
                y = self.rValList[i][2]
                self.distances.append(1)
                
                #For each value, look through the list and find the two closest
                for j in range(len(self.rValList)):
                    #Don't check a value against itself
                    if i != j:
                        distance = np.sqrt(np.square(x-self.rValList[j][1]) + np.square(y-self.rValList[j][2]))
                        if distance < min1:
                            #Ensure a new smaller value does not overwrite the old one, but stores as second smallest
                            if min1 != sys.maxsize:
                                min2 = min1
                                closest2 = closest1
                            min1 = distance
                            closest1 = j
                        elif distance < min2:
                            min2 = distance
                            closest2 = j
                #Store the closest distances for each
                val1 = None if closest1 == None else self.rValList[closest1][0]
                val2 = None if closest2 == None else self.rValList[closest2][0]
                
                #Store indexes of 2 closest contours
                self.distances.append((closest1, closest2, min1, min2))
                
        def calcColourCode(self):
            if len(self.distances) > 1:
                #Find one end of the resistor: look for gold
                
def calcColourCodeV2():
    global rValList
        
    sort = ColourCodeSort(rValList)
    sort.calcClosestDistances()
    
    #Find smallest Pythagorean distance between resistor codes
    #Use to sort list based on their relationship to each other
    #Obtain ordered list of colour codes in order
    
    #For Husnal:
    #Check first value. If it is a tolerance, go backwards, otherwise, go forwards
"""

#Make thesh global so it can be accessed by trackbar callbacks
thresh = []

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
def getResistorLoc(frame, threshList, kernel):
    #Convert to HSV colourspace, which is better for colour detection
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    height, width, _ = hsvFrame.shape
    mask = np.zeros((height, width), np.uint8)
    for thresh in threshList:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsvFrame, (thresh['hMin'], thresh['sMin'], thresh['vMin']), (thresh['hMax'], thresh['sMax'], thresh['vMax'])))
    
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
                        

    #print('minX:' + str(minX) + ' maxX' + str(maxX) + '  minY:' + str(minY) + ' maxY' + str(maxY))
    cv2.rectangle(hsvFrame, (minX,minY), (maxX,maxY), (0,0,255), 2)
    
    return frame[minY:maxY, minX:maxX], hsvFrame[minY:maxY, minX:maxX]


def getColourContours(roi, roihsv, thresh, text, kernel, rValList):
    #filter out colours in range using the values from the trackbars
    mask = cv2.inRange(roihsv, (thresh['hMin'], thresh['sMin'], thresh['vMin']), (thresh['hMax'], thresh['sMax'], thresh['vMax']))
    
    #Opening consists of eroding, then dilating
    #erode to remove false positive noise
    mask = cv2.erode(mask, kernel, iterations=1)
    #dilate to undo the effect of erode on our object, and remove false negative noise
    mask = cv2.dilate(mask, kernel, iterations=2)
    
        #hierarchy describes how contours are nested.
    #RETR_EXTERNAL says we only take the outermost contour, so there is no hierarchy
    #Stores the points representing the boundary of the contours
    #APPROX_SIMPLE approximmates the object to minimize the number of points to save memory
    #APPROX_NONE makes no approximations, and stores more points
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
   
        #Hierarchy at [i][0] is the index of the next contour at the same level. When it is negative, there are no more contours
    for c in contours:
        moment = cv2.moments(c)
        area = moment['m00']
        
        if area > 250:
            x = int(moment['m10']/area)
            y = int(moment['m01']/area)
            
            #cv2.circle(roi, (x,y), 3, (255,0,0), 2)
            write(roi, text, x, y)
            
            #Add the locations to the rValList, which tracks the locations and values of resistor colour codes
            rValList.append((text, x, y))
            
            #input image, contours array, contours to draw, colour to draw with, line width (if -ve, interiour of contour filled)
            cv2.drawContours(roi, c, -1, (0, 255, 0), 2)
    
    return mask


def write(frame, text, x, y):
    cv2.putText(
     frame, #numpy array on which text is written
     text, #text
     (int(x), int(y)), #position at which writing has to start
     cv2.FONT_HERSHEY_SIMPLEX, #font family
     1, #font size
     (255, 0, 0)) #font color
    
#Blindly get colours from left to right
def calcColourCodeV1(rValList):
    #Make a new list of rVals from left to right
    lToR = []
    
    #Go until entire list is empty
    for i in range(len(rValList)):
        
        minX = rValList[0]
        #Find smallest x value (leftmost) and store in list
        for val in rValList[1:]:
            if val[1] < minX[1]:
                minX = val
                
        #Add the smallest item to the sorted list and get rid of the old value
        lToR.append(minX[0])
        rValList.remove(minX)
        
    return lToR

#Lookup for colour codes
def color_string(n):
    switcher={
            0:'black',
            1:'brown',
            2:'red',
            3:'orange',
            4:'yellow',
            5:'green',
            6:'blue',
            7:'violet',            
            8:'grey',
            9:'white',
            10:'gold'
            }
    return switcher.get(n, 'invalid')


def readColourCodes(debug=False):
    global thresh
    
    #Create the kernel to be used for eroding. Be sure to use numpy, or it will be slow
    kernel = np.ones((5, 5), np.uint8)

    #Test values for markers
    """
    orangeThresh = {'hMin' : 0, 'hMax' : 10, 'sMin' : 178, 'sMax' : 255, 'vMin' : 220, 'vMax' : 255}
    yellowThresh = {'hMin' : 21, 'hMax' : 38, 'sMin' : 78, 'sMax' : 255, 'vMin' : 129, 'vMax' : 232}

    orangeThreshLowLight = {'hMin' : 0, 'hMax' : 10, 'sMin' : 140, 'sMax' : 255, 'vMin' : 72, 'vMax' : 174}
    yellowThreshLowLight = {'hMin' : 21, 'hMax' : 38, 'sMin' : 133, 'sMax' : 255, 'vMin' : 29, 'vMax' : 133}
    """

    rBackingColour = []
    rBackingColour.append({'hMin' : 0, 'hMax' : 20, 'sMin' : 45, 'sMax' : 144, 'vMin' : 53, 'vMax' : 181}) #tan
    rBackingColour.append({'hMin' : 81, 'hMax' : 194, 'sMin' : 82, 'sMax' : 191, 'vMin' : 12, 'vMax' : 166}) #blue
    rBackingColour.append({'hMin' : 0, 'hMax' : 190, 'sMin' : 70, 'sMax' : 144, 'vMin' : 53, 'vMax' : 181}) #burnt umber (same as tan, but hMax is 190


    #Create list of thresholds for each colour code
    codeThresh = []
    
    codeThresh.append({'hMin' : 0, 'hMax' : 165, 'sMin' : 0, 'sMax' : 250, 'vMin' : 0, 'vMax' : 65})    #Black
    codeThresh.append({'hMin' : 114, 'hMax' : 205, 'sMin' : 70, 'sMax' : 125, 'vMin' : 44, 'vMax' : 148})    #Brown
    codeThresh.append({'hMin' : 148, 'hMax' : 185, 'sMin' : 105, 'sMax' : 172, 'vMin' : 59, 'vMax' : 200})    #Red
    codeThresh.append({'hMin' : 0, 'hMax' : 12, 'sMin' : 100, 'sMax' : 137, 'vMin' : 20, 'vMax' : 243})    #Orange
    codeThresh.append({'hMin' : 11, 'hMax' : 27, 'sMin' : 30, 'sMax' : 119, 'vMin' : 70, 'vMax' : 255})    #Yellow
    codeThresh.append({'hMin' : 56, 'hMax' : 117, 'sMin' : 0, 'sMax' : 130, 'vMin' : 0, 'vMax' : 180})    #Green
    codeThresh.append({'hMin' : 105, 'hMax' : 117, 'sMin' : 132, 'sMax' : 177, 'vMin' : 33, 'vMax' : 255})    #Blue
    codeThresh.append({'hMin' : 118, 'hMax' : 152, 'sMin' : 67, 'sMax' : 134, 'vMin' : 45, 'vMax' : 185})    #Violet
    codeThresh.append({'hMin' : 113, 'hMax' : 140, 'sMin' : 18, 'sMax' : 58, 'vMin' : 00, 'vMax' : 185})    #Grey proto
    codeThresh.append({'hMin' : 117, 'hMax' : 160, 'sMin' : 16, 'sMax' : 34, 'vMin' : 151, 'vMax' : 255})    #White proto

    #codeThresh.append({'hMin' : 0, 'hMax' : 15, 'sMin' : 40, 'sMax' : 86, 'vMin' : 83, 'vMax' : 255})    #Gold proto

    #Set up trackbars to adjust a specific threshold if debug mode
    if (debug):
        thresh = codeThresh[1]
        cv2.namedWindow('Threshold')
        cv2.createTrackbar('H1 min', 'Threshold', thresh['hMin'], 255, updateHmin1)
        cv2.createTrackbar('H1 max', 'Threshold', thresh['hMax'], 255, updateHmax1)
        cv2.createTrackbar('S1 min', 'Threshold', thresh['sMin'], 255, updateSmin1)
        cv2.createTrackbar('S1 max', 'Threshold', thresh['sMax'], 255, updateSmax1)
        cv2.createTrackbar('V1 min', 'Threshold', thresh['vMin'], 255, updateVmin1)
        cv2.createTrackbar('V1 max', 'Threshold', thresh['vMax'], 255, updateVmax1)


    video = cv2.VideoCapture(0)
    ret, frame = video.read()
    width, height = frame.shape[:2]


    while True:
        ret, frame = video.read()
        
        #Create the list to store the values and locations of resistor colour codes
        rValList = []
        
        
        #Flip the frame so it isn't backwards
        frame = cv2.flip(frame, 1)

        

        """
        orangeMask = getColourContours(hsv, orangeThresh, "Orange")
        yellowMask = getColourContours(hsv, yellowThresh, "Yellow")
        
        finalMask = cv2.bitwise_or(orangeMask, yellowMask)
        """
        
        #TODO (optional): locate resistor location by base colour using boundingRect around contours
        #Search each submat at this location individually for resistor colour codes to scan multiple resistors
        #Potential problem: colour will be split into several contours due to colour codes
        roi, roihsv = getResistorLoc(frame, rBackingColour, kernel)
        
        height, width, _ = roi.shape
        if height > 0 and width > 0: 
            #Acquire all masks for all colour codes
            maskList = []
            for i in range(len(codeThresh)):
                maskList.append(getColourContours(roi, roihsv, codeThresh[i], color_string(i), kernel, rValList))
            
            finalMask = maskList[0]
            for i in range(1, len(maskList)):
                finalMask = cv2.bitwise_or(finalMask, maskList[i])
                
            #TODO: Alter rValList to contain the size of the contours
            #If we expect 4 bands, only keep the four largest contours to remove contours split in half
                
            
            print('Values')
            print(rValList)
            
            codes = calcColourCodeV1(rValList)
            #calcColourCodeV2()
            
            cv2.imshow("Filter", finalMask)
            cv2.imshow("Contours", roi)
            
            #Only loop continously in debug mode. Otherwise, just take a single picture
            if not debug:
                break

            if cv2.waitKey(200) & 0xFF == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()
    return codes



if __name__ == '__main__':
    print(readColourCodes(debug=True))

