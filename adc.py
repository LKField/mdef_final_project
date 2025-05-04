from machine import ADC
from time import sleep

sensor = ADC(28)

while True:
        sensor_value = sensor.read_u16()   #reading analog pin
        print(sensor_value)                   #printing the ADC value
        sleep(0.25)