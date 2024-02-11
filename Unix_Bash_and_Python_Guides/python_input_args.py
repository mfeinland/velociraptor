## Guide/outline for python script that takes input arguments
#-------------------------------------------------------------
## Imports and libraries 
import os, sys

#-------------------------------------------------------------
## Functions 


#-------------------------------------------------------------
## Main function 
	# not necessarily needed, it just can make things look 
    # cleaner if there are a lot of functions
    
def main(): 
 	# Grab system input to script
    sys_args = sys.argv

    # Grab actual imput arguments. They start at index 1 
    # (index 0 is the name of the file that was run)
    imput_arg1 = sys_args[1] 
    # imput_arg2 = sys_args[2]
    # etc.
    
    # One way this script could be run from another python
    # script is the following, using the oc package:
    
    # os.system("python python_input_args.py arg1 arg2")
    
    # On the other hand, the script could run from a 
    # terminal or bash script like the following:
    
    # python3 python_input_args.py arg1 arg2

if __name__ == "__main__":
    main()