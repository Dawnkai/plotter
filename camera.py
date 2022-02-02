import logging
from time import sleep
from datetime import datetime
from picamera import PiCamera

logger = logging.getLogger()


class Camera:
    """
    Main camera node. Responsible for taking pictures and saving them locally.
    :param filename: Absolute filepath (without extension) where node will save images
    :type arg: str
    :param width: Width of the image
    :type width: int
    :param height: Height of the image
    :type height: int
    """


    def __init__(self, filename = "/home/pi/Desktop/plotter/static/cam",
                 width = 640, height = 480):
        self.camera = PiCamera()
        self.filename = filename
        self.width = width
        self.height = height
        self.framerate = 15
        self.brightness = 70


    def save_settings(self):
        '''
        Function saving new settings for camera. Called after every individual update
        such as resizing the image or changing its framerate.
        '''
        self.camera.resolution = (self.width, self.height)
        self.camera.framerate = self.framerate
        self.camera.brightness = self.brightness


    def set_width(self, width):
        '''
        Set new width for the image.
        :param width: New width
        :type width: int
        '''
        self.width = width
        self.save_settings()


    def set_height(self, height):
        '''
        Set new height for the image.
        :param height: New height
        :type height: int
        '''
        self.height = height
        self.save_settings()


    def set_framerate(self, framerate):
        '''
        Set new framerate for the camera.
        :param framerate: New framerate
        :type framerate: int
        '''
        self.framerate = framerate
        self.save_settings()


    def set_brightness(self, brightness):
        '''
        Set new brightness for the camera.
        :param brightness: New brightness
        :type brightness: int
        '''
        self.brightness = brightness
        self.save_settings()


    def save_picture(self):
        '''
        Take and save a picture on the local drive.
        '''
        logger.debug("Taking picture, please wait 3 seconds...")
        sleep(2)
        # All pictures have appended time and date for easy search
        filename = self.camera.capture(self.filename + datetime.now()
                                       .strftime("-%d-%m-%Y-%H-%M-%S") + ".jpg")
        logger.debug("Picture saved to %s.", filename)


    def take_picture(self):
        '''
        Take new picture.
        '''
        logger.debug("Preparing to take a picture...")
        self.camera.start_preview()
        self.save_picture()
        self.camera.stop_preview()
        logger.info("Picture taken successfully!")
