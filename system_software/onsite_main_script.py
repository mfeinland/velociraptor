# onsite_main_script.py
# Date: 2/10/24
# Author: Rebecca Blum
# 
# Revisions: 
#   [name]       [date]       [notes]
#   R. Blum      2/10/24      initial script creation 
#
# Summary: 
#     
#
# Inputs:
#   [] 
#
# Outputs: 
#   []
#
# Limitations: 
#    
#
# Future edits: 
#   [issue]                               [status]                    [name]
#   
#
#------------------------------------------------------------------------------
#
# Import Packages and Libraries 
import re
import sys, os # maybe not os if we turn cmd interpreter into function
from common_functions import read_file, write_file
#from ops_functions import calibration_cycle, sys_health, check_mail

###########################################
# Functions 

def calibration_cycle(ser, bat_level, temperature):
	   N = 18 # 18*5 = 90 mins
	   for n in range(0,N)
        if n = 0: # send back longitude, latitude, battery health, and sys temp
			         # get longitude and latitude from NMEA file 
			         flag = 0
			         while flag == 0: # flag is down
				            # read in nmea lines
				            data = ser.readline()
				            # if line contains long/lat (GLL -- Geographic Position - Longitude/Latitude)
				            check = re.search("GLL", data)
				            if check:
					               flag = 1 # flag goes up
					               GLL_line = data.split(", ")
					               latitude = GLL_line[1] + GLL_line[2]
					               longitude = GLL_line[3] + GLL_line[4]

            # send message 
		          message = "long=" + str(longitude) + ",lat=" + str(latitude) + ",B=" + bat_level + ",T=" + temperature
            # send_string
		          send_string(message)
													
	       else:
            # check inbox
			         command = check_mail()
			
			         if command = no_message: # execute commands
				            sleep(5)
			         else:
   	            os.system("python command_interpreter.py " + command)
		              sleep(5)

def check_mail():
	# check inbox
	
def sys_health():
    message = []
	   # get battery level [units]
	   bat_level = 30
   	# get system temperature [deg. C]
	   temperature = 20

	   # check battery level 
	   if bat_level <= 10: # no idea what value or units this should be
		  message.append("Battery level too low. Pausing ops for 2 hrs")
	
	   # check system temperature 
	   if temperature < -30: # degrees Celcius
		  message.append("System temp. is too hot. Pausing ops for 2 hrs")
	   elif temperature > 55: # degrees Celsius 
		  message.append("System temp. is too cold. Pausing ops for 2 hrs")
		
	   # send messages back if needed 
	   if len(message[0]) > 1:
		      for item in message 
        send_string(item)
        sys.exit() # if there are any issues (might change this for cold temp)
	
    return bat_level, temperature

###########################################
# Main function 
def main():
	
    ser = os.environ.get("SERIAL")
    if ser == "None"
		      ser = cereal()
	
    set_vars = read_file('setvars.txt')
    freq = set_vars[0]
    el_mask = [set_vars[1], set_vars[2]]
    az_mask = [set_vars[3], set_vars[4]]
    mode = set_vars[5]
    timeres = set_vars[6]

    # Check mailbox 
    command = check_mail() # 0 if no mail
    # if command != 0:
    os.system("python command_interpreter.py " + command)
    # or make this a function: command_interpreter(command)

    # check system health 
    bat_level, temperature = sys_health()

    # if in calibration mode, run every 5 mins until n = N (so it stops in >1.5 hours)
    if mode == "calibration":
				    calibration_cycle(ser, bat_level, temperature)

    else: #normal ops (need to implement time resolution)
    #	time res idea: read in all available files? divide number of files by 
    # 	number of desired blocks  
        read_nmea()
		      nmea2dino()
		      heights = reflector_height()
    
        # check system health 
	       bat_level, temperature = sys_health()
    
        # send string to ground station 
	       send_string("H=" heights[0] + "B=" + bat_level + ",T=" + temperature)
								if len(heights) > 2

if __name__ == "__main__":
    main()
