from PIL import ImageGrab
import cv2
import numpy as np
import time
def screen_capture():
	last_time=time.time()
	while(True):
		capture_screen=np.array(ImageGrab.grab(bbox=(100,100,740,580)))
		print('heres our {} fps '.format(time.time()-last_time))
		last_time=time.time()
		cv2.imshow('wondow',cv2.cvtColor(capture_screen,cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
screen_capture()