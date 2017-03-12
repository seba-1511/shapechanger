#!/usr/bin/env python

import socket as sk
import struct as st
import RPi.GPIO as GPIO
import time

DEFAULT_PORT = 5000
DEFAULT_IP = '192.168.1.4'
BUFFER_SIZE = 32

IN1=15
IN2=13
IN3=11
IN4=7

class RobotServer(object):
    def __init__(self):
        self.port = DEFAULT_PORT
        self.ip = DEFAULT_IP
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        print 'Address: ', addr
        self.conn = conn

    def recv(self):
        data = self.conn.recv(BUFFER_SIZE)
        data = st.unpack('ffff', data)
        return data

    def shutdown(self):
        self.conn.close()

def send_positive(amount, pin_a, pin_b):
	if amount == 0:
		return
	pin_b.ChangeDutyCycle(0)
	pin_a.ChangeDutyCycle(64*amount)
	time.sleep(1)
	pin_a.ChangeDutyCycle(0)
	
def send_negative(amount, pin_a, pin_b):
	if amount == 0:
		return
	pin_a.ChangeDutyCycle(0)
	pin_b.ChangeDutyCycle(64*amount)
	time.sleep(1)
	pin_b.ChangeDutyCycle(0)


if __name__ == '__main__':
    master = RobotServer();
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    p1 = GPIO.PWM(IN1, 50)
    p2 = GPIO.PWM(IN2, 50)
    p3 = GPIO.PWM(IN3, 50)
    p4 = GPIO.PWM(IN4, 50)
    p1.start(0)
    p2.start(0)
    p3.start(0)
    p4.start(0)

    try:
        while True:
            data = master.recv()
            print 'Received data:', data
            send_positive(data[0], p1, p2) #go forward
            send_negative(data[1], p1, p2) #go backward
            send_positive(data[3], p3, p4) #go left
            send_negative(data[2], p3, p4) #go right
                    
    except Exception as e:
            master.shutdown()
            print e

    p1.stop()
    p2.stop()
    p3.stop()
    p4.stop()
    GPIO.cleanup()
