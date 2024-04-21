from reflector_height import *
from nmea2dino import *
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

path = '/home/velociraptor/two_hour_lifecycle_test/'
dinofile = 'current_dino.csv'


file_name_list = []
for i in range(104, 110):
	for j in range(1, 17):
		file_name_list.append(f"nmea_file_2024_{i}_{j}")
		
del file_name_list[0:7]
del file_name_list[81:]

min_az = 90
max_az = 270
min_el = 5
max_el = 25
t_res = 2

h1vec = []
h2vec = []
tvec = []

# ~ file_name_list = ["nmea_file_2024_104_9", "nmea_file_2024_104_10"]

files2 = file_name_list[72:]
file_counter = 0
print(files2)
for fname in files2:
	print("doing nmea2dino")
	try:
		nmea2dino(path +'nmea_files/' + fname + ".txt", path + dinofile)
		parts = fname.split("_")
		doy = int(parts[3])
		timechunk = int(parts[4])
		print(f"working on file {file_counter} of {len(file_name_list)}") 
		# mins = (timechunk-1)*90 + 22.5
		tstmp1 = datetime(2024, 1, 1) + timedelta(days=(doy - 1), minutes=timechunk*90)
		# tstmp2 = tstmp1 + timedelta(minutes=45)
		try:
			heights = reflector_height(path + dinofile, min_az, max_az, min_el, max_el, t_res)
			h1vec.append(heights[0])
			h2vec.append(heights[1])
			tvec.append(tstmp1)
			
			# ~ if heights[0] is not None:
				# ~ hvec.append(heights[0])
				# ~ tvec.append(tstmp1)
			# ~ if heights[1] is not None:
				# ~ hvec.append(heights[1])
				# ~ tvec.append(tstmp2)

		except:
			heights = ["couldn't resolve height"]
		print(tvec, h1vec, h2vec)
		df = pd.DataFrame({'t': tvec, 'h1': h1vec, 'h2': h2vec})
		df.to_csv("reflheights2.csv", index=False)
		file_counter += 1
	except:
		pass
		# df.to_csv("reflheights.csv", mode='a', header=False, index=False)
		

df = pd.DataFrame({'t': tvec, 'h1': h1vec, 'h2': h2vec})
df.to_csv("reflheights2.csv", index=False)
