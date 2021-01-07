import cv2
import numpy as np
import time
from grabScreen import grab_screen
from direct_key_inputs import PressKey, ReleaseKey, W, A, S, D

def forward():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
def process_roi_lanes(img,lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
            #print(coords[0],coords[1])
            #draw circle at the bottom of lane
            cv2.circle(img,(coords[0],coords[1]), 10, (255,0,255), 1)
    except:
        pass
def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 100)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked
def Image_processing(origional_img):
    processed_img_1 = cv2.imshow('wondow',origional_img)
    processed_img = cv2.Canny(cv2.cvtColor(origional_img,cv2.COLOR_BGR2RGB), threshold1=50, threshold2=300)
    #get edges only from our region of interest
    vertices = np.array([[1,480],[1,280],[100,225],[540,225],[640,280],[640,470]], np.int32)
    #vertices = np.array([[bottomleft],left up],[middle left],[middle right],[right up],[right bottom])
    processed_img = roi(processed_img, [vertices])
    #process edges in roi
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 55, 45)
    process_roi_lanes(processed_img,lines)
    return processed_img
def screen_capture():
    last_time=time.time()
    while(True):
        #grab_image
        capture_screen,image_1 = grab_screen(region=(100,100,740,580))
        #find edges or process image
        edges = Image_processing(image_1)
        print('heres our {} time '.format(time.time()-last_time))
        last_time=time.time()
        cv2.imshow('window', edges)
        #cv2.imshow('wondow',cv2.cvtColor(capture_screen,cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25)&0xFF==('q'):
            cv2.destroyAllWindows()
            break

screen_capture()

