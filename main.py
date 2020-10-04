import pyautogui
import time
import logging
import argparse

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S')

parser = argparse.ArgumentParser(description='autohs')
parser.add_argument("-e", action="store_true", default=False)
args = parser.parse_args()
# vars
timer = 0
count = 0

flag = True
if args.e is True:
    flag = False

# factor = 1440 / 2880
factor = 1920 / 3840
# factor = 1
pre_path = 'resources/3840/'
cache_list = ['setting_button.png', 'concept_button.png']


def check_button(filename):
    _cor = pyautogui.locateOnScreen(
        pre_path + filename, confidence=0.9, grayscale=True)
    return _cor


cache = {}


def click_button(filename, sleep=2, clear=True, post_fun=None, args=None):
    global cache
    logging.info('click %s' % filename)
    global timer

    if filename in cache.keys():
        x, y = cache[filename]
        logging.info('cache hit')
    else:
        _cor = check_button(filename)
        if _cor is None:
            return False
        x, y = pyautogui.center(_cor)
        x = x * factor
        y = y * factor
        if filename in cache_list:
            cache[filename] = (x, y)
    pyautogui.click(x, y)
    if clear:
        timer = 0
    time.sleep(sleep)
    if post_fun is not None:
        return post_fun(args)


def wait_for(filename):
    counter = 0
    while True:
        counter += 3
        if counter > 60:
            break
        _cor = check_button(filename)
        time.sleep(3)
        if _cor is not None:
            return True


def _exit():
    click_button('setting_button.png', sleep=1)
    ret = click_button('exit.png')
    if ret is False:
        _exit()


click_button('icon.png')

while True:
    count += 1
    # step 1
    logging.info('loop %d' % count)
    click_button('start_button.png', post_fun=wait_for, args='initial.png')
    click_button('confirm_button.png')
    # step 2

    cor3 = check_button('continue_button.png')
    if cor3 is not None:
        if flag:
            cor2 = check_button('complete.png')
            if cor2 is not None:
                break
        click_button('continue_button.png')
    pyautogui.click()
    # step 3
    cor = check_button('finish.png')
    if cor is not None:
        click_button('setting_button.png', sleep=1)
        click_button('concept_button.png')
    time.sleep(5)
    timer += 5

_exit()
