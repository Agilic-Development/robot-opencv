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
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')


    while True:
        bot.update()
        # Get an image from the robot
        im, im_time = bot.get_latest_camera_image()

        #img = video_source.read()[1]

        # Convert to grayscale
        im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im_bin = cv2.threshold(im_gray,127,255,cv2.THRESH_BINARY)

        # Display the image
        cv2.imshow( "Image", img )

        #check if user presses a key
        key = cv2.waitKey( 10 )

        if key > 0:
            # Disconnect from the robot
            bot.disconnect()
            exit(0)
