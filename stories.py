"""stories.py creates a class Stories with functions for handling the trackpad touch reactions


"""
from machine import ADC, Pin
from mcp3008 import MCP3008
from picodfplayer import DFPlayer
from debouncer import Debouncer
from time import sleep

# ------------- setup the MCP3008 -------------
# constants - set the MCP3008 pins
SCK_PIN = Pin(18)
MOSI_PIN = Pin(19)
MISO_PIN = Pin(16)
CS_PIN = Pin(17, Pin.OUT)

spi = machine.SPI(0, sck=SCK_PIN, mosi=MOSI_PIN, miso=MISO_PIN, baudrate=100000)
cs = CS_PIN

# create the MCP3008 instance 
chip = MCP3008(spi, cs)

# create threshold for 'press'
THRESHOLD = 500

# ------------- setup the DFPlayer -------------
# constants - set the DFPlayer pins
UART_INSTANCE = 1
TX_PIN = 4
RX_PIN = 5
BUSY_PIN = 6

# create player instance
player = DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

# ------------- setup the button -------------
# create the button Debouncer instance 
button = Debouncer(4)

class Stories: 
    """This class sets up the structure and functions for Stories

    :param name: Name of the new story object (name of the speaker)\
    :type name: string 
    :param led_pin: GPIO pin for the associated LED 
    :type led_pin: int 
    :param adc_ch: Channel for the associated ADC channel on MCP3008
    :type adc_ch: int 
    :param folder: Folder index (from 1 not 0) for audio files 
    :type folder: int 
    :param other_audio: Flag for secondary audio file, default False
    :type other_audio: bool
    :param voltage: Voltage reading to be updated from ADC, default 0 
    :type voltage: int

    """
    stories_lst = []                    # create a list of the stories
    voltages_lst = []                   # create a list of the voltages 


    def __init__(self, name, led_pin, adc_ch, folder, other_audio=False, voltage=0):
        """Constructor method

        Initialized the instance of the class:
        - initializes the passed parameters 
        - instantiates the LED pin as an output pin 
        
        """
        self.name = name					# name of the associated Story information (person's name)
        self.led_pin = led_pin				# LED pin
        self.adc_ch = adc_ch				# ADC channel
        self.folder = folder				# folder index (from 1 not 0) for audio files 
        self.other_audio = other_audio		# is there a Non-English audio file, default False 
        self.voltage = voltage				# voltage
        
        self.led = Pin(led_pin, Pin.OUT)	# initialize the LED Pin
 
        self.stories_lst.append(self)       # create a list of the created stories and append new
        self.index = len(self.stories_lst)  # create an index the length of the list of stories

        self.voltages_lst.append(voltage)		# append the voltage to the voltages list 
    
    def __str__(self):
        return f"{self.name}, LED: {self.led_pin}, ADC: {self.adc_ch}, {self.eng}, {self.non}, Voltage: {self.voltage}"
  
    
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
        
        :return: max_ind (index of maximum), max_value (value of maximum)
        :rtype: max_ind (int), max_value (int) 
        """
        max_value = max(cls.voltages_lst)
        max_ind = cls.voltages_lst.index(max_value)
        print(f"Index of Max: {max_ind}, Value of Max: {max_value}")
        return max_ind, max_value
    
    def ledOn(self):
        """Toggles the LED to On"""
        print("LED on")
        self.led.value(1)
        
    def ledOff(self):
        """Toggles the LED to Off"""
        print("LED off")
        self.led.value(0)
        
    def soundToggle(self):
        """Toggles the audio file

        TODO: actually make a toggle 
        """
#        pressed = False
        if self.other_audio:
            # Debounce the button function - Where can this be included? Somewhere other than here? 
            if button.duration > 0.075:
                button.duration = 0
                if pressed:
                    return 2
                else:
                    return 2
        else:
            return 1
        
    def playAudio(self):
        """Plays the audio from the file"""
        file = soundToggle()
        player.playTrack(self.folder,file)


if __name__ == "__main__":
    
    # ------------- setup the stories -------------
    # create the story instance
    stories = Stories("Vitti", "LED", 0, 1, True, 0) # For Pico W use "LED" for onboard LED
    stories = Stories("Denisa", 25, 1, "audio/denisa/en.wav", "audio/denisa/non.wav", 0) # for Pico use 25 for onboard LED 


    while True:    
        for i, story in enumerate(Stories.stories_lst):
    #        print(i, story)
            Stories.updateVoltage(i, chip.read(story.adc_ch))
            
        max_index, max_value = Stories.findMax()# find the story and max voltage from Stories.voltages (Need to rewrite function)
    #    print(max_story, max_value)
        max_story = Stories.stories_lst[max_index] #TODO Clean this up! 

        if max_value < THRESHOLD:	# below the treshold, go back and look again 
            # Go back to loop to check the trackpad ADCs 
            pass 
        else:
            max_story.ledOn()
#            print(Stories.stories_lst[max_story])
#            print(max_story, max_value)
            
            player.playTrack(max_story.folder,1)						# start the associated english file playback
            
#            while player.queryBusy():	
            
        sleep(1)