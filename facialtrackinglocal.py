#! /usr/bin/python

# This example shows the simplest way of getting an image from the robot's camera. The image
# is an OpenCV image so we also show how to perform edge detection on the image

#some code is based on: http://blog.derivatived.com/posts/OpenCV-Tutorial-on-Face-Tracking-Raspberry-PI-Camera/

import time
import argparse
import cv2
#import py_websockets_bot
import numpy as np
import picamera
import io

#---------------------------------------------------------------------------------------------------        
if __name__ == "__main__":

    #video_source = cv2.VideoCapture(0)

    #select cascade library
    face_cascade = cv2.CascadeClassifier('cascade_resources/haarcascade_frontalface_alt.xml')

    stream = io.BytesIO()

    #set the resolution
    CAMERA_WIDTH = 320
    CAMERA_HEIGHT = 240

    with picamera.PiCamera() as camera:
        camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        #capture into stream
        camera.capture(stream, format='jpeg')
    #convert image into numpy array
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #turn the array into a cv2 image
    im = cv2.imdecode(data, 1)

    while True:

        #flip the video as the camera is upside down
        im_flip = cv2.flip(im, flipCode = 0)

        # Convert to grayscale
        im_gray = cv2.cvtColor(im_flip, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(im_gray, 1.3, 5)
        faces_center=[]
        for (x,y,w,h) in faces:
            cv2.rectangle(im_flip,(x,y),(x+w,y+h),(255,0,0),2)
            #find center point
            faces_center.append(x+(w/2))
            faces_center.append(y+(w/2))
            cv2.circle(im_flip,(faces_center[0],faces_center[1]),2,(255,0,0),2)
        
        #find image dimensions
        im_width, im_height = im_gray.shape[:2]

        #check if faces_center has anything in it
        if faces_center:
            #follow face
            if im_width/2 > faces_center[0]:
                print "go left"

            if im_width/2 < faces_center[0]:
                print "go right"

            if im_height/2 > faces_center[0]:
                print "go up"

            if im_height/2 < faces_center[0]:
                print "go down"

        # Display the image
        cv2.imshow( "Image", im_flip )

        #check if user presses a key
        key = cv2.waitKey()
        if key > 0:
            print key
            if key == 1113937:
                bot.set_motor_speeds(-80.0,80.0)
            #face_cascade = cascade_choice(key)
            #bot.set_motor_speeds(-80.0,80.0) #spin left
            if key == 1048603:
                # Disconnect from the robot
                bot.disconnect()
                exit(0)

def cascade_choice(choice = 1):
    if choice == 1:
        face_cascade = cv2.CascadeClassifier('cascade_resources/haarcascade_frontalface_alt.xml')
    if choice == 2:
        face_cascade = cv2.CascadeClassifier('cascade_resources/haarcascade_eye.xml')
    if choice == 3:
        face_cascade = cv2.CascadeClassifier('cascade_resources/haarcascade_smile.xml')
    if choice == 4:
        face_cascade = cv2.CascadeClassifier('cascade_resources/lbpcascade_frontalface.xml')
    if choice == 5:
        face_cascade = cv2.CascadeClassifier('cascade_resources/lbpcascade_profileface.xml')
    if choice == 6:
        face_cascade = cv2.CascadeClassifier('cascade_resources/lbpcascade_silverware.xml')
    if choice == 7:
        face_cascade = cv2.CascadeClassifier('cascade_resources/hogcascade_pedestrians.xml')
    if choice == 8:
        face_cascade = cv2.CascadeClassifier('cascade_resources/inria_caltech-17.01.2013.xml')
    if choice == 8:
        face_cascade = cv2.CascadeClassifier('cascade_resources/soft-cascade-17.12.2012.xml')
    else:
        print "invalid cascade selection"
