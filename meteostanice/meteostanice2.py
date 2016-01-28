#Druhá verze meteostanice, přepíná mezi teplotami, přidané čidlo vnější teploty

from lcd_display import lcd
import RPi.GPIO as GPIO
import time
import dht11
import os
import glob

#Cteni ID tymu
file = open("id.txt", "r")
id = file.read()
id = id[:-1]

#Nastaveni GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()

#Promenne
teplota = " "
vlhkost = " " 
temp_c = " "
currentMode = "inTemp"

#Nacteni teplomeru z 1Wire
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#Nacteni DHT11 a displeje
cidlo = dht11.DHT11(pin = 11)
displej = lcd()

displej.display_string("Nacitam data", 1)

#Cteni teploty z DHT11 a odeslani na soutezni server
def read_inside():
        data = cidlo.read()
	if data.is_valid():
		global teplota
		global vlhkost
		teplota = data.temperature
		vlhkost = data.humidity

		adresa = "https://ioe.zcu.cz/th.php?id=" + str(id) + "&temperature=" + str(teplota) + "&humidity=" + str(vlhkost)
				
		os.system('curl "' + adresa + '"') 
	else:
		read_inside()

#Cteni z 1Wire teplomeru
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
	global temp_c
        temp_c = float(temp_string) / 1000.0


while 1:
	read_inside()
	read_temp()
	if currentMode == "inTemp":
		displej.display_string("Vnitrni teplota", 1)
		displej.display_string("je " + str(teplota) + " C", 2)
		currentMode = "outTemp"
		time.sleep(5)
	
	elif currentMode == "outTemp":
		displej.display_string("Vnejsi teplota", 1)
		displej.display_string("je " + str(temp_c) + " C", 2)
		currentMode = "inHum"
		time.sleep(5)
		
	elif currentMode == "inHum":
		displej.display_string("Vnitrni vlhkost", 1)
		displej.display_string("je " + str(vlhkost) + " %", 2)
		currentMode = "inTemp"
		time.sleep(5)

