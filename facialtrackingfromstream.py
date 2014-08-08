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


    while True:
        key = cv2.waitKey(10)
        #check if face cascade should be changed
        if key > 0
            face_cascade = cascade_choice(key)

        bot.update()
        # Get an image from the robot
        im, im_time = bot.get_latest_camera_image()
        #flip the video as the camera is upside down
        im_flip = cv2.flip(im, flipCode = 0)

        # Convert to grayscale
        im_gray = cv2.cvtColor(im_flip, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(im_gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(im_flip,(x,y),(x+w,y+h),(255,0,0),2)
        # Display the image
        cv2.imshow( "Image", im_flip )

        #check if user presses a key
        key = cv2.waitKey( 10 )

        if key > 0:
            # Disconnect from the robot
            bot.disconnect()
            exit(0)

def cascade_choice(choice = 1):
    if choice == 1:
        face_cascade = cv2.CascadeClassifier('cascade_resources/haarcascade_frontalface_alt.xml')
    if choice == 2:
        face_cascade = cv2.CascadeClassifier('cascade_resources/')
    if choice == 3:
        face_cascade = cv2.CascadeClassifier('cascade_resources/')
    if choice == 4:
        face_cascade = cv2.CascadeClassifier('cascade_resources/')
    if choice == 5:
        face_cascade = cv2.CascadeClassifier('cascade_resources/')
    if choice == 6:
        face_cascade = cv2.CascadeClassifier('cascade_resources/')
    if choice == 7:
        face_cascade = cv2.CascadeClassifier('cascade_resources/')
    if choice == 8:
        face_cascade = cv2.CascadeClassifier('cascade_resources/')
