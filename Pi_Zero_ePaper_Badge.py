#!/usr/bin/env python

# Pi Zero ePaper Badge
# Taken from        - http://frederickvandenbosch.be/?p=2387
# 3D Files          - http://www.thingiverse.com/thing:21759355 i75
# Automated install - curl -sSL https://goo.gl/i1Imel | sudo bash
#                   - sudo papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]

# Cron Job
# @reboot sudo /home/pi/ebadge.py
# Add this echo @reboot sudo /home/pi/ebadge.py > cron
#

import os
import RPi.GPIO as GPIO
from papirus import PapirusImage
from time import sleep, time
from PIL import Image

# Run as root
user = os.getuid()
if user != 0:
    print "Please run script as root"
    sys.exit()

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.setup(26, GPIO.IN)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.IN)

image = PapirusImage()

# picture folder
projects = "/home/pi/images/"

paths = []

current_index = 0
previous_index = -1

slideshow = 0
last_execution = 0

# populate image list
for filename in os.listdir(projects):
        paths.append(projects + filename)

def my_callback(channel):
        global current_index, previous_index, slideshow

        slideshow = 0

        # display first image
        if(channel == 16):
                current_index = 0
        # display second image
        elif(channel == 26):
                current_index = 1
        # display all images except first two
        elif(channel == 20):
                if(current_index < 2):
                        current_index = 2
                else:
                        current_index = current_index + 1
                if(current_index > len(paths) - 1):
                        current_index = 2
        # start slideshow of all images
        elif(channel == 21):
                slideshow = 1

def display_image():
        # Write image to display if it has changed
        global current_index, previous_index
        if(current_index != previous_index):
                image.write(projects + str(current_index) + ".bmp")
                previous_index = current_index

def increment():
        # Find next image index to display
        global current_index, previous_index, last_execution

        current_index = current_index + 1
        if(current_index > len(paths) - 1):
                current_index = 0

        last_execution = time()

def main():
        while(1):
                now = time()

                # If slideshow mode, automatically switch images
                if(slideshow == 1 and now - last_execution > 10):
                        increment()

                display_image()
                sleep(0.1)

# Wait for button presses
GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=my_callback, bouncetime=300)
GPIO.add_event_detect(20, GPIO.FALLING, callback=my_callback, bouncetime=300)
GPIO.add_event_detect(21, GPIO.FALLING, callback=my_callback, bouncetime=300)

if __name__ == '__main__':
        main()
