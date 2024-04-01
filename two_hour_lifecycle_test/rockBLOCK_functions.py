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
    import serial
    import time
    
    # establish serial connection 
    ser = TRX_ser

    # At the top of the hour, check the inbox for messages.
    # Add line(s) here that check(s) the time. (Becca?)
    establish_connection = "AT\r"
    ser.write(establish_connection.encode("ascii"))
    establish_connection_input = ser.readline()
    # print(establish_connection_input.decode('utf-8').rstrip()) # this should say "AT"
    
    establish_connection_out = ser.readline()
    establish_connection_out = establish_connection_out.decode('utf-8').rstrip()
    # print(establish_connection_out) # this should say "OK"
    
    if establish_connection_out == "OK": # if the serial connection is successful
        print("success!")
        successful_transmission = 0 # assume the message has not yet successfully transmitted.
        
        write_msg = "AT+SBDWT=" + current_string + "\r" # request read/write status
        ser.write(write_msg.encode("ascii")) # write the message to the rockblock
        sbdwt_in = ser.readline() # should say the contents of write_msg
        sbdwt_out = ser.readline() # should say OK
        if sbdwt_out.decode('utf-8').rstrip() == "OK":
            number_of_attempts = 0
            while successful_transmission == 0 and number_of_attempts < 10:
                w = "AT+SBDIX\r" # start the transmission
                ser.write(w.encode("ascii"))
                if number_of_attempts > 0:
                    sbdix_0 = ser.readline()
                    sbdix_1 = ser.readline()
                    sbdix_in = ser.readline()
                else:
                    sbdix_in = ser.readline()
                
                sbdix_in = sbdix_in.decode('utf-8').rstrip()
                sbdix_out = ser.readline()
                sbdix_out = sbdix_out.decode('utf-8').rstrip()
                sbdix_out = sbdix_out[8:].split(",") # splits response up by commas
                number_of_attempts += 1
                # Detailed in the AT command reference
                mo_status = int(sbdix_out[0]) # should be 0-2
            
                # Ok this is all stuff to read commands from the ground station
                if mo_status < 3: # if the message was successfully transmitted
                    successful_transmission += 1
                else:
                    # print("Transmission unsuccessful, waiting 10 seconds\n")
                    time.sleep(20) # wait 20 seconds to try again
    if number_of_attempts > 10:
        print("Maximum attempts exceeded")

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

      if mailbox_status[3] == 1: 
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
