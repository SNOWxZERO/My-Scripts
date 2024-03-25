import pyautogui
import keyboard
import time

language_En = 1

while True:

    if language_En == 1 :
        if keyboard.is_pressed('q+u'):
            pyautogui.press('left')
            pyautogui.press('backspace')
            pyautogui.press('right')
        if keyboard.is_pressed('n'):
            pyautogui.press('right')
            pyautogui.press('backspace')
    else:
        if keyboard.is_pressed('q+u'):
            pyautogui.press('right')
            pyautogui.press('backspace')
            pyautogui.press('left')
        if keyboard.is_pressed('n'):
            pyautogui.press('left')
            pyautogui.press('backspace')


