#!/usr/bin/python3

import serial
import sys
import time
from datetime import datetime
import struct

def temperature_readout(target, time_create, file_type):
    device_name = 'COM6'
    serial_device = serial.Serial(device_name)  # open serial port

    # event counter
    n = 1

    with open(f"temp_data_{target}_entries_{time_create}.{file_type}", "wb") as bin_file:


        while n <= target:
                while True:
                        marker = serial_device.read(1)
                        if marker == b'\xAA':  # Found syncro bit (hexademimal AA)
                                break

                timestamp_b = serial_device.read(8)
                if len(timestamp_b) != 8:
                       continue
                
                temperature_b = serial_device.read(4)
                if len(temperature_b) != 4:
                       continue
                
                # extract data
                #done above
                
                bin_file.write(timestamp_b)  # Write the raw 8 bytes for timestamp
                bin_file.write(temperature_b)

                n += 1

    print(f"Data saved to temp_data_{target}_entries_{time_create}.{file_type}")

if __name__ == '__main__':

        n_arg=len(sys.argv)

        now = datetime.now()
        day = now.day
        month = now.month
        year = now.year
        hour = now.hour
        minute = now.minute
        second = now.second
        formatted_time = f"{day:02d}{month:02d}{year % 100:02d}_{hour:02d};{minute:02d};{second:02d}"

        start_time = int(time.time() * 1000000)

        if n_arg == 5:
                start = int(sys.argv[1])
                stop = int(sys.argv[2])
                step = int(sys.argv[3])
                file_type = str(sys.argv[4])
                actual_stop=(stop//step)*step
                print(f"I will take datasets with the number of events ranging from {start} to {actual_stop}, in steps of {step}")
                n_events_range=range(start,stop,step)
                for n in n_events_range:
                        print(f"I will read {n} events")
                        temperature_readout(n, formatted_time, file_type)
                        end_time = int(time.time() * 1000000)
                        elapsed_time_microseconds = (end_time - start_time)
                        f_csv = open(f"file_write_times.csv", "a")
                        f_csv.write(f"{file_type}_struct,{n},{elapsed_time_microseconds}\n")
                        f_csv.close()
        elif n_arg == 3:
                n=int(sys.argv[1])
                file_type = str(sys.argv[2])
                print(f"I will read {n} events")
                temperature_readout(n, formatted_time, file_type)
                end_time = int(time.time() * 1000000)
                elapsed_time_microseconds = (end_time - start_time)
                f_csv = open(f"file_write_times.csv", "a")
                f_csv.write(f"{file_type}_struct,{n},{elapsed_time_microseconds}\n")
                f_csv.close()
        elif n_arg == 2:
                file_type = str(sys.argv[1])
                temperature_readout(float('inf'), formatted_time, file_type)
                end_time = int(time.time() * 1000000)
                elapsed_time_microseconds = (end_time - start_time)
                f_csv = open(f"file_write_times.csv", "a")
                f_csv.write(f"{file_type}_struct,inf,{elapsed_time_microseconds}\n")
                f_csv.close()
        else:
                print(f"Invalid number of arguments: {n_arg}")


