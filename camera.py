import logging
from picamera import PiCamera
from time import sleep
from datetime import datetime

logger = logging.getLogger()


class CameraNode:
    def __init__(self, filename = "/home/pi/Desktop/plotter/images/img", width = 1920, height = 1080):
        self.camera = PiCamera()
        self.filename = filename
        self.width = width
        self.height = height
        self.framerate = 15
        self.brightness = 70
    

    def save_settings(self):
        self.camera.resolution = (self.width, self.height)
        self.camera.framerate = self.framerate
        self.camera.brightness = self.brightness
    
    
    def set_width(self, width):
        self.width = width
        self.save_settings()
    

    def set_height(self, height):
        self.height = height
        self.save_settings()
    

    def set_framerate(self, framerate):
        self.framerate = framerate
        self.save_settings()
    

    def set_brightness(self, brightness):
        self.brightness = brightness
        self.save_settings()

    
    def save_picture(self):
        logger.debug("Please wait 2 seconds")
        sleep(2)
        logger.info("Taking picture...")
        filename = self.camera.capture(self.filename + datetime.now().strftime("-%d-%m-%Y-%H-%M-%S") + ".jpg")
        logger.debug("Picture saved to " + filename)
        return
        
    
    def take_picture(self):
        logger.debug("Preparing to take a picture...")
        self.camera.start_preview()
        self.save_picture()
        self.camera.stop_preview()
        logger.info("Picture taken successfully!")
