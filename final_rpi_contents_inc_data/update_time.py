import serial
from receiver_functions import *
import sys


def main():

    GNSS_ser = serial.Serial("/dev/ttyUSB1", 115200)

    t = get_time(GNSS_ser)
    #send_string(str(t) + ", successfully started ops")
    sys.exit(t)

if __name__ == "__main__":
    main()
