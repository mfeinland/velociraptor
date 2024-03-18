#!bin/bash

update_time=$(python3 path/get_time)

sudo date -s $update_time

python3 path/onsite_main_script.py