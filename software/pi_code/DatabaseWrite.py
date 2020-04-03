import random
import pyrebase  # You can use the pyrebase library to work on the firebase connection from Raspberry Pi
import time
import math

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
"""
def databasewrite(temperature, humidity, message):
  seconds = time.time()
  a = {"name": "Pyrebase", "temperature": str(int(math.ceil(temperature))),
       "humidity": str(int(math.ceil(humidity))), "message": message,
       "timestamp": str(int(math.ceil(seconds)))}
  try:
     db.child("data").push(a)
     print("Database writing success!")
  except:
     print ("Database cannot be written, check the permission on database")
"""
def main():
  databaseinit()
  
  
  if (dev_id != None):
      while (True):
          try:
              #Get the requestcode for this device
              request = db.child('devices').child(dev_id).child('request').get()
              print('Requestcode: ' + str(request.val()))
              
              #If the requestcode is not 0, take a scan and update the database
              if (request.val() != 0):
                  #Create the data
                  data = {'device':dev_id, 'timestamp':time.ctime(time.time()), 'type':'Resistor', 'value':'2kohm'}
                  
                  try:
                      #Push the data into the historydata of the user ID given in the requestcode
                      db.child('historydata').child(request.val()).push(data)
                      print('scan uploaded')
                  except Exception as e:
                     print ("Database cannot be written, check the permission on database or the requestcode")
                     print(str(e))
                     
              #Check for a request every 5 seconds    
              time.sleep(5)
              
              
                  
          except KeyboardInterrupt:
              break
  else:
      print('No device id found')
  
  """
  index = 0
  # Generate some random data to display on the database.
  while index <30:
    sign1= random.random()
    if (sign1 <0.5):
      sign1 = -1
    else:
      sign1 = 1
    temperature = 20+ random.random()*5*sign1
    humidity = 30 + random.random()*5*sign1*(-1)

    databasewrite( temperature, humidity, "This is from PC Testing: " + str(index))
    index += 1
     # write the data every 10 seconds. 
    time.sleep(10) """

if __name__ == '__main__':
    main()
