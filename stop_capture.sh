#!/bin/bash
sudo kill -9 $(ps aux | grep "gst-launch-1.0" | awk '{ print $2 }')
