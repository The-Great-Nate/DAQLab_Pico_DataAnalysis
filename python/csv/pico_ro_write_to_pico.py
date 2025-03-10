#!/usr/bin/python3

import serial
import sys
import time
from datetime import datetime

def temperature_readout(target, time_create):

        #device_name='COM6'
        #serial_device = serial.Serial(device_name)  # open serial port

        # event counter
        n=1

        # csv file
        f_csv = open(f"temp_data_{target}_entries_{time_create}.csv", "w")

        while n<=target:
                line = serial_device.readline()
                recieved_timestamp = int(time.time() * 1000000)
                text = line.decode()
                
                # extract data
                words = text.split()
                timestamp = int(words[3]) - elapsed_time_microseconds
                temperature = words[5]

                data_string=f"{timestamp},{temperature},{recieved_timestamp}"

                # csv
                f_csv.write(data_string+"\n")


                n+=1

        f_csv.close()

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

        device_name='COM6'
        serial_device = serial.Serial(device_name, baudrate = 115200, timeout = 0.5)  # open serial port
        


        start_time = int(time.time() * 1000000)
        while True:
                green_light = serial_device.readline().strip().decode()
                if str(green_light) == "START_MEASURING...":
                        print("DAQ Computer received the message: START_MEASURING...")
                        ref_time_write = str(int(time.time() * 1000000)) + "n"
                        for byte in ref_time_write.encode():
                                while True:
                                        serial_device.write(byte.to_bytes(1, "little"))
                                        serial_device.flush() 
                                        pico_msg = serial_device.readline().strip().decode()
                                        if pico_msg == f"Received bit: {chr(byte)}":
                                                break

                                '''
                                pico_msg = serial_device.readline().strip().decode()
                                if pico_msg == "Reference_Time_Recieved":
                                        print(f"Pico acknowledged the reference time: {ref_time_write}")
                                        break
                                '''
                        break
                        
                else:
                        print(f"Unexpected data: {green_light}")

        end_time = int(time.time() * 1000000)
        elapsed_time_microseconds = (end_time - start_time)

        timestamp_file = open(f"ref_time_write_times.csv", "a")
        timestamp_file.write(f"{elapsed_time_microseconds}\n")
        timestamp_file.close()

        if n_arg == 4:
                start = int(sys.argv[1])
                stop = int(sys.argv[2])
                step = int(sys.argv[3])
                actual_stop=(stop//step)*step
                print(f"I will take datasets with the number of events ranging from {start} to {actual_stop}, in steps of {step}")
                n_events_range=range(start,stop,step)
                for n in n_events_range:
                        print(f"I will read {n} events")
                        temperature_readout(n, formatted_time)
        elif n_arg == 2:
                n=int(sys.argv[1])
                print(f"I will read {n} events")
                temperature_readout(n, formatted_time)
        elif n_arg == 1:
                temperature_readout(float('inf'), formatted_time)
        else:
                print(f"Invalid number of arguments: {n_arg}")
