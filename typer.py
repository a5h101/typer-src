import keyboard
import threading
import pyautogui
import json
import datetime
import time
import sys
import os

# Read values from config.json
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# Convert the values from config.json to integers
PROD_KEY = int(config_data.get("PROD_KEY", -1))
PROD_KEY_USER = int(config_data.get("PROD_KEY_USER", -1))
USER = str(config_data.get("USER", -1))

home_directory = os.path.expanduser("~")
subdirectories = [d for d in os.listdir(
    home_directory) if os.path.isdir(os.path.join(home_directory, d))]
if subdirectories:
    # Get the name of the first subdirectory
    first_subdirectory = subdirectories[0]
else:
    first_subdirectory = "empty"

if PROD_KEY == -1:
    user_key = str(input("Enter PRODUCT KEY: "))
    # Your code here to validate user_key if needed
    current_time_minutes = datetime.datetime.now().minute

    # Check if the user_key matches the current time in minutes
    if user_key == str(current_time_minutes):
        # Generate PROD_KEY and PROD_KEY_USER
        PROD_KEY = int(user_key) + int(user_key) + 17
        PROD_KEY_USER = int(user_key) + int(user_key) + 33
        USER = home_directory+first_subdirectory
        # Update values in config.json
        config_data["PROD_KEY"] = str(PROD_KEY)
        config_data["PROD_KEY_USER"] = str(PROD_KEY_USER)
        config_data["USER"] = str(USER)
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)
        print("-----------------> Access granted! <----------------- \n")
        print("-----------------> Press Ctrl+C to exit Typer <----------------- \n")
        print("-----------------> Press ESC to exit while Typing <----------------- \n")
    else:
        print("Access denied. Exiting program.")
        config_data["PROD_KEY"] = "-1"
        config_data["PROD_KEY_USER"] = "-1"
        config_data["USER"] = "-1"

        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)
        sys.exit(1)  # Exit the program with a non-zero status code
else:
    if (PROD_KEY-17) == PROD_KEY_USER-33 and home_directory+first_subdirectory == str(USER):
        print("-----------------> Access granted! <----------------- \n")
        print("-----------------> Press Ctrl+C to exit Typer <----------------- \n")
        print("-----------------> Press ESC to exit while Typing <----------------- \n")
        print("Paste the text you want to type in txt.txt, If you want to pause the typing just include '~' in the text file. Then press the Shif key to continue. For line change add '`' wherever you want to change the line")
        print("\n")
        print("<------------------------------------------------------------------>")
        print("\n")

    else:
        print("Access denied. Exiting program. Reopen any try again")
        config_data["PROD_KEY"] = "-1"
        config_data["PROD_KEY_USER"] = "-1"
        config_data["USER"] = "-1"

        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)
        sys.exit(1)  # Exit the program with a non-zero status code

######################################
# AFTER LOGIN
#####################################

typing_continues = True  # Initialize the typing_continues variable

def wait_for_shift():
    while True:
       keyboard.wait('shift')
       break

def type_text_fast(text, wpm):
    global typing_continues
    words = text.split()
    seconds_per_word = 60 / wpm

    for word in words:
        if word == "~":
            # print(word)
            wait_for_shift()
            continue
        for char in word:
            if not typing_continues:
                return
            if char =="`":
             pyautogui.press('enter')  
             continue
            pyautogui.typewrite(char)
            time.sleep(seconds_per_word / len(word) / 10)
        pyautogui.press('space')

def start_typing(text, wpm):
    global typing_continues
    typing_continues = True
    typing_thread = threading.Thread(target=type_text_fast, args=(text, wpm))
    typing_thread.start()
    typing_thread.join()

def stop_program():
    global typing_continues
    typing_continues = False

# Listen for the "Esc" key press to exit the program
keyboard.add_hotkey('esc', lambda: stop_program(), suppress=True)

while typing_continues:
    try:
        typing_speed_wpm = int(input("Typing speed? 100 is default, press any key to skip:"))
    except ValueError:
        typing_speed_wpm = 100
    try:
        mode = int(input("Enter 1 for auto formatting or press any key to continue: "))
    except ValueError:
        mode = 0
    
    with open("txt.txt", "r") as text_file:
        text_to_type = text_file.read()
        if(mode == 1):
            text_to_type = text_to_type.replace("\n", "`\n")

    print("Press '-----------------> 'Shift' key to start typing... <-----------------\n")
    keyboard.wait('shift')
    start_typing(text_to_type, typing_speed_wpm)

print("Exiting the program.")
