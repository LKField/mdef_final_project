"""languageButton.py uses the Debouncer class from debouncer.py and a language flag to change the language

This function reads the state of the 'language toggle' button which by default is GPIO 21 as defined in debouncer.py
Debouncer uses the PIO (state machine on the Pico) and interrupts to read button. To learn more about this class, check debouncer.py 

languageButton.py returns the desired language as: English (True) or Not English (False) and also prints a language flag

"""
from debouncer import Debouncer

button = Debouncer(4)
    
def language_toggle(english):

    if button.duration > 0.075:
        button.duration = 0
        if english:
            print("Languge: English")
            english = False
        
        else:
            print("Language: Not English")
            english = True
            
    return english

if __name__ == "__main__":
    english_toggle = True
    
    while True:
        english_toggle = language_toggle(english_toggle)
        
        