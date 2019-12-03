from socket import *
from threading import Thread

from gpiozero import Robot, DistanceSensor

SPEED = 0


class Server:

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

    def __init__(self, ultrasonic):
        Thread.__init__(self)
        self.cleared = False
        self.set_distanced = 0.3  # keep this amount of meters from wall
        self.last_error = 0
        self.Kp = 3.
        self.Kd = 0.
        self.ultrasonic = ultrasonic

    def run(self):
        while self.cleared:
            if len(self.distances) > 5:
                self.distances = self.distances[-1:]
            self.distances.append(self.ultrasonic.distance)
            direction = self.PD_control()
            print("PD value", direction)
            if direction >= 0:
                if direction > 1:
                    direction = 0.9
                elif direction < 0.05:
                    direction = 0.05
                robot.forward(SPEED, curve_right=direction)
            else:
                direction = -direction
                if direction > 1:
                    direction = 1
                elif direction < 0.05:
                    direction = 0.05
                robot.forward(SPEED, curve_left=direction)

            # if self.derivative() == 1:
            #     robot.left(TURN_SPEED)
            # elif self.derivative() == -1:
            #     robot.right(TURN_SPEED)
            # else:
            #     robot.forward(SPEED)

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

    def PD_control(self):
        print("Distance: ", self.distances[-1])
        error = self.distances[-1] - self.set_distanced
        derivative = error - self.last_error  # simplified derivative
        turn = self.Kp * error + self.Kd * derivative
        self.last_error = error
        return turn

    def set_cleared(self, value):
        self.cleared = value


if __name__ == "__main__":

    robot = Robot(left=(10, 9), right=(8, 7))
    sensor = DistanceSensor(echo=18, trigger=17, queue_len=1)
    server = Server()
    control = RobotControl(sensor)
    while True:
        server.new_connect()
        command = server.get_message().strip()

        """Basic start/stop commands"""
        if command == "start":
            SPEED = 0.3
            control = RobotControl(sensor)
            control.set_cleared(True)
            control.start()
        if command == "stop":
            SPEED = 0
            control.set_cleared(False)
            control.join()
            robot.stop()

        """Tuning the speed values"""
        if command == "increasespeed":
            if SPEED == 0:
                SPEED = SPEED + 0.1
                control = RobotControl(sensor)
                control.set_cleared(True)
                control.start()
            elif SPEED == 1:
                server.send_message("Robot is at max speed" + "\n")
            else:
                SPEED = SPEED + 0.1
                server.send_message("Robot speed has been increased to" + str(SPEED) + "\n")
        if command == "decreasespeed":
            if SPEED == 0:
                server.send_message("Robot is stopped" + "\n")
            elif SPEED == 0.1:
                SPEED = SPEED - 0.1
                control.set_cleared(False)
                control.join()
                server.send_message("Robot has been stopped" + "\n")
            else:
                SPEED = SPEED - 0.1
                server.send_message("Robot speed has been increased to" + str(SPEED) + "\n")

        """Tuning the controller values"""
        if command == "increasekd":
            control.Kd = control.Kd + 0.1
            server.send_message("Derivative coefficient has been increased to" + str(control.Kd) + "\n")
        if command == "increasekp":
            control.Kd = control.Kp + 0.1
            server.send_message("Proportional coefficient has been increased to" + str(control.Kp) + "\n")
        if command == "decreasekd":
            control.Kd = control.Kd - 0.1
            server.send_message("Derivative coefficient has been decreased to" + str(control.Kd) + "\n")
        if command == "decreasekp":
            control.Kd = control.Kp - 0.1
            server.send_message("Proportional coefficient has been decreased to" + str(control.Kp) + "\n")

        """Get the sensor/motor values"""
        if command == "getdist":
            server.send_message("Ultrasonic distance measurements in cm: " + str(sensor.distance) + "\n")
        if command == "getmotors":
            server.send_message("Motor speed values: " + str(robot.value) + "\n")
