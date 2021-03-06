# import cv2
import time
import serial
import cv2
import os
import numpy as np
import sys

if len(sys.argv)>=2:	
	VIDEO_DEVICE=int(sys.argv[1])
cap=cv2.VideoCapture(VIDEO_DEVICE)
cap.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
if len(sys.argv)>=3:	
	form=sys.argv[2]
	cap.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc(form[0],form[1],form[2],form[3]))
message=os.popen('v4l2-ctl -d /dev/video%d -P'%VIDEO_DEVICE).read()
message+=os.popen('v4l2-ctl -d /dev/video%d -V'%VIDEO_DEVICE).read()
message+=os.popen('v4l2-ctl -d /dev/video%d --list-formats-ext'%VIDEO_DEVICE).read()
print(message)
ser=serial.Serial("/dev/ttyUSB0",115200,timeout=0.001)
while(1):
	_,image=cap.read()
	cv2.imshow("enter Key 't' to test,'q' to quit,'r' to reset",image)
	c=cv2.waitKey(1)
	if c==-1:
		continue
	if chr(c)=='t':
		_,image0=cap.read()     
                time0=time.time()   
		ser.write(' ')	
		_,image1=cap.read()
                time1=(time.time()-time0)*1000   
		_,image2=cap.read()
                time2=(time.time()-time0)*1000   
		_,image3=cap.read()
                time3=(time.time()-time0)*1000
                cv2.imshow('before key',image0)
		cv2.imshow('%.2fms'%time1,image1)
		cv2.imshow('%.2fms'%time2,image2)
		cv2.imshow('%.2fms'%time3,image3)
	if chr(c)=='r':
 		cv2.destroyAllWindows()	
	if chr(c)=='q':
		reak	
