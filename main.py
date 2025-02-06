import cv2
import mss
import numpy as np
import time
from pynput import keyboard


class KeyListener:
    def __init__(self):
        self.keys = ["W", "A", "S", "D", "R"]
        self.key_vector = [0, 0, 0, 0, 0]
        self.listener = keyboard.Listener(on_press=self.press, on_release=self.release)
        self.listener.start()

    def press(self, key):
        if hasattr(key, 'char') and key.char.upper() in self.keys:
            self.key_vector[self.keys.index(key.char.upper())] = 1

    def release(self, key):
        if hasattr(key, 'char') and key.char.upper() in self.keys:
            self.key_vector[self.keys.index(key.char.upper())] = 0

    def get_keys(self):
        return self.key_vector

    def reset_keys(self):
        self.key_vector = [0, 0, 0, 0, 0]


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

images = []
key_states = []
while True:
    if run:
        img = capture_img()
        keys = key_listener.get_keys()
        images.append(img)
        key_states.append(keys)
        if keys[4] == 1:
            name = f"episodes/ep_{str(time.time())}"
            np.savez(name + ".npz",
                     frames=np.array(images, dtype=np.uint8),
                     keys=np.array(key_states, dtype=np.uint8))
            print(name + " saved!")
            key_listener.reset_keys()
    time.sleep(0.01)