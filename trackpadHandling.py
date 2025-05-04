"""trackpadHandling.py creates a class with functions for handling the trackpad touch reactions

pseudocode for ADC readings

From https://github.com/romilly/pico-code/blob/master/src/pico_code/pico/mcp3008/mcp3008-demo.py

from time import sleep
from mcp3008 import MCP3008
from machine import Pin

spi = machine.SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=100000)
cs = machine.Pin(22, machine.Pin.OUT)


chip = MCP3008(spi, cs)

while True:
    print(chip.read(0))
    sleep(1)

"""

from machine import ADC, Pin
from time import sleep

sensors = []
sensor1 = ADC(28)
sensor2 = ADC(27)

sensors.append(sensor1)
sensors.append(sensor2)

class Trackpad:
    entries = []
    voltages = []
    def __init__(self, name, index, led_pin, en_path, non_path, voltage):
        self.name = name    				# name of the associated trackpad information (person's name)
        self.index = index					# the index of the objext so that it can be called sequentially 
        self.led_pin = led_pin				# LED pin 
        self.en_path = en_path				# path to the English audio file 
        self.non_path = non_path			# path to the Non-English audio file 
        self.voltage = voltage 				# voltage
        Trackpad.entries.append(self)		# append the new object to the entries list 
        Trackpad.voltages.append(voltage)	# append the voltage to the voltages list 
        self.led = Pin(led_pin, Pin.OUT)	# initialize the LED Pin 
        
    def __str__(self):
        return f"{self.name}, Index: {self.index}, LED: {self.led_pin}, {self.en_path}, {self.non_path}, Voltage: {self.voltage}"
 
    def updateVoltage(index, voltage):
        Trackpad.voltages[index] = voltage
        return Trackpad.voltages
        
    def findMax(voltages):
        m = max(voltages)
        ind = voltages.index(m)
        print(f"Index of Max: {ind}, Value of Max: {m}")
        return ind, m

    def ledOn(self):
        print("LED on")
        self.led.value(1)
        
    def ledOff(self):
        print("LED off")
        self.led.value(0)
        
    def playAudio(path):
        # Add audio playing code for the path passed
        pass
        
        
        
 
if __name__ == "__main__":
    story1 = Trackpad("Vitti", 0, 25, "audio/vitti/en", "audio/vitti/non", 0)
    story2 = Trackpad("Denisa", 1, 25, "audio/denisa/en", "audio/denisa/non", 0)

    # Read the ADC and update voltages (Will need to be replaced with SPI code for 8 channel ADC) 
    for i in range(len(Trackpad.entries)):
        voltages = Trackpad.updateVoltage(i, sensors[i].read_u16())

    # Find the maximum ADC value 
    ind, m = Trackpad.findMax(voltages)

    
    # Turn on and off the LED of the maximum - for now set to the onboard LED 
    Trackpad.entries[ind].ledOn()
    sleep(2)
    Trackpad.entries[ind].ledOff()

        
        


    