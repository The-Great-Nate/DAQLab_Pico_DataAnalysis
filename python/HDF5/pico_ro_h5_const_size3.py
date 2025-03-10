#!/usr/bin/python3

import serial
import sys
import time
from datetime import datetime
import h5py

def temperature_readout(target, time_create, file_type):
    device_name = 'COM6'
    serial_device = serial.Serial(device_name)  # open serial port

    # event counter
    n = 1

    # open a h5 file
    file_name = f"temp_data_{target}_entries_{time_create}.{file_type}"
    with h5py.File(file_name, "w") as h5_file:
        time = h5_file.create_dataset("timestamp", shape=(target,), maxshape=(None,), dtype="i8")
        temp = h5_file.create_dataset("temperature", shape=(target,), maxshape=(None,), dtype="f8")
        clock_spd = h5_file.create_dataset("clock_speed", shape=(target,), maxshape=(None,), dtype="i8")


        while n < target:
                line = serial_device.readline()
                text = line.decode().strip()
                
                # extract data
                words = text.split(",")
                timestamp = int(words[0])
                temperature = float(words[1])
                clock_speed = int(words[2])

                time[n] = timestamp
                temp[n] = temperature
                clock_spd[n] = clock_speed

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
                        f_csv = open(f"file_write_times_clk.csv", "a")
                        f_csv.write(f"{file_type},{n},{elapsed_time_microseconds}\n")
                        f_csv.close()
        elif n_arg == 3:
                n=int(sys.argv[1])
                file_type = str(sys.argv[2])
                print(f"I will read {n} events")
                temperature_readout(n, formatted_time, file_type)
                end_time = int(time.time() * 1000000)
                elapsed_time_microseconds = (end_time - start_time)
                f_csv = open(f"file_write_times_clk.csv", "a")
                f_csv.write(f"{file_type},{n},{elapsed_time_microseconds}\n")
                f_csv.close()
        elif n_arg == 2:
                file_type = str(sys.argv[1])
                temperature_readout(float('inf'), formatted_time, file_type)
                end_time = int(time.time() * 1000000)
                elapsed_time_microseconds = (end_time - start_time)
                f_csv = open(f"file_write_times_clk.csv", "a")
                f_csv.write(f"{file_type},inf,{elapsed_time_microseconds}\n")
                f_csv.close()
        else:
                print(f"Invalid number of arguments: {n_arg}")


