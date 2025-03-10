_readme written by Stoyan Trilov_
# `Communicating with Pico using serial over USB`

With suitable compilation parameters, the `standard in/out` of a Pico, e.g. the output of `printf` can be received and or sent to a computer over the USB cable. The example `onboard_temperature_daq` project is already configured in this way. Below you will find instructions to monitor the incoming data.

## Windows instructions:

1. Download and install the application, `MobaXterm`, https://download.mobatek.net/2362023122033030/MobaXterm_Installer_v23.6.zip 

2. Once installed, open MobaXterm, and click `Session`->`Serial`

3. Under `Serial port`, you should be able to see a device similar to: `USB Serial Device (COM6)`. Select it, and click OK.

## Mac/Linux instructions:

1. The Pico should appear as an USB serial device under the `/dev` directory. For example, `/dev/tty.usbmodem11101`. Check that this is the case, and note down the device name.

2. Use screen, together with the device name from previous step, to view the incoming data: `screen /dev/tty.usbmodem11101`

<br>

# `Communicating with Pico using serial over USB in python`

In the previous section, you learnt how to communicate with the Pico using a dedicated application. In this section, you will learn how to receive the data using a python script.

1. Modify the `pico_ro.py` script with the correct device name as per the previous section.

2. Install the `pyserial` package into your python environment.

**N.B. It is highly recommended that you use a dedicated python environment, e.g. `venv` or `conda`, for this work.**
