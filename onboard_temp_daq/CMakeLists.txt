add_executable(onboard_temp_daq
onboard_temp_daq_adc_buffer_optimised.cpp
        #test_button.cpp
        )

# Add pico_multicore which is required for multicore functionality
target_link_libraries(onboard_temp_daq
        pico_stdlib
        pico_multicore
        hardware_adc
        hardware_rtc
        hardware_uart
        hardware_gpio
        hardware_clocks
        )

pico_sdk_init()
pico_enable_stdio_usb(onboard_temp_daq 1)
pico_enable_stdio_uart(onboard_temp_daq 1)

# create map/bin/hex file etc.
pico_add_extra_outputs(onboard_temp_daq)