# script to send MT (mobile-terminated) message to RockBlock using HTTP Post endpoint
# (i.e. to send from ground station to on-site system)

# in terminal before running: python -m pip install requests
import requests
import numpy as np
# query parameters
    # it would be a good idea to have these as inputs at the beginning so a different user could set up their RockBlock with our code
imei = "300434068462010"
username1 = "max.feinland%40colorado.edu"
username2 = "max.feinland@colorado.edu" # this is just how they did the RockBlock example code I'm not sure why
password = "Velociraptor"
msg_ASCII = "Wutz up" # user input will be string

# convert user input to hex (this is required by RockBlock)
ascii_bytes = msg_ASCII.encode('ascii')
hex_list = [format(byte, '02x') for byte in ascii_bytes]
msg_hex = ''
for n in range(len(hex_list)):
    msg_hex = msg_hex+hex_list[n]

# url format required by RockBlock
url = 'https://rockblock.rock7.com/rockblock/MT?imei=300434068462010&username='+username1+'&username='+username2+'&password='+password+'&data='+msg_hex

headers = {"accept": "text/plain"} # also how they did the RockBlock example code
# Response body will be list of values separated by commas
# first value: status ("OK" or "FAILED")
# if status "OK":
    # second value: mtId (mobile-terminated identfier)
# if status "FAILED"
    # second value: integer error code
    # third value: error code text description
response = requests.post(url, headers=headers)
print(response.text)
