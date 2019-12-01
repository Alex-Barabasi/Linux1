from socket import *
import time
from threading import Thread

from gpiozero import Robot, DistanceSensor

SPEED = 0.2
TURN_SPEED = SPEED + 0.3


class Server():

    def __init__(self):
        # """
        # let's set up some constants
        # super().__init__()
        TCP_IP = '192.168.99.7'
        TCP_PORT = 8080
        self.BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
        # """

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(5)

    def get_message(self):
        return self.conn.recv(self.BUFFER_SIZE)

    def send_message(self, message):
        self.conn.send(message)

    def new_connect(self):
        print('Waiting for connection:')
        self.conn, self.clientaddr = self.s.accept()
        print('Connection address:', self.clientaddr)
        print('listening...')


class RobotControl(Thread):
    distances = list()

    def __init__(self):
        Thread.__init__(self)
        self.cleared = False

    def run(self):
        while self.cleared:
            if len(self.distances) > 5:
                self.distances = self.distances[-1:]
            self.distances.append(sensor.distance)
            if self.derivative() == 1:
                robot.left(TURN_SPEED)
            elif self.derivative() == -1:
                robot.right(TURN_SPEED)
            else:
                robot.forward(SPEED)

    def derivative(self):
        try:
            print(self.distances[-1], self.distances[-2])
            if abs(self.distances[-1] - self.distances[-2]) == 0:
                print("forward")
                return 0
            elif (self.distances[-1] - self.distances[-2]) < 0:
                print("right")
                return 1
            elif (self.distances[-1] - self.distances[-2]) > 0:
                print("left")
                return -1
        except IndexError as e:
            return 0

    def set_cleared(self, value):
        self.cleared = value


if __name__ == "__main__":

    robot = Robot(left=(10, 9), right=(8, 7))
    sensor = DistanceSensor(echo=18, trigger=17)
    server = Server()
    control = RobotControl()
    while True:
        server.new_connect()
        command = server.get_message().strip()
        if command == "start":
            control = RobotControl()
            control.set_cleared(True)
            control.start()
        if command == "stop":
            control.set_cleared(False)
            control.join()
            robot.stop()
        if command == "getdist":
            server.send_message("Ultrasonic distance measurements in cm: " + str(sensor.distance) + "\n")
        if command == "getmotors":
            server.send_message("Motor speed values: " + str(robot.value) + "\n")
