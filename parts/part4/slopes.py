import cv2
import numpy as np
import time
from grabScreen import grab_screen
from direct_key_inputs import PressKey, ReleaseKey, W, A, S, D
countW=0
triggered=0
def forward():
	global countW,triggered
	countW+=1
	if countW>=15 or triggered==1:
		if countW==0:
			triggered=0
		countW-=1
	elif triggered==0:
		PressKey(W)
def right():
	PressKey(D)
	PressKey(W)
	time.sleep(0.5)
	ReleaseKey(W)
	ReleaseKey(D)
	time.sleep(0.5)
def left():
	PressKey(A)
	PressKey(W)
	time.sleep(1)
	ReleaseKey(W)
	ReleaseKey(A)
	time.sleep(1)
def process_roi_lanes(img,lines):
	try:
		for line in lines:
			coords = line[0]
			cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],3)
			if (coords[0]<=180 and coords[1]>=350) or (coords[0]>=460 and coords[1]>=350):
				cv2.circle(img,(coords[0],coords[1]),10,(255,0,255),2)
				return coords[0],coords[1]
	except:
		pass
def roi(img,vertices):
	#blank mask
	mask = np.zeros_like(img)
	#fill the mask
	cv2.fillPoly(mask, vertices, 100)
	masked = cv2.bitwise_and(img, mask)
	return masked
def image_processing(origional_img):
	#processed_img_1= cv2.imshow('wondow',origional_img)
	processed_img =cv2.Canny(cv2.cvtColor(origional_img,cv2.COLOR_BGR2RGB), threshold1=50,threshold2=300)
	vertices = np.array([[1,480],[1,280],[100,225],[540,225],[640,280],[640,470]], np.int32)
	#processing the edges
	processed_img=roi(processed_img, [vertices])
	#draw lines and hough transform
	lines=cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]),55,45)
	try:
		cordx,cordy = process_roi_lanes(processed_img,lines)
	except:
		cordx=0
		cordy=0
	return processed_img , cordx, cordy
def key_deside(cordx):
	if cordx<=40 or cordx>=590:
		forward()
	if cordx>=40 and cordx<=350:
		print("right")
		time.sleep(1)
		ReleaseKey(W)
		time.sleep(1)
		right()
	if cordx<=620 and cordx>=350 :
		time.sleep(1)
		ReleaseKey(W)
		time.sleep(1)
		left()
		print("left")
def screen_capture():
	check_lane=0
	last_time=time.time()
	while(True):
		capture_screen, image_1=grab_screen(region=(100,100,740,580))
		#find edges
		if check_lane==0:
			edges, cordx, cordy = image_processing(image_1)
		print('heres our {} fps '.format(1/(time.time()-last_time)))
		last_time=time.time()
		key_deside(cordx)
		cv2.imshow("window",edges)
		#cv2.imshow('wondow',cv2.cvtColor(capture_screen,cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
screen_capture()