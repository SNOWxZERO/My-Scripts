import keyboard
import time

count = 0

def on_key_release(event):
    global count
    if event.name == '0':
        count += 1
        print('\r' + str(count), end='')

keyboard.on_release(on_key_release)

try:
    while True:
        time.sleep(1)  # Let the program run indefinitely
except KeyboardInterrupt:
    keyboard.unhook_all()  # Clean up