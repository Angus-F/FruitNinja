# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
# initialize the camera and grab a reference to the raw camera capture
def main(pos):
    camera = PiCamera()
    camera.resolution = (600, 400)
    camera.framerate = 30
    camera.hflip = True
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size=(600, 400))
    # allow the camera to warmup
    time.sleep(0.1)
    lower_red=np.array([50,100,100])
    upper_red=np.array([255,255,255])
    # capture frames from the camera
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = image.array
        x,y,w,h=0,0,0,0
        frame = cv2.flip(frame, 0)
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,lower_red,upper_red)
        frame=cv2.bitwise_and(frame,frame,mask=mask)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area = []
        for k in range(len(contours)):
            area.append(cv2.contourArea(contours[k]))
        if area!=[]:
            max_idx = np.argmax(np.array(area))
            x,y,w,h = cv2.boundingRect(contours[max_idx])
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            pos[0]=[x+w//2,y+h//2]
        cv2.imshow('frame', frame)  
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            return

if __name__ == '__main__':
    main()
    

