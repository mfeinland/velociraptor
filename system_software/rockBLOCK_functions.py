# rockBLOCK_functions.py
# Date: 2/10/24
# Author: Rebecca Blum
# 
# Revisions: 
#   [name]       [date]       [notes]
#   R. Blum      2/10/24      initial script creation 
#
# Summary: 
#     
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

def check_mail():
    message = []
    ser = serial.Serial("/dev/ttyUSB0", 19200)
    # At the top of the hour, check the inbox for messages.
    # Add a line here that checks the time.
    establish_connection = "AT\r"
    ser.write(establish_connection)
    ans = ser.readline()
    if ans == "OK": # if the serial connection is successful
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
