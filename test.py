import pyautogui


_cor = pyautogui.locateOnScreen('complete.png', confidence=0.35, grayscale=True)
x,y = pyautogui.center(_cor)


print(_cor)