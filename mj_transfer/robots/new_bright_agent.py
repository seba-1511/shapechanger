#!/usr/bin/env python

import io
import time
import socket as sk
import struct as st
try:
    import RPi.GPIO as GPIO
except:
    pass

from PIL import Image
from threading import Thread

from .remote_robot_agent import RemoteRobotAgent, forever


BUFFER_SIZE = 16
POWER_SCALING = 60
STEERING_SCALING = 40
SLEEP_TIME = 0.5

IN1 = 15
IN2 = 13
IN3 = 11
IN4 = 7
PWM1 = 20
PWM2 = 21


#********************* Camera Stuff *********************
try:
    import picamera
    DEBUG = False
except ImportError:
    pass
    class cdict(dict):
        def __enter__(self): return cdict()

        def __exit__(self, *args, **kwargs): return cdict()
    picamera = cdict()
    picamera.PiCamera = lambda: cdict()
    DEBUG = True
# debug_img = Image.open('asdf.jpg')
# debug_stream = io.BytesIO()
# debug_img.save(debug_stream, format='jpeg')
debug_img = None
debug_stream = None


def infinite_buffer(callback):
    stream = io.BytesIO()
    while True:
        yield stream
        stream.seek(0)
        callback(stream)
        stream.seek(0)
        stream.truncate()


def capture_with_callback(camera, callback=None):
    if callback is None:
        callback = lambda stream: None
    camera.capture_sequence(infinite_buffer(callback),
                            'jpeg', use_video_port=True)


def init_camera_capture(callback=None):
    s = time.time()
    with picamera.PiCamera() as camera:
        # camera.resolution = (256, 256)
        camera.resolution = (128, 128)
        # camera.resolution = (256, 96)
        camera.framerate = 80
        time.sleep(2)
        start = time.time()
        stream = io.BytesIO()
        if not DEBUG:
            capture_with_callback(camera, callback)
        else:
            for _ in range(40):
                print('outer loop')
                debug_stream.seek(0)
                callback(debug_stream)

        finish = time.time()
        print('Captured 40 images at %.3f fps.' % (40.0 / (finish - start)))

#********************* New Bright Architecture *********************

class NewBrightAgent(RemoteRobotAgent):

    def __init__(self, ip, port):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)
        self.p1 = GPIO.PWM(IN1, 50)
        self.p2 = GPIO.PWM(IN2, 50)
        self.p3 = GPIO.PWM(IN3, 50)
        self.p4 = GPIO.PWM(IN4, 50)
        self.pwm1 = GPIO.PWM(PWM1, 50)
        self.pwm2 = GPIO.PWM(PWM2, 50)
        self.p1.start(0)
        self.p2.start(0)
        self.p3.start(0)
        self.p4.start(0)
        self.pwm1.start(0)
        self.pwm2.start(0)
        super(NewBrightAgent, self).__init__(ip, port)

    def clean(self):
        super(NewBrightAgent, self).clean()
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()
        self.p4.stop()
        GPIO.cleanup()

    # Overrideable
    def run(self):
        print('running')
        init_camera_capture(self.robot_process)

    # Overrideable
    def robot_process(self, stream):
        img = stream.getvalue()
        # print('img size:', len(img))
        self.send([0.0, len(img), 0.0, 0.0])
        # send the image
        self.conn.sendall(img)
        action = self.recv()
        if action[0] == -1:
            raise Exception('This run has been terminated by the client.')
        self.execute(action)

    def execute(self, action):
        print('Received action:', action)
        # go forward
        forward = Thread(target=self.send_positive,
                         args=(POWER_SCALING * action[0],
                               self.p1,
                               self.p2))
        # go backward
        back = Thread(target=self.send_negative,
                      args=(POWER_SCALING * action[1],
                            self.p1,
                            self.p2))
        # go left
        left = Thread(target=self.send_positive,
                      args=(STEERING_SCALING * action[3],
                            self.p3,
                            self.p4))
        # go right
        right = Thread(target=self.send_negative,
                       args=(STEERING_SCALING * action[2],
                             self.p3,
                             self.p4))
        forward.start()
        back.start()
        left.start()
        right.start()

    def send_positive(self, amount, pin_a, pin_b):
        if amount == 0:
            return
        pin_b.ChangeDutyCycle(0)
        pin_a.ChangeDutyCycle(amount)
        time.sleep(SLEEP_TIME)
        pin_a.ChangeDutyCycle(0)

    def send_negative(self, amount, pin_a, pin_b):
        if amount == 0:
            return
        pin_a.ChangeDutyCycle(0)
        pin_b.ChangeDutyCycle(amount)
        time.sleep(SLEEP_TIME)
        pin_b.ChangeDutyCycle(0)


if __name__ == '__main__':

    def main():
        robot = NewBrightAgent('192.168.42.1', 5000)
        try:
            robot.run()
            print('Run Finished')
        except:
            print('qwer')
            robot.clean()
        robot.clean()

    forever(main)
