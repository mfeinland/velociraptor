# Luke and Jeong made this

# idk what any of this means
import time
import w1thermsensor

# this part should be fun
sensor = w1thermsensor.__main__()

#YAY
while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s degrees Celcius" % temperature)
    time.sleep(1)
