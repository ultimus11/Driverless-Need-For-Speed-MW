import cv2
import numpy as np
import time
from grabScreen import grab_screen
from direct_key_inputs import PressKey, ReleaseKey, W, A, S, D
def forward():
	PressKey(W)
	time.sleep(2)
	ReleaseKey(W)
	time.sleep(2)
def process_roi_lanes(img,lines,origional_img):
	try:
		for line in lines:
			coords = line[0]
			cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],3)
			if coords[0]<=180 and coords[1]>=400:
				cv2.circle(img,(coords[0],coords[1]),10,(255,0,255),2)
				#Creating initial window roi for lane tracking
				x, y, w, h = coords[0], coords[1], 30, 30 # simply hardcoded the values
				track_window = (x, y, w, h)
				# set up the ROI for tracking
				roi1 = origional_img[y:y+h, x:x+w]
				hsv_roi =  cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)
				mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
				roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
				cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
				# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
				term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
				return coords[0],coords[1],track_window,roi_hist,term_crit
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
		cordx,cordy,track_window,roi_hist,term_crit = process_roi_lanes(processed_img,lines,origional_img)
	except:
		cordx=0
		cordy=0
		track_window=0
		roi_hist=0
		term_crit=0
	return processed_img , cordx, cordy, track_window, roi_hist, term_crit
def Artificial_Sensors(image_1,cordx,cordy):
	#ok
	avg_b=0
	avg_g=0
	avg_r=0
	for x_cord in range(cordx-5,cordx+5):
		for y_cord in range(cordy-5,cordy+5):
			#print(x_cord)
			#print(y_cord)
			avg_b+=(image_1[y_cord,x_cord])[0]
			avg_g+=(image_1[y_cord,x_cord])[1]
			avg_r+=(image_1[y_cord,x_cord])[2]
	print(avg_b/100,avg_g/100,avg_r/100)
	return avg_b/100, avg_g/100, avg_r/100
def Artificial_Sensors_l1(image_1,cordx,cordy):
	#ok
	avg_b_l1=0
	avg_g_l1=0
	avg_r_l1=0
	for x_cord in range(cordx-5,cordx+5):
		for y_cord in range(cordy-5,cordy+5):
			#print(x_cord)
			#print(y_cord)
			avg_b_l1+=(image_1[y_cord,x_cord])[0]
			avg_g_l1+=(image_1[y_cord,x_cord])[1]
			avg_r_l1+=(image_1[y_cord,x_cord])[2]
	print(avg_b_l1/100,avg_g_l1/100,avg_r_l1/100)
	return avg_b_l1/100, avg_g_l1/100, avg_r_l1/100
def Artificial_Sensors_R1(image_1,cordx,cordy):
	#ok
	avg_b_r1=0
	avg_g_r1=0
	avg_r_r1=0
	for x_cord in range(cordx-5,cordx+5):
		for y_cord in range(cordy-5,cordy+5):
			#print(x_cord)
			#print(y_cord)
			avg_b_r1+=(image_1[y_cord,x_cord])[0]
			avg_g_r1+=(image_1[y_cord,x_cord])[1]
			avg_r_r1+=(image_1[y_cord,x_cord])[2]
	print(avg_b_r1/100,avg_g_r1/100,avg_r_r1/100)
	return avg_b_r1/100, avg_g_r1/100, avg_r_r1/100
def Deside_Keystrokes():
	#generate keystrokes
	print("ok")
def screen_capture():
	check_lane=0
	last_time=time.time()
	while(True):
		capture_screen, image_1=grab_screen(region=(100,100,740,580))
		#find edges
		if check_lane==0:
			edges, cordx, cordy, track_window, roi_hist, term_crit = image_processing(image_1)
		print('heres our {} fps '.format(1/(time.time()-last_time)))
		last_time=time.time()
		#find average pixel values at sensors
		if cordx!=0 and cordy!=0:
			#print(image_1[cordy,cordx])
			check_lane=1
			#sensor midle
			avg_b, avg_g, avg_r =Artificial_Sensors(image_1,cordx,cordy)
			#sensor left 1
			avg_b_l1, avg_g_l1, avg_r_l1 =Artificial_Sensors_l1(image_1,cordx,cordy)
			#sensor right 1
			avg_b_r1, avg_g_r1, avg_r_r1 =Artificial_Sensors_R1(image_1,cordx,cordy)
			#
			#Applying Camshift object tracking
			hsv = cv2.cvtColor(image_1, cv2.COLOR_BGR2HSV)
			dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
			# apply camshift to get the new location
			ret, track_window = cv2.meanShift(dst, track_window, term_crit)
			#nfs needed elements track_window,roi_hist,term_crit
			# Draw it on image
			x,y,w,h = track_window
			img2 = cv2.rectangle(image_1, (x,y), (x+w,y+h), 255,2)
			cv2.imshow('img2',img2)
		cv2.imshow("window",edges)
		#cv2.imshow('wondow',cv2.cvtColor(capture_screen,cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
screen_capture()