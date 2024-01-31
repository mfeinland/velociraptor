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
    for i in range(len(n)):
        # Determine whether to use battery log or not
        if lines[n[i] + 2].strip().lower() == "[debug] filename (battery): 210101.bat":
            gga_msg = lines[n[i] + 3]
            gsv_msg = lines[n[i] + 4]
        else:
            gga_msg = lines[n[i] + 2]
            gsv_msg = lines[n[i] + 3]

        # Extract time information from GGA message
        gga_split = gga_msg.split(",")
        h = float(gga_split[1][0:1])
        m = float(gga_split[1][2:3])
        s = float(gga_split[1][4:5])
        seconds_elapsed = 3600 * h + 60 * m + s
        # stringA = f"Hello, the value is: {seconds_elapsed}" ##### for debugging
        # print(stringA)

        # Extract information from GSV message
        gsv_split = gsv_msg.split(",")
        number_of_messages = int(gsv_split[1])
        lines_to_consider = range(n[i] + 3, n[i] + 3 + number_of_messages)
        print(lines_to_consider)

        # Process each message in the block
        for j in lines_to_consider:
            current_msg = lines[j].split(",")
            print(current_msg)
            #print(current_msg)
            sats_in_this_message = (len(current_msg) - 4) // 4

            # Process each satellite in the message
            for k in range(sats_in_this_message):
                f = 4 * k
                prn = int(current_msg[4 + f]) # pseudorandom number (identifier; useful for arcs)
                elev = float(current_msg[5 + f]) # elevation in degrees
                az = float(current_msg[6 + f]) # azimuth in degrees

                # Handle special case for the 4th satellite
                if k == 3:
                    # print(f"k {k}")
                    # print(f"j {j}")
                    snr_placehold = current_msg[7 + f]
                    last_index_of_snr = snr_placehold.find('*')
                    snr = float(snr_placehold[0:last_index_of_snr])
                if k==0 and j==6:
                    print(f"k 2nd {k}")
                    print(f"j 2nd {j}")
                    snr_placehold = current_msg[7 + f]
                    last_index_of_snr = snr_placehold.find('*')
                    snr = float(snr_placehold[0:last_index_of_snr])
                else:
                    # print(f"k in else {k}") ##### for debugging
                    # print(f"j in else {j}") ##### for debugging
                    snr = float(current_msg[7 + f])

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