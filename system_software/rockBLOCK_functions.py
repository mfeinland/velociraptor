# rockBLOCK_functions.py
# Date: 2/10/24
# Author: Rebecca Blum, Max Feinland
# 
# Revisions: 
#   [name]       [date]       [notes]
#	B. Blum      2/29/24      added Max's send_string()
#	R. Blum      2/10/24      initial script creation 
#
# Summary: 
# 	This script contains functions that communicate with the rockBLOCK 
#	transceiver. 
#
#	connect_to_rock - Max
#	send_string - Max 
#	check_mail - Becca
# Inputs:
#   [] 
#
# Outputs: 
#   []
#
# Limitations: 
#
# Future edits: 
#   [issue]                               [status]                    [name]
#   
#------------------------------------------------------------------------------
import serial
import time

def connect_to_rock():
	# establish serial connection 
    ser = serial.Serial("/dev/ttyUSB0", 19200)
    establish_connection = "AT\r"
    ser.write(establish_connection)
    check = ser.readline() # OK if connection is successful
    return check

def send_string(current_string):
    # establish serial connection 
    ser = serial.Serial("/dev/ttyUSB0", 19200)
    
    # At the top of the hour, check the inbox for messages.
    # Add a line here that checks the time. 
      # - this would actually be in the main script - becca
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

def check_mail():
    message = []
    check = connect_to_rock()
    
    if check == "OK": # the serial connection is successful
      # Execute Send/Receive
      ser.write("AT+SBDIX\r")
      # Receive response 
      # +SBDIX: 0, 1, 1, 1, 6, 8\r
      mailbox_status = ser.readline()
      mailbox_status = mailbox_status.split(',')
      # OK\r

      if ans[3] == 1: 
          # Transfer "Hello1" message to your controller 
          ser.write("AT+SBDRT\r")
          message_end = 0 # flag down
          while message_end == 0:
            message.append(ser.readline())
            if "OK" in message:
               message_end = 1 # flag goes up
          # Receive response
          #+SBDRT:\r
          #Hello1\r
          #OK\r
      else:
        message = "None"

    return message 