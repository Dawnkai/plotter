#!/bin/bash
# execute command to allow pigpio control Servo pulses
# - lauch pigpio library as deamon
sudo pigpiod
# Start the Flask webserver
sudo python3 main.py
