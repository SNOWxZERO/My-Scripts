import pyautogui as pyautogui
import webbrowser
import time
import os

Error404 = [True for i in range(200)]


def CHK_LOST():
    lost = []
    path = os.getcwd()
    for i in range(1, 201):
        if f'a68d8ad8-2b0d-4193-a6b0-2d3804339d44_{i}.pdf' in os.listdir(path):
            continue
        Error404[i - 1] = False
        lost.append(i)
    return lost


def Dwnld_LOST(lost):
    for i in range(len(lost)):
        webbrowser.open(
            f"https://dorar.uqu.edu.sa/Dspace/pdf/a68d8ad8-2b0d-4193-a6b0-2d3804339d44/a68d8ad8-2b0d-4193-a6b0-2d3804339d44_{lost[i]}.pdf")
    input()
    webbrowser.open('https://www.google.com.eg/')
    for _ in range(len(lost)):
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'w')


lost = CHK_LOST()
print(len(lost))
print(lost)
Dwnld_LOST(lost)
