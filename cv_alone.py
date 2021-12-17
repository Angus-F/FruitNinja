import cv2
import numpy as np
import time
from imutils.video import WebcamVideoStream


def loop(cam,lower_red,upper_red):
    time.sleep(1)
    stop=0
    x,y,w,h=0,0,0,0
    frame = cam.read()
    frame = cv2.flip(frame, 1)
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
    
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        stop=1
    return x+w//2,y+h//2,stop

    

def main():
    cam = WebcamVideoStream(src=0).start()
    time.sleep(1)
    lower_red=np.array([50,100,100])
    upper_red=np.array([255,255,255])
    while(1):
        #loop(cam,lower_red,upper_red)
        x,y,stop=loop(cam,lower_red,upper_red)
        #with open("./pos.txt",'w') as f:
        #    f.write(str(x))
        #    f.write('\n')
        #    f.write(str(y))
        if stop:
            break
        

if __name__ == '__main__':
    main()
    
    
