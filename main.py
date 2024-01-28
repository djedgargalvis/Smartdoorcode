try:
    import urequests as requests
except ImportError:
    import requests

from time import sleep
import time

import esp
esp.osdebug(None)
import gc
gc.collect()

phone_number = '573015688459'
api_key = '6136738'

def send_message(phone_number, api_key, message):
    url = 'https://api.callmebot.com/whatsapp.php?phone='+phone_number+'&text='+message+'&apikey='+api_key
    try:
        start_time = time.ticks_ms()
        response = requests.get(url)
    
        if response.status_code == 200:
            print('¡Éxito!')
        else:
            print('Error')
            print(response.text)
    except Exception as e:
        print('Error:', e)

    gc.collect()

from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from machine import Pin
from machine import SoftI2C
from machine import SPI
import network
import time 

I2C_ADDR =0x27
totalrows = 2
totalcolumns =16

i2c = SoftI2C(scl=Pin(22, Pin.OUT, Pin.PULL_UP),
              sda=Pin(21, Pin.OUT, Pin.PULL_UP),
              freq=10000) 
lcd = I2cLcd(i2c,I2C_ADDR, totalrows, totalcolumns)

red = Pin(14, Pin.OUT)
grn = Pin(13, Pin.OUT)
rele = Pin(32, Pin.OUT)
spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    while not wlan.isconnected():
        print('Conectando...')
        wlan.connect('Wilson Castilla', '28868534*') # Coloca tu nombre de red y contraseña
        time.sleep(1)
    print('Conexión establecida!')

connect_wifi()

print("Place card")

lcd.putstr("Scan your room card")
time.sleep(5)
lcd.clear()

valid_card_ids = ["0xa4ed5b4d", "0xf644213f", "0x8804c482", "0x8804c91c", "0x650b6386"]


while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            lcd.clear()
            lcd.putstr("RFID: ")            
            card_id = "0x%02x%02x%02x%02x" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("UID:", card_id)        
            if card_id in valid_card_ids:
                rele.value(1)
                grn.value(True)           
                red.value(False)                
                lcd.putstr(" OK Welcome! Access Granted ")
                message = 'Usted%20ingreso%2C%20al%20cuarto'
                send_message(phone_number, api_key, message)
                time.sleep(6)
                lcd.clear()      
                rele.value(0)
                grn.value(False)                     
            else:
                rele.value(0)                               
                grn.value(False)                 
                red.value(True)               
                lcd.putstr(" Invalid Card! Access Denied ")
                message = 'Alguien%20intento%2C%20ingresar%20con%20tarjeta%20invalida'
                send_message(phone_number, api_key, message)                
                time.sleep(2)
                lcd.clear()
                red.value(False)