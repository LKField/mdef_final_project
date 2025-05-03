""" language button changer for mending laptop - will be used in the main playback loop to change the language

pseudocode:
import Debouncer
LANGUAGE_PIN = ?
lang_pressed = false
english = true

lang_pressed = Debouncer(LANGUAGE_PIN)

if lang_pressed && english:
    english = false
    lang_pressed = false // is this necessary with Debouncer?
elif lang_pressed && not enlgish:
    english = true
    lang_pressed = false // is this necessary with Debouncer?
"""
from debouncer import Debouncer

button = Debouncer(4)
english = True


while True:
    
    if button.duration > 0.1:
        button.duration = 0
        if english:
            print("Languge: English")
            english = False
        
        elif not english:
            print("Language: Not English")
            english = True
