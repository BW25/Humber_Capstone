# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:02:26 2020

@author: Husnal
"""

import math

def color_value(name):
    switcher={
            'black': 0,
            'brown':1,
            'red':2,
            'orange':3,
            'yellow':4,
            'green':5,
            'blue':6,
            'violet':7,            
            'grey':8,
            'white':9
            }
    return switcher.get(name, 'wrong colour')
    
def tolerance(value):
    switcher={
            'brown':1,
            'red':2,
            'green':0.5, 
            'blue':0.25,
            'violet':0.10,
            'grey':0.05,
            'gold':5,
            'silver':10
            }
    return switcher.get(value, 'wrong colour')



def code2str(code):
    #6 band colour codes do exist, with the final band being temperature tolerance, but are not read
    if (len(code) >=6):
        print('Too many colour codes detected')
    elif (len(code) < 3):
        print('Not enough colour codes detected')   
    else:  
        #Three band colour codes have no tolerance band
        #For a three band colour code stop reading values before the last colour code, which is multiplier
        #For all others, stop reading before the second last colour code, which is multiplier, then tolerance
        if len(code) == 3:
            n = 1
        else:
            n = 2
            
        value = 0
        for i in range(len(code)-n):
            value = value*10
            value += color_value(code[i])
        multiplier = color_value(code[len(code)-n])
        value = value * math.pow(10, multiplier)
        
        #If it is a 3 band colour code, default tolerance of 20%
        if len(code) == 3:
            tol_Val = 20
        else:
            tol_Val = tolerance(code[len(code)-1])
        value = str(int(value)) + ' ohms ± ' + str(tol_Val) + '%'
        
        return str(value)
    
if __name__ == '__main__':
    testcode = ['brown','red','red','orange','gold']
    print(code2str(testcode))