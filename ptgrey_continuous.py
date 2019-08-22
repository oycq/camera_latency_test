import os
import PySpin
import numpy as np
import cv2
import serial#sudo pip3 install pyserial
import time

#2-3frame latency, 3-4ms latency
setting_list = [
    ['AcquisitionMode'           , 'Continuous'      , 'General'],
    ['StreamBufferHandlingMode'  , 'NewestOnly'      , 'Stream' ],
                ]


def config_camera(cam, setting_list):
    for i in range(len(setting_list)):
        if setting_list[i][2] == 'General':
            nodemap = cam.GetNodeMap()
        if setting_list[i][2] == 'Stream':
            nodemap = cam.GetTLStreamNodeMap()
        attribute = setting_list[i][0]
        value =  setting_list[i][1]
        node =  PySpin.CEnumerationPtr(nodemap.GetNode(attribute))
        if not PySpin.IsAvailable(node) or not PySpin.IsWritable(node):
            print('Unable to set attribute : %s'%attribute)
            continue
        node_new_value = node.GetEntryByName(value)
        if not PySpin.IsAvailable(node_new_value) or not PySpin.IsReadable(node_new_value):
            print('Cant set %s --> %s'%(value,attribute))
            continue
        node.SetIntValue(node_new_value.GetValue())

def read(cam):
    image_pt = cam.GetNextImage()
    if image_pt.IsIncomplete():
        print('Image incomplete with image status %d ...' % image_pt.GetImageStatus())
        os._exit(0) 
    image= image_pt.GetNDArray()
    image_pt.Release()
    return image


def loop(cam):

    ser=serial.Serial("/dev/ttyUSB0",115200,timeout=0.001)
    last_time = time.time()
    while(1):
        image = read(cam)
        cv2.imshow("image",image)
        key = cv2.waitKey(1)
        print((time.time() - last_time)* 1000, end = '\r')
        last_time = time.time()
        if key == ord('q'):
            os._exit(0)
            break
        if key == ord('t'):
            image0 = read(cam)     
            time0 = time.time()   
            ser.write(' '.encode())	
            image1 = read(cam)
            time1 = (time.time() - time0) * 1000   
            image2 = read(cam)
            time2 = (time.time() - time0 ) * 1000   
            image3 = read(cam)
            time3 =(time.time() - time0) * 1000
            cv2.imshow('before key', image0)
            cv2.imshow('%.2fms' % time1, image1)
            cv2.imshow('%.2fms' % time2, image2)
            cv2.imshow('%.2fms' % time3, image3)
        if key == ord('r'):
            cv2.destroyAllWindows()
    ser.close()
     
def main():
    system = PySpin.System.GetInstance()
    cam_list = system.GetCameras()
    num_cameras = cam_list.GetSize()
    if num_cameras == 0:
        cam_list.Clear()
        system.ReleaseInstance()
        print('Not enough cameras!')
        return -1 
    cam = cam_list[0]
    cam.Init()
    config_camera(cam, setting_list)
    cam.BeginAcquisition()

    loop(cam)

    cam.EndAcquisition()
    cam.DeInit()
    del cam
    cam_list.Clear()
    system.ReleaseInstance()

if __name__ == '__main__':
    main()
