# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 18:25:01 2024

@author: maxim
"""

def send_string(current_string):
    import serial
    import time
    # establish serial connection 
    ser = serial.Serial("/dev/ttyUSB0", 19200)
    
    # At the top of the hour, check the inbox for messages.
    # Add a line here that checks the time.
    establish_connection = "AT\r"
    ser.write(establish_connection)
    ans = ser.readline()
    if ans == "OK": # if the serial connection is successful
        successful_transmission = 0
        while successful_transmission == 0:
            write_msg = "AT+SBDWT=" + current_string + "\r" # request read/write status
            ser.write(write_msg)
            sbdix_ans1 = ser.readline()
            if sbdix_ans1 == "OK":
                ser.write("AT+SBDIX\r")
                sbdix_ans = ser.readline()
                sbdix_ans = sbdix_ans[8:].split(",") # splits response up by commas
                
                # Detailed in the AT command reference
                mo_status = sbdix_ans[0] # should be 0-2
            
                # Ok this is all stuff to read commands from the ground station
                if int(mo_status) < 3: # if the message was successfully transmitted
                    successful_transmission += 1
                else:
                    time.sleep(10) # wait 10 seconds to try again
                    
                    
                
