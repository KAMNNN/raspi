#!/bin/bash

# Replace first GstElement with alsasrc device=hw:iD14
gst-launch-1.0 audiotestsrc ! audioconvert ! flacenc ! multifilesink location="/home/pi/Documents/raspi/raw/chunk%d.flac" next-file=4 max-file-size=500000 &
