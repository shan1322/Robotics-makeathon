import serial
import time
import requests
import json
import re
firebase_url = 'https://iot-data-d6cb8.firebaseio.com/'
#Connect to Serial Port for communication
ser = serial.Serial('COM11', 250000, timeout=0)
#Setup a loop to send Temperature values at fixed intervals
#in seconds


fixed_interval = 60
while 1:
  x = []
  try:
    #temperature value obtained from Arduino + DH11 Temp Sensor          
    sensor_c = ser.readline().decode('utf-8')
    x=re.split(" ",sensor_c)
    #current time and date
    time_hhmmss = time.strftime('%H:%M:%S')
    date_mmddyyyy = time.strftime('%d/%m/%Y')
    #current location name
    #print (temperature_c + ',' + time_hhmmss + ',' + date_mmddyyyy + ',' + temperature_location)
     
  #insert record
    if(len(x)==5):
      data = {'date':date_mmddyyyy,'time':time_hhmmss,'Temperature':x[0],'Humidity':x[1],'HeartRate_constant':x[2],'Shock Switch':x[3],'Alert Button Press Status':x[4]}
      result = requests.post(firebase_url + '/sensor.json', data=json.dumps(data))
      print ('Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text)
      time.sleep(fixed_interval)
    else:
      print("Please Wait Initializing......")
    
  except IOError:
    print('Error! Something went wrong.')
    time.sleep(fixed_interval)
