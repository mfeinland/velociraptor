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

def connect_to_rock(TRX_ser):
    
    # establish serial connection 
    ser = TRX_ser#serial.Serial("/dev/ttyUSB1", 19200)
    print(ser)

    # At the top of the hour, check the inbox for messages.
    # Add line(s) here that check(s) the time. (Becca?)
    establish_connection = "AT\r"
    ser.write(establish_connection.encode("ascii"))
    establish_connection_input = ser.readline()
    # print(establish_connection_input.decode('utf-8').rstrip()) # this should say "AT"
    
    establish_connection_out = ser.readline()
    check = establish_connection_out.decode('utf-8').rstrip()
    # print(establish_connection_out) # this should say "OK"
    
    ahh = "AT&K0\r"
    ser.write(ahh.encode("ascii"))
    ahh2 = ser.readline()
    ahh_out = ser.readline()
    check = ahh_out.decode('utf-8').rstrip()
    return check

def send_string(current_string, TRX_ser):
    # establish serial connection 
    # TRX_ser = serial.Serial("/dev/ttyUSB0", 19200)
    
    # At the top of the hour, check the inbox for messages.
    # Add a line here that checks the time. 
      # - this would actually be in the main script - becca
    establish_connection = "AT\r"
    TRX_ser.write(establish_connection.encode("ascii"))
    ans = TRX_ser.readline()
    if ans == "OK": # if the serial connection is successful
        successful_transmission = 0
        while successful_transmission == 0:
            write_msg = "AT+SBDWT=" + current_string + "\r" # request read/write status
            TRX_ser.write(write_msg)
            sbdix_ans1 = TRX_ser.readline()
            if sbdix_ans1 == "OK":
                TRX_ser.write("AT+SBDIX\r")
                sbdix_ans = TRX_ser.readline()
                sbdix_ans = sbdix_ans[8:].split(",") # splits response up by commas
                
                # Detailed in the AT command reference
                mo_status = sbdix_ans[0] # should be 0-2
            
                # Ok this is all stuff to read commands from the ground station
                if int(mo_status) < 3: # if the message was successfully transmitted
                    successful_transmission += 1
                else:
                    time.sleep(10) # wait 10 seconds to try again

def check_mail(TRX_ser):
    message = []
    check = connect_to_rock(TRX_ser)
    
    if check == "OK": # the serial connection is successful
      # Execute Send/Receive
      TRX_ser.write("AT+SBDIX\r")
      # Receive response 
      # +SBDIX: 0, 1, 1, 1, 6, 8\r
      mailbox_status = TRX_ser.readline()
      mailbox_status = mailbox_status.split(',')
      # OK\r

      if ans[3] == 1: 
          # Transfer "Hello1" message to your controller 
          TRX_ser.write("AT+SBDRT\r")
          message_end = 0 # flag down
          while message_end == 0:
            message.append(TRX_ser.readline())
            if "OK" in message:
               message_end = 1 # flag goes up
          # Receive response
          #+SBDRT:\r
          #Hello1\r
          #OK\r
      else:
        message = "None"

    return message 
