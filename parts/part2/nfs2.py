import cv2
import numpy as np
import time
from grabScreen import grab_screen
from direct_key_inputs import PressKey, ReleaseKey, W, A, S, D

def forward():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
def screen_capture():
    last_time=time.time()
    while(True):
        capture_screen=grab_screen(region=(100,100,740,580))
        forward()
        ReleaseKey(W)
        print('heres our {} time '.format(time.time()-last_time))
        last_time=time.time()
        cv2.imshow('wondow',cv2.cvtColor(capture_screen,cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25)&0xFF==('q'):
            cv2.destroyAllWindows()
            break

screen_capture()

