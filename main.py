import pyautogui
import time
import logging

logging.basicConfig(level=logging.INFO)


def click_button(filename, sleep=2, clear=True, grayscale=False, post_fun=None, args=None):
    logging.info('click %s' % filename)
    global timer
    factor = 1440 / 2880
    _cor = pyautogui.locateOnScreen(filename, confidence=0.9, grayscale=True)

    if _cor is None:
        return False
    x, y = pyautogui.center(_cor)
    x = x * factor
    y = y * factor
    pyautogui.click(x, y)
    if clear:
        timer = 0
    time.sleep(sleep)
    if post_fun is not None:
        post_fun(args)


def wait_for(filename):
    counter = 0
    while True:
        counter += 5
        if counter > 20:
            break
        _cor = pyautogui.locateOnScreen(filename, confidence=0.8)
        if _cor is not None:
            return True
        else:
            time.sleep(5)


def _exit():
    click_button('setting_button.png', sleep=1)
    ret = click_button('exit.png')
    if ret is False:
        _exit()


click_button('icon.png')

timer = 0
count = 0
while True:
    count += 1
    logging.info('loop %d' % count)
    click_button('start_button.png', post_fun=wait_for, args='initial.png')
    click_button('confirm_button.png')

    cor2 = pyautogui.locateOnScreen('complete.png', confidence=0.8, grayscale=True)
    cor3 = pyautogui.locateOnScreen('continue_button.png', confidence=0.8)
    if cor3 is not None:
        if cor2 is not None:
            break
        else:
            click_button('continue_button.png')

    cor = pyautogui.locateOnScreen('finish.png', confidence=0.8, grayscale=True)
    cor1 = pyautogui.locateOnScreen('confirm_button.png', confidence=0.8, grayscale=True)
    if (cor is not None) and (cor1 is None) and timer >= 10:
        click_button('setting_button.png', sleep=1)
        click_button('concept_button.png')
    time.sleep(5)
    timer += 5
    pyautogui.click()

_exit()
