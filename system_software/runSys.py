# literally just establishes da serial connection
import serial
import numpy as np
from receiver_functions import cereal, setFreq, read_nmea
# import readnmea

numLines = 50
freq = 4

ser = cereal()
setFreq(ser, freq)
readnmea(ser, numLines)
