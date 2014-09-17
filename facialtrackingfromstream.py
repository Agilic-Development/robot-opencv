#! /usr/bin/python

# This example shows the simplest way of getting an image from the robot's camera. The image
# is an OpenCV image so we also show how to perform edge detection on the image

import time
import argparse
import cv2
import py_websockets_bot
import numpy as np

#---------------------------------------------------------------------------------------------------        
if __name__ == "__main__":

    video_source = cv2.VideoCapture(0)

    # Set up a parser for command line arguments
    parser = argparse.ArgumentParser( "Gets an image from the robot" )
    parser.add_argument( "hostname", default="localhost", nargs='?', help="The ip address of the robot" )

    args = parser.parse_args()
 
    # Connect to the robot
    bot = py_websockets_bot.WebsocketsBot( args.hostname )

    # Start streaming images from the camera
    bot.start_streaming_camera_images()

    #select cascade library
    face_cascade = cv2.CascadeClassifier('cascade_resources/haarcascade_frontalface_alt.xml')

    left_motor = 0
    right_motor = 0
    camera_pan = 90
    camera_tilt = 90

    while True:
        bot.update()
        # Get an image from the robot, returns the image and a time stamp
        im, im_time = bot.get_latest_camera_image()
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
                left_motor = 100
                right_motor = -100

            if im_width/2 < faces_center[0]:
                print "go right"
                left_motor = 100
                right_motor = -100

            if im_height/2 > faces_center[1]:
                print "go up"

            if im_height/2 < faces_center[1]:
                print "go down"
        else:
            left_motor = 0
            right_motor = 0

        left_motor, right_motor, camera_pan, camera_tilt = offset_to_movement(x_offset, y_offset)
        send_motor_commands(left_motor, right_motor, camera_pan, camera_tilt)
        # Display the image
        cv2.imshow( "Image", im_flip )

        #check if user presses a key
        key = cv2.waitKey( 10 )
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

def offset_to_movement(x_offset, y_offset):

    return left_motor, right_motor, camera_pan, camera_tilt

def send_motor_commands(left_motor, right_motor, camera_pan, camera_tilt):
    bot.set_neck_angles(camera_pan,camera_tilt)
    bot.set_motor_speeds(left_motor,right_motor)

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
