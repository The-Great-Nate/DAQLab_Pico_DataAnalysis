# `Data Acquisition Investigation with a Raspberry Pi Pico`

_Install instructions adapted from Stoyan Trilov and Sudan Paramesvaran._
This repository includes a project showing an example of how to use Raspberry Pi Pico functionality in a DAQ context.

## Build instructions

1. Install VS Code and relevant dependencies by following the instructions in Chapter 2 and 3 of the [Raspberry Pi Pico Getting Started Guide](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf).

    1. If using Windows, download [git for Windows](https://git-scm.com/downloads/win), which will give you access to git commands and bash emulation. Alternatively, you could use the Windows Subsystem for Linux.
2. Create, and move into a project directory for the DAQ Lab.
```
mkdir pico_daq_lab
cd pico_daq_lab
```
3. Get a copy of the Pico DAQ repository (foundation taken from this repo)
```
git clone https://github.com/sparamesvaran/PHYS30033_DAQ_24_25.git
cd PHYS30033_DAQ_24_25
```

4. Import the newly cloned project using the Raspberry Pi Pico extension.
    1. Open the extension from the right-hand toolbar
    2. Click `Import Project`, and set the `Location` field to the correct directory of the cloned DAQ repository. 
    3. Click `Import`. A new window should open, and VS Code will begin to download the Pico SDK and requisite tools.

5. Build the DAQ project by clicking the `Compile` button in the blue ribbon of VS Code, which should now be available. The compilation output should now be under `build/onboard_temp_daq`.

## Pico programming instructions

1. Hold down the `BOOTSEL` button on Pico
2. Plug the Pico micro-controler  into a computer using the micro-USB cable. A USB mass storage device, named `RPI-RP2` should appear.
3. Copy the desired `.uf2` file (e.g.: `build/onboard_temp_daq/onboard_temp_daq.uf2`) to `RPI-RP2` (i.e. the Pico). This should cause the Pico to reboot, and start running the code in the binary file.
