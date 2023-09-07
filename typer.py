import json
import datetime
import time
import sys

# Read values from config.json
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# Convert the values from config.json to integers
PROD_KEY = int(config_data.get("PROD_KEY", -1))
PROD_KEY_USER = int(config_data.get("PROD_KEY_USER", -1))

def main_code():
    print("EMERGENCY STOP ---->  Press the 'Esc' key to stop typing...\n")
    text_to_type = input("Paste your text: ")

    # Input validation for typing speed
    while True:
        try:
            typing_speed_wpm = int(input("How much typing speed do you want? "))
            if typing_speed_wpm > 0:
                break
            else:
                print("Please enter a positive integer for typing speed. \n")
        except ValueError:
            print("Invalid input. Please enter a valid integer for typing speed. \n")

    delay = int(input("Enter after how many seconds typing should start: "))
    time.sleep(delay)

    # Rest of your main code here

# Check if PROD_KEY is -1
if PROD_KEY == -1:
    user_key = str(input("Enter PRODUCT KEY: "))
    # Your code here to validate user_key if needed
    current_time_minutes = datetime.datetime.now().minute

    # Check if the user_key matches the current time in minutes
    if user_key == str(current_time_minutes):
        # Generate PROD_KEY and PROD_KEY_USER
        PROD_KEY = int(user_key) + int(user_key) + 5
        PROD_KEY_USER = int(user_key) + int(user_key) + 15
        # Update values in config.json
        config_data["PROD_KEY"] = str(PROD_KEY)
        config_data["PROD_KEY_USER"] = str(PROD_KEY_USER)
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)
        print("Access granted!")
        # Call the main code function
        # main_code()
    else:
        print("Access denied. Exiting program.")
        config_data["PROD_KEY"] = "-1"
        config_data["PROD_KEY_USER"] = "-1"
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)
        sys.exit(1)  # Exit the program with a non-zero status code
else:
    # Check if PROD_KEY - 5 is equal to PROD_KEY_USER - 15
    if (PROD_KEY-5) == (PROD_KEY_USER-15):
        print("Access granted!")
        # Call the main code function
        # main_code()
    else:
        print("Access denied. Exiting program.")
        # Update values in config.json
        config_data["PROD_KEY"] = "-1"
        config_data["PROD_KEY_USER"] = "-1"
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)
        sys.exit(1)  # Exit the program with a non-zero status code

######################################
# MAIN LOGIN
#####################################
import time
import pyautogui
import keyboard  
import threading
# Variable to control whether typing should continue
typing_continues = True

# Function to type text at a given WPM rate
def type_text_slowly(text, wpm):
    global typing_continues  # Declare that we're using the global variable
    words = text.split()
    seconds_per_word = 60 / wpm  # Calculate seconds per word

    for word in words:
        pyautogui.typewrite(word)
        pyautogui.press('space')
        time.sleep(seconds_per_word)

        # Check if the user pressed the "Esc" key
        if not typing_continues:
            break

print("EMERGENCY STOP ---->  Press the 'Esc' key to stop typing...\n")
text_to_type = input("Paste your text: ")

# Input validation for typing speed
while True:
    try:
        typing_speed_wpm = int(input("How much typing speed you want? "))
        if typing_speed_wpm > 0:
            break
        else:
            print("Please enter a positive integer for typing speed. \n")
    except ValueError:
        print("Invalid input. Please enter a valid integer for typing speed. \n")

delay = int(input("Enter after how many seconds typing should start: "))
time.sleep(delay)


# Start typing slowly in a separate thread
typing_thread = threading.Thread(target=type_text_slowly, args=(text_to_type, typing_speed_wpm))
typing_thread.start()

# Listen for the "Esc" key press
keyboard.add_hotkey('esc', lambda: stop_typing(), suppress=True)

# Function to stop typing when the "Esc" key is pressed
def stop_typing():
    global typing_continues
    typing_continues = False
    typing_thread.join()
    print("\nTyping stopped.")

# Wait for the typing thread to finish
typing_thread.join()
