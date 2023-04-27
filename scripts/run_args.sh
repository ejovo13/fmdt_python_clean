#!/usr/bin/bash

K_TRIALS=150

echo "Spawning 10 processes"
for i in {1..10} ;
do
    ( /bin/python /home/ejovo/MAIN/S8/METEORIX/fmdt_scripts/ground_truth.py 1> "data_$i.txt" 2>/dev/null & );
done

# sleep 200 # K_TRIALS * 38s
# sleep 38 # K_TRIALS * 38s
sleep 6750 # K_TRIALS * 45s

echo "Processes finished!"

> "data_all.txt"

for i in {1..10} ;
do
    ( tail -n 3 "data_$i.txt" >> "data_all.txt");
done