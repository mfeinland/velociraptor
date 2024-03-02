from rockBLOCK_functions import send_string
import time
from datetime import datetime

for i in range(20):
    time_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = "This is message number " + str(i)
    send_string(message)
    time.sleep(10) # seconds
    