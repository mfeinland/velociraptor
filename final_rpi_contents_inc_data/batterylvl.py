import sys
from time import sleep
from quick2wire.parts.pcf8591 import *
from quick2wire.i2c import I2CMaster
def battlvl():
    address = int(sys.argv[1]) if len(sys.argv) > 1 else BASE_ADDRESS
    pin_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    # ref_voltage = 3.3
    # divider = 6 # see https://www.enigma14.eu/wiki/AD_Converter_PCF8591_for_Raspberry_Pi
    calib = 105
    with I2CMaster() as i2c:
        adc = PCF8591(i2c, FOUR_SINGLE_ENDED)
        pin = adc.single_ended_input(pin_index)
        count = 1
        # while True:
        voltage = calib*pin.value
        # print("{}".format(voltage))
        sleep(0.5)
        count += 1
    return voltage
