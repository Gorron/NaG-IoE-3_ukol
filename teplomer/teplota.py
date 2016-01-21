import RPi.GPIO as GPIO
import dht11
import time
import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()

cidlo = dht11.DHT11(pin = 7)

while (1):
	data = cidlo.read()
	if data.is_valid():
		print("Posledni validni vstup:" + str(datetime.datetime.now()))
		print("Teplota je: %d C " % data.temperature)
		print("Vlhkost je: %d %%" % data.humidity)
	time.sleep(1)
