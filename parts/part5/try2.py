import cv2
import numpy as np
import time
from grabScreen import grab_screen
from statistics import mean
from numpy import ones,vstack
from numpy.linalg import lstsq
from direct_key_inputs import PressKey, ReleaseKey, W, A, S, D
import t
lane_color_r=0
lane_color_g=0
lane_color_b=0
fisrst_time=0
last_pos="w"
def straight():
	PressKey(W)
	ReleaseKey(A)
	ReleaseKey(D)
def left():
	PressKey(A)
	for i in range (0,200):
		PressKey(W)
	ReleaseKey(W)
	ReleaseKey(D)
	ReleaseKey(A)
def right():
	PressKey(D)
	for i in range (0,200):
		PressKey(W)
	ReleaseKey(A)
	ReleaseKey(W)
	ReleaseKey(D)
def slow_ya_roll():
	ReleaseKey(W)
	ReleaseKey(A)
	ReleaseKey(D)
def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):
	# if this fails, go with some default line
	try:
		# finds the maximum y value for a lane marker 
		# (since we cannot assume the horizon will always be at the same point.)
		ys = []  
		for i in lines:
			for ii in i:
				ys += [ii[1],ii[3]]
		min_y = min(ys)
		max_y = 600
		new_lines = []
		line_dict = {}
		for idx,i in enumerate(lines):
			for xyxy in i:
				# These four lines:
				# modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
				# Used to calculate the definition of a line, given two sets of coords.
				x_coords = (xyxy[0],xyxy[2])
				y_coords = (xyxy[1],xyxy[3])
				A = vstack([x_coords,ones(len(x_coords))]).T
				m, b = lstsq(A, y_coords)[0]
				# Calculating our new, and improved, xs
				x1 = (min_y-b) / m
				x2 = (max_y-b) / m
				line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
				new_lines.append([int(x1), min_y, int(x2), max_y])
		final_lanes = {}
		for idx in line_dict:
			final_lanes_copy = final_lanes.copy()
			m = line_dict[idx][0]
			b = line_dict[idx][1]
			line = line_dict[idx][2]

			if len(final_lanes) == 0:
				final_lanes[m] = [ [m,b,line] ]
			else:
				found_copy = False
				for other_ms in final_lanes_copy:
					if not found_copy:
						if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
							if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
								final_lanes[other_ms].append([m,b,line])
								found_copy = True
								break
						else:
							final_lanes[m] = [ [m,b,line] ]
		line_counter = {}
		for lanes in final_lanes:
			line_counter[lanes] = len(final_lanes[lanes])
		top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]
		lane1_id = top_lanes[0][0]
		lane2_id = top_lanes[1][0]
		def average_lane(lane_data):
			x1s = []
			y1s = []
			x2s = []
			y2s = []
			for data in lane_data:
				x1s.append(data[2][0])
				y1s.append(data[2][1])
				x2s.append(data[2][2])
				y2s.append(data[2][3])
			return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 
		l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
		l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])
		return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
	except Exception as e:
		print(str(e))

def process_roi_lanes(img,lines):
	try:
		for line in lines:
			coords = line[0]
			cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],3)
			if coords[0]<=180 and coords[1]>=300 and coords[1]<=350:
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
def image_processing(image):
	original_image=image
	#processed_img_1= cv2.imshow('wondow',origional_img)
	processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	processed_img =  cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
	processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
	vertices = np.array([[1,480],[1,280],[100,225],[540,225],[640,280],[640,470]], np.int32)
	#processing the edges
	processed_img=roi(processed_img, [vertices])
	#draw lines and hough transform
	lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,20,15)
	m1 = 0
	m2 = 0
	rtn=0
	try:
		l1, l2, m1,m2 = draw_lanes(original_image,lines)
		cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
		cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
		print(l1[2],l1[3])
		rtn=1
		print("returned 1")
	except Exception as e:
		print(str(e))
		pass
	'''
	try:
		for coords in lines:
			coords = coords[0]
			try:
				cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 53)
			except Exception as e:
				print(str(e))
	except Exception as e:
		pass
	'''
	if rtn==1:
		return processed_img,original_image, m1, m2, 110, 200
	elif rtn==0:
		return processed_img,original_image, m1, m2, 110, 200
def check_origional_lane_colour(xcord,ycord,img):
	print("inside colour check")
	colour=img[int(xcord),int(ycord)]
	if coulor[0]>130 and colour[0]<160:
		if colour[1]>90 and colour[1]<120:
			if colour[2]>20 and colour[2]<52:
				img[int(xcord),int(ycord)]=[255,0,0]
	return colour,img
def screen_capture():
	check_lane=0
	last_time=time.time()
	while(True):
		capture_screen, image_1=grab_screen(region=(100,100,740,580))
		t.car_detection(capture_screen)
		#find edges
		if check_lane == 0:
			print("1check")
			new_screen,original_image, m1, m2, xcord, ycord = image_processing(capture_screen)
			print("2check")
			print(xcord,ycord)
			cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
		print('heres our {} fps '.format(1/(time.time()-last_time)))
		last_time=time.time()
		'''
		if m1 < 0 and m2 < 0:
			right()
		elif m1 > 0  and m2 > 0:
			left()
		else:
			straight()
		'''
		#cv2.imshow('wondow',cv2.cvtColor(capture_screen,cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
screen_capture()