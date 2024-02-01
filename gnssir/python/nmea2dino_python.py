import numpy as np

def nmea2dino(): # setting it up as a method will help to do user input later
    # Read lines from the file
    lines = open("WESL001021.txt").readlines()

    # Define the start pattern
    start_pat = "210101.log"
    
    # Find indices of lines that start messages
    n = [i for i, line in enumerate(lines) if line.strip() == start_pat]

    # Initialize the snr_file matrix
    snr_file = np.zeros((len(n) * 13, 5))
    instances_counter = 0

    # Process each message block
#     for i in n:
    for i in [0, 9, 18]:
        # Determine whether to use battery log or not
        if lines[i + 2].strip().lower() == "[debug] filename (battery): 210101.bat":
            debug = 1
            gga_msg = lines[i + 3]
            gsv_msg = lines[i + 4]
        else:
            debug = 0
            gga_msg = lines[i + 2]
            gsv_msg = lines[i + 3]

        # Extract time information from GGA message
        gga_split = gga_msg.split(",")
        h = float(gga_split[1][0:1])
        m = float(gga_split[1][2:3])
        s = float(gga_split[1][4:5])
        seconds_elapsed = 3600 * h + 60 * m + s

        # Extract information from GSV message
        gsv_split = gsv_msg.split(",")
        number_of_messages = int(gsv_split[1])
        lines_to_consider = range(i + 3 + debug, i + 3  + debug + number_of_messages)

        # Process each message in the block
        for j in lines_to_consider:
            current_msg = lines[j].split(",")
            sats_in_this_message = (len(current_msg) - 4) // 4
            # Process each satellite in the message
            for k in range(sats_in_this_message):
                f = 4 * k
                try:
                    prn = int(current_msg[4 + f]) # pseudorandom number (identifier; useful for arcs)
                except:
                    prn = None
                try:
                    elev = float(current_msg[5 + f]) # elevation in degrees
                except:
                    elev = None
                try:
                    az = float(current_msg[6 + f]) # azimuth in degrees
                except:
                    az = None
                # Handle special case for the 4th satellite
                if k == 3:
                    snr_placehold = current_msg[7 + f]
                    last_index_of_snr = snr_placehold.find('*')
                    try: # these try-except blocks handle the cases in which there is no SNR data
                        snr = float(snr_placehold[0:last_index_of_snr])
                    except:
                        snr = None
                elif k == 0 and j == lines_to_consider[-1]:
                    snr_placehold = current_msg[7 + f]
                    last_index_of_snr = snr_placehold.find('*')
                    try:
                        snr = float(snr_placehold[0:last_index_of_snr])
                    except:
                        snr = None
                else:
                    try:
                        snr = float(current_msg[7 + f])
                    except:
                        snr = None

                # Populate the snr_file matrix
                snr_file[instances_counter, :] = [seconds_elapsed, prn, elev, az, snr]
                instances_counter += 1

    # Trim the snr_file matrix to the actual data
    snr_file = snr_file[:instances_counter, :]
        
    try:
        np.savetxt("snrdata.txt", snr_file)
        print("File saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

nmea2dino()


# In[ ]:




