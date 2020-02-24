#!/usr/bin/env python3
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime
import RPi.GPIO as GPIO
from random import random

import requests
import logging
import boto3
from botocore.exceptions import ClientError

LedPin_1 = 36
LedPin_2 = 35
Button_1 = 38
Button_2 = 40

session_id = ""
active_session = False
session_started = False

disp_1 = ""
disp_2 = ""

KAMN_API_URL = 'https://3lyr5z791l.execute-api.us-west-2.amazonaws.com/Prod'

bucket = '460163561631-us-west-2-sourceaudiobucket'
file_name = '4389_1.mp3'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#Numbers GPIOs by physical location
GPIO.setup(LedPin_1, GPIO.OUT) # Set LedPin's mode is output
GPIO.output(LedPin_1, GPIO.HIGH)  # Set LedPin to low
GPIO.setup(LedPin_2, GPIO.OUT) # Set LedPin's mode is output
GPIO.output(LedPin_2, GPIO.HIGH)  # Set LedPin to low
GPIO.setup(Button_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_2, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

p = GPIO.PWM(LedPin_1, 60) # set Frequece to 1KHz
p.start(0)                       # Duty Cycle = 0
g = GPIO.PWM(LedPin_2, 1000)
g.start(0)


        
def setdisp_1(input):
    try:
        global disp_1 
        disp_1 = str(input).strip()
        return 1
    except:
        print('Threading error... value is unknown\n')
        return 0
        
def setdisp_2(input):
    try:
        global disp_2
        disp_2 = str(input).strip()
        return 1
    except:
        print('Threading error... value is unknown\n')
        return 0  
        
def getdisp_1():
    global disp_1
    return disp_1
    
def getdisp_2():
    global disp_2
    return disp_2
    
def create_session():
    global active_session,file_name,bucket,KAMN_API_URL
    if(not active_session):
        active_session = True 
        session_id = ""
        PARAMS = {'session_id': session_id} 
        r = requests.get(url = KAMN_API_URL, params = PARAMS)
        data = r.json()
        logging.info(data)
        
        
        print(str(data) + "t\n")
        global LedPin_1
        global p 
        p.ChangeDutyCycle(100)
        return True
    else: #do nothing if session is already made  
        return True
        
def start_stop_session():
    global session_started
    global active_session
    global p,g,LedPin_1,LedPin_2
    # upload_file(file_name, bucket,None)
    if(not session_started and active_session):#session active && not started yet --> starting
        p.ChangeDutyCycle(20)
        g.ChangeDutyCycle(0)
        session_started = True
        ##look in KAMN-API-DATA-TIER index.js create 
        ##set session id 
        return True
    elif(session_started and active_session):#session active && started --> ending
        session_id = "" ##4389
        p.ChangeDutyCycle(0)
        g.ChangeDutyCycle(20)
        session_started = False 
        active_session = False
        return False
    else:#session was not active --> do nothing
        session_id = ""
        g.ChangeDutyCycle(0)
        session_started = False
        return False
        
def getbutton_1(channel): 
    print("Pressed 1\n")
    create_session()
    
def getbutton_2(channel): 
    print("Pressed 2\n")
    start_stop_session()
        
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def loop():
    setdisp_1("Hello")
    setdisp_2(get_time_now())
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    global Button_1
    global Button_2
    GPIO.add_event_detect(Button_1,GPIO.RISING,callback=getbutton_1) 
    GPIO.add_event_detect(Button_2,GPIO.RISING,callback=getbutton_2) 
    
    while(True):         
        try:
            lcd.clear()
            lcd.setCursor(0,0)  # set cursor position
            
            lcd.message(getdisp_1() + '\n')
            lcd.message(getdisp_2() + '\n')   # display the tim
                
            sleep(.3)
        except KeyboardInterrupt:
            exit(1)
        
        
def upload_file(file_name, bucket, object_name):
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        setDisplay_1('Uploaded:' + file_name);
    except ClientError as e:
        logging.error(e)
        return False
    return True

def destroy():
    lcd.clear()
    global p
    p.stop()
    GPIO.output(LedPin_1, GPIO.LOW)    # turn off led
    GPIO.cleanup()
    
PCF8574_address  = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print ('I2C Address Error !')
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

