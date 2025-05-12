"""pseudocode for the overall structure of the mending laptop

"""
from machine import Pin, ADC
from picodfplayer import DFPlayer
from mcp3008 import MCP3008
from debouncer import Debouncer
# from myClass import MyClass

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

# ------------- setup the button -------------
sm = 4    # constant - set the statemachine 

# create the button Debouncer instance 
button = Debouncer(sm)

# ------------- setup the DFPlayer -------------
# constants - set the DFPlayer pins
UART_INSTANCE = 1
TX_PIN = 4
RX_PIN = 5
BUSY_PIN = 6

# create player instance
player = DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

# ------------- setup the volume control -------------
VOL_PIN = 26    # constant - set the volume pin
vol_sensor = ADC(VOL_PIN)

# ------------- setup the stories -------------
# create the story instances
# TODO: create the class to actually handle this 


# Debounce the button function - Where can this be included? Somewhere other than here? 
def language_toggle(english):
    if button.duration > 0.075:
        button.duration = 0
        if english:
            print("Language: English")
            english = False
        
        else:
            print("Language: Not English")
            english = True
            
    return english

english = True


# THE MAIN LOOP! 
while True: 
    for story in Stories:
        Stories.voltages(story) = chip.read(story.adc_ch)	# updates the voltage of the given story from the set ADC channel
        
    max_story, max_value = Stories.findMax(Stories.voltages)# find the story and max voltage from Stories.voltages (Need to rewrite function)

    if max_value < threshold:								# below the treshold, go back and look again 
        # Go back to loop to check the trackpad ADCs 
        pass 
    else:													# above threshold, do a bunch of stuff 
        max_story.ledOn()									# turn associated LED on 
        player.playTrack(max_story.en)						# start the associated english file playback
        
        while player.queryBusy():							# while the playback is happening 
            english = language_toggle(english)				# check the button is pressed and return toggle 
            if not english:
                player.playTrack(max_story.non)				# if toggle is not enlgish play non-english 
            else:
                player.playTrack(max_story.en)				# if toggle is english play english
                
            # ALSO: read the volume ADC input (need to prototype the hardware)
            volume = vol_sensor.read_u16()					#reading analog pin
            player.setVolume(volume)
            
        max_story.ledOff()									# at end of audio - turn associated LED off
        # loop back to checking trackpad ADCs 
