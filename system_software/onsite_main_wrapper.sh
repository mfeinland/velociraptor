#!bin/bash

update_time=$(python3 /home/velociraptor/two_hour_lifecycle_test/get_time)

sudo date -s $update_time

python3 /home/velociraptor/two_hour_lifecycle_test/onsite_main_script.py