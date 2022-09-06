from turtle import right
import cv2
import time
import numpy as np
import pyautogui
import pydirectinput
from PIL import ImageGrab
import win32gui
from math import *
from mss import mss
import threading as th
#from pyjoystick.sdl2 import Key, Joystick, run_event_loop

prev_frame_time = 0
new_frame_time = 0
start_time = time.time()
font = cv2.FONT_HERSHEY_DUPLEX
mon = {'top': 600, 'left': 750, 'width': 400, 'height': 250}
pydirectinput.pause = 0
PAUSE = 0
leftside=0
rightside=0
def leftcontroll():
    
    pydirectinput.move(-1,None)
    print("left")
    #time.sleep(0.1)
def rightcontroll():
    
    pydirectinput.move(+1,None)
    print("right")
    #time.sleep(0.1)

    

with mss() as sct:
    while True:
        pydirectinput.pause = 0
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)
        img1 = sct.grab(mon)
        img_np = np.array(img1)
        
        frame = cv2.GaussianBlur(img_np, (5, 5), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_white = np.array([0, 0, 180])
        up_white = np.array([172, 111, 255])
        mask = cv2.inRange(hsv, low_white, up_white)
        cv2.line(mask, (-10, 50), (100, -40), (0, 0, 0), 90)
        cv2.line(mask, (420, 55), (280, -80), (0, 0, 0), 90)
        global lines_edges
        edges = cv2.Canny(mask, 150, 180)
        cv2.line(hsv, (-10, 50), (100, -40), (0, 0, 0), 90)
        cv2.line(hsv, (420, 55), (280, -80), (0, 0, 0), 90)
        
        cv2.putText(hsv, fps, (7, 70), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 30, maxLineGap=100)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                frame=cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                #lines_edges = cv2.addWeighted(img_np, 0.1, frame, 1.5, 0)

        #cv2.line(lines_edges, (-20, 50), (90, -30), (0, 0, 0), 90)
        #cv2.line(lines_edges, (420, 55), (280, -80), (0, 0, 0), 80)
        #print(x1,x2)
            if ((x1 or x2) > img1.size.width/2) :
            #print(sqrt(x1*x1+y2*y2))
                if 240<sqrt(x1*x1+y2*y2) < 280:
                    #print("Sola git")
                    #print(sqrt(x1*x1+y2*y2))
                    #pydirectinput.keyDown('a')
                    #pydirectinput.move(-1,None)
                    #time.sleep(0.1)
                    #pydirectinput.keyUp('a')
                    t1=th.Thread(target=leftcontroll)
        
                    t1.start()
        
                    leftside=sqrt(x1*x1+y2*y2)
                    
                #
            elif ((x1 or x2) < img1.size.width/2):
                if 160>sqrt(x1*x1+y2*y2) > 120:
                    #print("saga git")
                    #print(sqrt(x1 * x1 + y2 * y2))
                    #pydirectinput.keyDown('d')
                    #pydirectinput.move(1,None)
                    #time.sleep(0.1)
                    #pydirectinput.keyUp('d')
                    rightside=sqrt(x1*x1+y2*y2)
                    t2=th.Thread(target=rightcontroll)
                    t2.start()

            
            """""
            avg=int((leftside+rightside)/2)
            if 200>avg and 160>sqrt(x1*x1+y2*y2) > 120:
                pydirectinput.keyDown('d')
                time.sleep(0.1)
                pydirectinput.keyUp('d')
            
            if 200<avg and 240<sqrt(x1*x1+y2*y2) < 280:
                pydirectinput.keyDown('a')
                time.sleep(0.1)
                pydirectinput.keyUp('a')
            
            #print(avg)
            if avg!=0:
                print(avg)
            """""
        #if ((x1 or x2) < img1.size.width/2) and 260<(x1 or x2)<380 :

        cv2.imshow("frame", hsv)
        cv2.imshow("edges", mask)
        #print((x1+y1)/2)
        key = cv2.waitKey(1)
        if key == 27:
            break


cv2.destroyAllWindows()