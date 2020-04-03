import random
import pyrebase  # You can use the pyrebase library to work on the firebase connection from Raspberry Pi
import time
import math

import colourObjectDetection
import Color_recog

from VL53L0X_rasp_python_master.python import VL53L0X
import RPi.GPIO as GPIO


ledPin = 18


def databaseinit():
  global db
  global dev_id
  
  authFile = open('authFile','r')
  if authFile.mode == 'r':
      authList = authFile.read().split(':')
      apiKey = authList[0]
      dev_id = authList[1]
      
  
      config = {
            "apiKey": apiKey,
            "authDomain": "rvr-resistor-value-recognizer.firebaseapp.com",
            "databaseURL": "https://rvr-resistor-value-recognizer.firebaseio.com",
            "storageBucket": "rvr-resistor-value-recognizer.appspot.com"
          }
      firebase = pyrebase.initialize_app(config)
      db = firebase.database()
  authFile.close()
  
def tofInit():
    # Create a VL53L0X object
    tof = VL53L0X.VL53L0X(address=0x2B)

    # Start ranging
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    return tof

def lightTofCtrl(ledPwm):
    ledPwm.ChangeDutyCycle(0)
    
    distance = tof.get_distance()
    if (distance < 100):
        ledPwm.ChangeDutyCycle(100)
        
    
def ledInit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin, GPIO.OUT)

    pwm = GPIO.PWM(ledPin, 100) #100 Hz
    pwm.start(0)
    return pwm



if __name__ == '__main__':
  databaseinit()
  
  if (dev_id != None):
      tof = tofInit()
      ledPwm = ledInit()
      
      
      while (True):
          try:
              lightTofCtrl(ledPwm)
              
              
              
              #Get the requestcode for this device
              request = db.child('devices').child(dev_id).child('request').get()
              print('Requestcode: ' + str(request.val()))
              
              #If the requestcode is not 0, take a scan and update the database
              if (request.val() != 0):
                  
                  code = colourObjectDetection.readColourCodes(debug=True)
                  codeStr = Color_recog.code2str(code)
                  
                  #Create the data
                  data = {'device':dev_id, 'timestamp':time.ctime(time.time()), 'type':None, 'value':codeStr}
                  
                  try:
                      #Push the data into the historydata of the user ID given in the requestcode
                      db.child('historydata').child(request.val()).push(data)
                      
                      db.child('devices').child(dev_id).child('request').set(0)
                      print('scan uploaded')
                      print(data)
                  except Exception as e:
                     print ("Database cannot be written, check the permission on database or the requestcode")
                     print(str(e))
                     
              #Check for a request every 2 seconds. Also controls how long lights stay on  
              time.sleep(2)
              
              
                  
          except KeyboardInterrupt:
              break
            
      tof.stop_ranging()
      pwm.stop()
      GPIO.cleanup()
      
  else:
      print('No device id found')
