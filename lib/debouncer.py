"""debouncer.py uses the PIO and interrupts to read button

Using a statemachine,

- Button pin defined at top of file. Default but_pin = GPIO 21

debouncer.py contains the Debouncer, DebouncerLowPIO, and DebouncerHighPIO
classes which handle the button.

debouncer.py is based on code by benevpi available at the following
link. The class has been modified by Lucretia Field
Source: https://github.com/benevpi/DebouncerPIO
"""
from machine import Pin
import rp2
import time 

try:        # AttributeError under sphinx when machine package not available
    # Define button
    but_pin = 21
    pressed = False
except AttributeError:
    but_pin = []
    pressed = False

try:        # AttributeError under sphinx when machine package not available
    @rp2.asm_pio()
    def debounce_low():
        wait(0, pin, 0)

        set(y,7)
        label("loop")
        jmp(y_dec, "loop") [10]
        jmp(pin, "skip")

        set(y,7)
        label("loop2")
        jmp(y_dec, "loop2") [10]
        jmp(pin, "skip")

        set(y,7)
        label("loop3")
        jmp(y_dec, "loop3") [10]
        jmp(pin, "skip")

        irq(block, rel(0))
        wait(1, pin, 0)
        label("skip") #no idea why this isn't triggering the not-wrapping bug that debounce-high is
        set(y,1) # just a test -- doesn't work if removed. looks like it's not wrapping
except AttributeError:
    def debounce_low():
        pass

try:        # AttributeError under sphinx when machine package not available
    @rp2.asm_pio()
    def debounce_high():
        wait(1, pin, 0)

        set(y,7)

        label("loophigh")
        jmp(y_dec, "loophigh") [10]

        in_(pins,1)
        mov(y, isr)
        jmp(not_y, "skiphigh")

        set(y,7)

        label("loophigh2")
        jmp(y_dec, "loophigh2") [10]

        in_(pins,1)
        mov(y, isr)
        jmp(not_y, "skiphigh")

        irq(block, rel(0))

        wait(0, pin, 0)
        label("skiphigh")
        set(y,1) # just a test -- doesn't work if removed. looks like it's not wrapping
except AttributeError:
    def debounce_high():
        pass

class DebouncerLowPIO:
    """DebouncerLowPIO

    :param statemachine:
    :param but_pin:
    :param handler:
    """
    def __init__(self, statemachine, but_pin, handler):
        self.sm  = rp2.StateMachine(statemachine, debounce_low, in_base=self.pin, jmp_pin=self.pin, freq=4000)
        self.sm.irq(handler)
        self.sm.active(1)
    
    def stop(self):
        self.sm.active(0)
        
    def start(self):
        self.sm.active(1)
        
class DebouncerHighPIO:
    """DebouncerHighPIO

    :param statemachine:
    :param but_pin:
    :param handler:
    """
    def __init__(self, statemachine, but_pin, handler):
        self.sm  = rp2.StateMachine(statemachine, debounce_high, in_base=self.pin, freq=3000)
        self.sm.irq(handler)
        self.sm.active(1)
        
    def stop(self):
        self.sm.active(0)
        
    def start(self):
        self.sm.active(1)
        
class Debouncer:
    """Decouncer class handles

    Sets up two state machines, smA and smB, to debounce the high and low signals.

    CHECK Program, is it unnecessary?

    :param statemachine: State machine number for instance
    """
    def __init__(self, statemachine):
        self.pin = Pin(but_pin, Pin.IN, Pin.PULL_UP)
        self.pressed = pressed
        self.setup = False
        self.press_time = 0
        self.duration = 0
        self.smA = rp2.StateMachine(statemachine, debounce_low, in_base=self.pin, jmp_pin=self.pin, freq=4000)
        self.smB = rp2.StateMachine((statemachine + 1), debounce_high, in_base=self.pin, freq=3000)
        self.smA.active(1)
        self.smA.irq(self.handler_press)
        self.smB.irq(self.handler_release)
        
    def handler_press(self, sm):
        """handler_press sets the press_time when pressed

        Activates the smB state machine when pressed. Sets the pressed flag to True.

        :param sm: State machine instance
        :return: None
        """
        print("Pressed")
        self.pressed = True
        self.duration = 0
        self.press_time = time.ticks_us()
        self.smB.active(1)
        
    def handler_release(self, sm):
        """handler_release sets the pressed duration when released

        The duration is calculated as the difference between the current time and the press_time in seconds.
        Sets the pressed flag to False when button is released.

        :param sm: State machine instance
        :return: None
        """
        print("Released")
        self.duration = time.ticks_diff(time.ticks_us(), self.press_time)/1000000
        self.pressed = False
        print("Duration:", self.duration)
        
        
if __name__ == "__main__":
    button = Debouncer(4)
