import cv2
import mss
import numpy as np
import time
from pynput import keyboard


class KeyListener:
    def __init__(self):
        self.keys = ["W", "A", "S", "D"]
        self.key_vector = [0, 0, 0, 0]
        self.listener = keyboard.Listener(on_press=self.press, on_release=self.release)
        self.listener.start()

    def press(self, key):
        if hasattr(key, 'char') and key.char in self.keys:
            self.key_vector[self.keys.index(key.char)] = 1

    def release(self, key):
        if hasattr(key, 'char') and key.char in self.keys:
            self.key_vector[self.keys.index(key.char)] = 0

    def get_keys(self):
        return self.key_vector


key_listener = KeyListener()


def capture_img():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = cv2.resize(cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGR2GRAY), (160, 256))
        return img


def running():
    global run
    run = not run
    print("False" if not run else "True")


hotkey_listener = keyboard.GlobalHotKeys({'<ctrl>+<shift>+o': running})
hotkey_listener.start()
run = False


while run:
    img = capture_img()
    keys = key_listener.get_keys()

    time.sleep(0.1)


