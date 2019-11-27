from socket import *
import time
from gpiozero import Robot, DistanceSensor

distances = list()


def setup_server():
    # """
    # let's set up some constants
    HOST = ''  # we are the host
    PORT = 8080  # arbitrary port not currently in use
    ADDRESS = (HOST, PORT)  # we need a tuple for the address
    BUFFER_SIZE = 4096  # reasonably sized buffer for data
    # """

    """ now we create a new socket object (serv)
    see the python docs for more information on the socket types/flags
    """
    serv = socket(AF_INET, SOCK_STREAM)

    """ bind our socket to the address
    """
    serv.bind(ADDRESS)  # the double parens are to create a tuple with one element
    serv.listen(5)  # 5 is the maximum number of queued connections we'll allow
    print('listening...')


def derivative():
    try:
        threshold = 0.02
        if abs(distances[-1] - distances[-2]) < threshold:
            return 0
        elif (distances[-1] - distances[-2]) < 0:
            return -1
        elif (distances[-1] - distances[-2]) > 0:
            return 1
    except IndexError as e:
        return 0


if __name__ == "__main__":
    robot = Robot()
    sensor = DistanceSensor()
    while True:
        if len(distances) > 5:
            distances = distances[-1:]
        distances.append(sensor.distance)
        if derivative() == 1:
            robot.left()
        elif derivative() == -1:
            robot.right()
        else:
            robot.forward()

