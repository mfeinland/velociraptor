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

def check_mail():
  ser = serial.Serial("/dev/ttyUSB0", 19200)
  # At the top of the hour, check the inbox for messages.
  # Add a line here that checks the time.
  establish_connection = "AT\r"
  ser.write(establish_connection)
  ans = ser.readline()
  if ans == "OK": # if the serial connection is successful
  # Execute Send/Receive
  ser.write(AT+SBDIX\r)
  # Receive response 
  +SBDIX: 0, 1, 1, 1, 6, 8\r
  OK\r
  # Transfer "Hello1" message to your controller 
  AT+SBDRT\r
  # Receive response
  +SBDRT:\r
  Hello1\r
  OK\r
