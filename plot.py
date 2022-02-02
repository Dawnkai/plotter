import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import time
from extractor import Extractor


class Plotter:
    """
    Class responsible for handling basic plotter operations such as moving it
    to the right position and controlling the motors.
    :param @dir_x_pin: DIR pin of X axis motor
    :param @dir_y_pin: DIR pin of Y axis motor
    :param @step_x_pin: STEP pin of X axis motor
    :param @step_y_pin: STEP pin of Y axis motor
    :param @mode: Default mode pins
    :param @res: Resolution of the step, default is "Full" step
    :param @delay: Delay between movement
    """
    def __init__(self, dir_x_pin = 20, dir_y_pin = 26, step_x_pin = 21,
                 step_y_pin = 19, mode = (14,15,18), res = (0,0,1),
                 delay = 0.0208 / 28, servo_pin = 12):
        self.dir_x = dir_x_pin
        self.dir_y = dir_y_pin
        self.step_x = step_x_pin
        self.step_y = step_y_pin
        self.delay = delay
        self.mode = mode
        self.res = res
        # Position of the plotter pen
        self.pos = (0, 0)
        # Whether the pen is drawing or not
        self.pen = True
        # Start the servo
        factory = PiGPIOFactory()
        self.servo = Servo(servo_pin, pin_factory=factory)
        #self.servo = GPIO.PWM(servo_pin, 50)
        #self.servo.start(0)

    

    def setup_motor(self, dst, motor_x):
        """
        Setup appropriate motor pins before moving it across the axis.
        :param @dst: Distance to travel (in steps)
        :param @motor_x: Whether to move the X axis motor or Y axis motor
        """
        if motor_x:
            # move LEFT
            if dst < 0:
                GPIO.output(self.dir_x, GPIO.LOW)
                return 1
            # move RIGHT
            else:
                GPIO.output(self.dir_x, GPIO.HIGH)
                return -1
        else:
            # move DOWN
            if dst < 0:
                GPIO.output(self.dir_y, GPIO.LOW)
                return 1
            #move UP
            else:
                GPIO.output(self.dir_y, GPIO.HIGH)
                return -1


    def move_to(self, dst, motor_x):
        """
        Move the motor on specified axis to selected position.
        :param @dst: Distance to travel (in steps)
        :param @motor_x: Whether to move the X axis motor or Y axis motor
        """
        for _ in range(abs(dst)):
            GPIO.output(self.step_x if motor_x else self.step_y, GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(self.step_x if motor_x else self.step_y, GPIO.LOW)
            time.sleep(self.delay)

    def move_by(self, dst, motor_x):
        """
        Move the motor on specified axis to selected position.
        :param @dst: Distance to travel (in steps)
        :param @motor_x: Whether to move the X axis motor or Y axis motor
        """
        #for _ in range(abs(dst)):
        GPIO.output(self.step_x if motor_x else self.step_y, GPIO.HIGH)
        time.sleep(self.delay)
        GPIO.output(self.step_x if motor_x else self.step_y, GPIO.LOW)
        time.sleep(self.delay)

    def move(self, dst):
        """
        Move the motors to their destination.
        :param @dst: Destination to go to, in (x_axis, y_axis) format
        """
        # 1 step = 0.15 mm
        # 6 steps = 0.9 mm, a little above one pixel (1 px = 1 mm)
        # Convert pixels to steps, by multiplying by 6
        dst_x = (dst[0] - self.pos[0]) * 106
        dst_y = (dst[1] - self.pos[1]) * 106

        if (dst_x != 0):
            step_x = self.setup_motor(dst_x, True)
        if (dst_y != 0):
            step_y = self.setup_motor(dst_y, False)

        while (dst_x != 0 or dst_y != 0):
            if (dst_x != 0):
                self.move_by(dst_x, True)
                dst_x += step_x
                #print(dst_x)

            if (dst_y != 0):
                self.move_by(dst_y, False)
                dst_y += step_y
                #print(dst_y)

        self.pos = (dst[0], dst[1])


    def pen_down(self):
        """
        Move the pen downwards to start drawing.
        Prevent the servo from going downwards if the pen is already down.
        """
        if not self.pen:
            #self.servo.ChangeDutyCycle(-2.5) # Quarter rotation downwards
            self.servo.mid()
            time.sleep(0.30)
            self.servo.max()
            time.sleep(0.40)
            #self.servo.ChangeDutyCycle(0)
            self.pen = True


    def pen_up(self):
        """
        Move the pen upwards to stop drawing.
        Prevent the servo from going upwards if the pen is already up.
        Also called when the contour group is changed.
        """
        if self.pen:
            #self.servo.ChangeDutyCycle(2.5) # Quarter rotation upwards
            self.servo.mid()
            time.sleep(0.30)
            self.servo.min()
            time.sleep(0.30)
            #self.servo.ChangeDutyCycle(0)
            self.pen = False


    def plot(self, contours):
        """
        Main plotting function. Will draw the contours passed
        from openCV library and handle all pin setup and teardown.
        :@param contours: contours returned by find_contours in openCV
        """
        # Setup all motors
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.mode, GPIO.OUT)
        GPIO.output(self.mode, self.res)
        GPIO.setup(self.dir_x, GPIO.OUT)
        GPIO.setup(self.dir_y, GPIO.OUT)
        GPIO.setup(self.step_x, GPIO.OUT)
        GPIO.setup(self.step_y, GPIO.OUT)

        self.pen_up()
        for contour in contours:
            for pos in [val[0] for val in contour]:
                self.move(pos)
                self.pen_down()

            self.pen_up()

        self.finish()
        # Disable all motors
        GPIO.cleanup()



    def finish(self):
        """
        Return the plotter to default position after the drawing is finished.
        """
        dst_x = (0 - self.pos[0]) * 106
        dst_y = (0 - self.pos[1]) * 106

        self.setup_motor(dst_x, True)
        self.move_to(dst_x, True)

        self.setup_motor(dst_y, False)
        self.move_to(dst_y, False)

        self.pen_up()
        self.pos = (0, 0)


if __name__ == "__main__":
    extractor = Extractor()
    extractor.set_filepath("PP.png")
    ploter = Plotter()
    #contours = [[[90, 100], [91, 100], [92, 100], [92, 101], [92, 102], [91, 102], [90, 102], [90, 101], [90, 100]],
    # [[60, 60], [61, 61], [62, 62], [63, 61], [64, 60], [63, 59], [62, 58], [61, 59], [60, 60]]]
    #contours1 = [[[0, 0],[218, 121]]]
    cont =extractor.get_contours()
    #print(cont)
    ploter.plot(cont)