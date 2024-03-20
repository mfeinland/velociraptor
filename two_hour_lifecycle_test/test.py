import os
from rockBLOCK_functions import *
from common_functions import *
import time

time.sleep(60)
message = check_mail() 
#variable = os.environ.get("TESTVARY")
#print(variable)

'''
f = open('/home/velociraptor/raptor_test/test_file.txt', "w")
f.write(message)
f.close() '''

write_file(message,'/home/velociraptor/raptor_test/test_file.txt')
