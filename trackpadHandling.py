"""trackpadHandling.py creates a class Story with functions for handling the trackpad touch reactions


"""

from machine import ADC, Pin
from time import sleep

class Story:
    """This class sets up the structure and functions for the stories in the 'mended laptop' project 

    :param name: Name of new story object (name of the teller)
    :type name: string
    :param led_pin: GPIO pin for the associated LED
    :type led_pin: int
    :param adc_pin: GPIO pin for the associated ADC
    :type adc_pin: int
    :param en_path: Path to the associated English audio file
    :type en_path: string
    :param non_path: Path to the associated not English audio file
    :type non_path: string
    :param voltage: Voltage reading from ADC, default 0  
    :type voltage: int 
    
    """
    
    entries_lst = []
    voltages_lst = []
    
    def __init__(self, name, led_pin, adc_pin, en_path, non_path, voltage=0):
        """Constructor method

        Initialized the instance of the class:
        - intializes the passed parameters 
        - appends it to the entries list
        - appends the voltages to the voltages list
        - instantiates the LED pin as an output pin 
        
        """
        self.name = name					# name of the associated Story information (person's name)
        self.led_pin = led_pin				# LED pin
        self.adc_pin = adc_pin				# ADC pin
        self.en_path = en_path				# path to the English audio file 
        self.non_path = non_path			# path to the Non-English audio file 
        self.voltage = voltage				# voltage
        
        self.led = Pin(led_pin, Pin.OUT)	# initialize the LED Pin
        self.sensor = ADC(adc_pin)			# initialize the ADC Pin

        self.entries_lst.append(self)			# append the new object to the entries list
        self.voltages_lst.append(voltage)		# append the voltage to the voltages list 
    
    def __str__(self):
        return f"{self.name}, Index: {self.index}, LED: {self.led_pin}, ADC: {self.adc_pin}, {self.en_path}, {self.non_path}, Voltage: {self.voltage}"
        
        
    @classmethod   
    def updateVoltage(cls, index, voltage):
        """class method to update the voltages in the voltages_lst list

        :param index: index of in the voltages_lst to update
        :type index: int
        :param voltage: the value to update into the voltages_lst
        :type voltage: int
        
        :return: voltages_lst (list of voltages)
        :rtype: list of ints 
        """
        cls.voltages_lst[index] = voltage
        return cls.voltages_lst
       
    @classmethod   
    def findMax(cls):
        """Find the maximum value from the passed list and returns the index and value
        
        :return: ind (index of maximum), m (value of maximum)
        :rtype: ind (int), m (int) 
        """
        m = max(cls.voltages_lst)
        ind = cls.voltages_lst.index(m)
        print(f"Index of Max: {ind}, Value of Max: {m}")
        return ind, m

    def ledOn(self):
        """Toggles the LED to On"""
        print("LED on")
        self.led.value(1)
        
    def ledOff(self):
        """Toggles the LED to Off"""
        print("LED off")
        self.led.value(0)
        
    def playAudio(self):
        # Add audio playing code for the path passed
        pass
        
        
        
 
if __name__ == "__main__":
    story1 = Story("Vitti", 25, 28, "audio/vitti/en.wav", "audio/vitti/non.wav", 0)
    story2 = Story("Denisa", 25, 27, "audio/denisa/en.wav", "audio/denisa/non.wav", 0)
    
#    print(Story.entries_lst)
#    print(Story.voltages_lst)
    
    while True: 
        # Read the ADC and update voltages (Will need to be replaced with SPI code for 8 channel ADC) 
        for i in range(len(Story.entries_lst)):
            voltages = Story.updateVoltage(i, Story.entries_lst[i].sensor.read_u16())
            
        # Find the maximum ADC value 
        ind, max_value = Story.findMax()

        
        # Turn on and off the LED of the maximum - for now set to the onboard LED 
        Story.entries_lst[ind].ledOn()
        sleep(2)
        Story.entries_lst[ind].ledOff()
        sleep(2)
        
        

            
            


        
