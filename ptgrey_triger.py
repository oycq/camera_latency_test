import os
import PySpin
import numpy as np
import cv2
import serial#sudo pip3 install pyserial
import time

#2-3frame latency, 3-4ms latency
setting_list = [
    ['TriggerMode'           , 'Off'      , 'General'],
    ['TriggerSource'           , 'Software'      , 'General'],
    ['TriggerMode'           , 'On'      , 'General'],
    ['StreamBufferHandlingMode'  , 'NewestOnly'      , 'Stream' ],
    ['AcquisitionMode'           , 'Continuous'      , 'General'],
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



def read(cam, trigger_node):
    time0 = time.time()
    trigger_node.Execute()
    time1 = time.time()
    image_pt = cam.GetNextImage()
    time2 = time.time()
    if image_pt.IsIncomplete():
        print('Image incomplete with image status %d ...' % image_pt.GetImageStatus())
        os._exit(0) 
    image= image_pt.GetNDArray()
    time3 = time.time()
    image_pt.Release()
    print("%6.2f %6.2f %6.2f %6.2f"%((time1-time0)* 1000,(time2-time1)* 1000,(time3-time2)* 1000,(time3-time0)* 1000), end = '\r')
    return image


def loop(cam):
    nodemap = nodemap = cam.GetNodeMap()
    t = PySpin.CCommandPtr(nodemap.GetNode('TriggerSoftware'))
    ser=serial.Serial("/dev/ttyUSB0",115200,timeout=0.001)
    print('asdasdasd')
    last_time = time.time()

    while(1):
        image = read(cam,t)
        cv2.imshow("image",image)
        key = cv2.waitKey(1)
#        print((time.time() - last_time)* 1000, end = '\r')
        last_time = time.time()
        if key == ord('q'):
            os._exit(0)
            break
        if key == ord('t'):
            image0 = read(cam,t)     
            time0 = time.time()   
            ser.write(' '.encode())	
            image1 = read(cam,t)
            time1 = (time.time() - time0) * 1000   
            image2 = read(cam,t)
            time2 = (time.time() - time0 ) * 1000   
            image3 = read(cam,t)
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

    cam.DeInit()
    del cam
    cam_list.Clear()
    system.ReleaseInstance()

if __name__ == '__main__':
    main()
