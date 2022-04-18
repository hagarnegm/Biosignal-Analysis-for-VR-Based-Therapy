"""
This script logs serial data to a csv file. It has
only been tested on linux. It takes 3 command line 
parameters. 

Usage:
    $ python3 log-serial.py -d [serial port] -b [baudrate] -o [output file]
"""

import argparse
import serial, io
import time
 
parser = argparse.ArgumentParser()
 
parser.add_argument("-b", "--baudrate", type=int)
parser.add_argument("-o", "--output")
parser.add_argument("-d", "--device")
 
args = parser.parse_args()

device   = args.device
baudrate = args.baudrate                   
output_path = args.output                

with serial.Serial(device,baudrate) as serialPort, open(output_path,'w', encoding="utf-8") as f:
    now = time.time()
    while(1):
        line = serialPort.readline().decode("utf-8", errors="ignore")
        curr_time = time.time() - now
        f.write(f"{curr_time}, {line}")          
        f.flush()        
