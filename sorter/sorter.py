#!/usr/bin/python3
##############################################################################################
## Company: FSAE Lafayette College                                                               
## Engineers: Tafita Rakotozandry 
## Last Updated : 05/11/2022 5:14 PM                       
## Project Name: SCADA FSAE 2022                                 
## Module Name: sorter.py                                                 
## Description: Sorter module used to iterate through the list of defined sensors and display 
##the data              
#############################################################################################
import sys, os
import time
import smbus

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'


sys.path.append(lib_path)
sys.path.append(config_path)

from drivers import driver
import config
import utils
from utils import rtc_setup
from utils import imu_setup

##########Declariing i2C Bus##############
bus = smbus.SMBus(3) 

########################################## 


# ##Setting up connectiion to Redis Server###
# Redisdata = redis.Redis(host='localhost', port=6379, db=0)
# data = Redisdata.pubsub()
# data.subscribe('raw_data')
# ###########################################


# #######Configuring Pi Time on Boot########
# rtc_setup.set_RTCtime()
# ########################################## 


###Local Dictionary for Sensor Period Count####
SensorList = config.get('Sensors')
last_sampled = {}
sample_period = {}

for key in config.get('Sensors'):
    sample_period[key] = SensorList.get(key).get('sample_period')
    last_sampled[key] = time.time()
###############################################


while True: 

    # Go through the sensorList read on the Yalm file and display the readings 
    for sensorName in SensorList :
        try:
            print(sensorName+ " "+ str(driver.read(sensorName)))
        except:
            print("Error in  the reading  "+sensorName)
            pass

        #if(sensorName=="emulator_car_mph"):
            #print(driver.read(sensorName))

    #time.sleep(3)
    print("New Reading")
