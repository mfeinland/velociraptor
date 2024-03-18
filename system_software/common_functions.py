import re
import sys
from receiver_functions import setFreq
from rockBLOCK_functions import send_string

# Function to read in file lines to variable
def read_file(filename):

    file = open(filename, 'r')
    lines = file.readlines()
    i = 0
    for line in lines:
        lines[i] = line.strip("\n")
        i = i+1
    file.close()
    return lines

# Function to write to file
def write_file(content,filename):
    f = open(filename, "r+")
    for item in content:
        f.write(str(item) + "\n")
    f.close()
    return

# Check battery level and electronics temperature 
def sys_health(TRX_ser):
	message = []
	# get battery level [units]
	bat_level = 0.3
   	# get system temperature [deg. C]
	temperature = 20

	# check battery level 
	if bat_level <= 0.2: # 20%?
		message.append("Battery level too low. Pausing ops for 2 hrs")
	
	# check system temperature 
	if temperature < -30: # degrees Celcius
		message.append("System temperature too cold. Pausing ops for 2 hrs")
	elif temperature > 55: # degrees Celsius 
		message.append("System temperature too hot. Pausing ops for 2 hrs")
		
	# send messages back if needed 
	if len(message[0]) > 1:
		for item in message:
			send_string(item)
			sys.exit() # if there are any issues (might change this for cold temp)
	
	return bat_level, temperature

# Interpret and execute command 
def command_interpreter(message, GNSS_ser):

    # read in setvars file with current configuration 
    set_vars = read_file('setvars.txt')

    cmd_list = message.split(";")
    for item in cmd_list:
        cmd = re.split('=|,', item)

        if cmd[0] == 'sf':
            # setfreq - set sampling frequency of GNSS reciever   
            setFreq(GNSS_ser, [cmd[1],cmd[1]], [0,1] )

            set_vars[0] = cmd[1] # does it still need to output this? 
                               # Yes, so it can be kept safe in the parameter file  

        elif cmd[0] == 'el':
            # setelrng - set elevation range for height computation 
            # limits: el from NMEA exists in [0,90] (deg.)
 
            set_vars[1] = cmd[1] # min_el
            set_vars[2] = cmd[2] # max_el

        elif cmd[0] == 'az':
            # setazrng - set azmuth range for usable reflections

            set_vars[3] = cmd[1] # min_az
            set_vars[4] = cmd[2] # max_az

        elif cmd[0] == 'mode':
            # calibration - system checks inbox every 5 minutes
            # normal - system checks inbox every 2 hours

            if cmd[1] == '0':
                set_vars[5] = 'calibration'
            elif cmd[1] == '1':
                set_vars[5] = 'normal'

        elif cmd[0] == 'tres':
            # settimeres - one height calculations every X minutes (integer)

            set_vars[6] = cmd[1] # time_res

        else:
            print("Error: command not defined in database")

    # Update parameter file 
    updated_vars = set_vars
    print(updated_vars)

    # update setvars file with new configuration 
    write_file(updated_vars, "setvars.txt")

    return set_vars[0], set_vars[1], set_vars[2], set_vars[3], set_vars[4], set_vars[5], set_vars[6]
