/**
 * Copyright (c) 2021 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <stdio.h>
#include <cstdio>
#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <cstdlib>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/rtc.h"
#include "pico/util/datetime.h"
#include "pico/binary_info.h"

#include <vector>

/* Choose 'C' for Celsius or 'F' for Fahrenheit. */
#define TEMPERATURE_UNITS 'C'

/* References for this implementation:
 * raspberry-pi-pico-c-sdk.pdf, Section '4.1.1. hardware_adc'
 * pico-examples/adc/adc_console/adc_console.c */
float read_onboard_temperature(const char unit)
{

    /* 12-bit conversion, assume max value == ADC_VREF == 3.3 V */
    const float conversionFactor = 3.3f / (1 << 12);

    float adc = (float)adc_read() * conversionFactor;
    float tempC = 27.0f - (adc - 0.706f) / 0.001721f;

    if (unit == 'C')
    {
        return tempC;
    }
    else if (unit == 'F')
    {
        return tempC * 9 / 5 + 32;
    }

    return -1.0f;
}

int main()
{

    stdio_init_all();

    gpio_init(3);
    gpio_set_dir(3, GPIO_OUT);

    gpio_init(14);
    gpio_set_dir(14, GPIO_IN);
    gpio_pull_up(14);

#ifdef PICO_DEFAULT_LED_PIN
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
#endif

    /* Initialize hardware AD converter, enable onboard temperature sensor and
     *   select its channel (do this once for efficiency, but beware that this
     *   is a global operation). */
    adc_init();
    adc_set_temp_sensor_enabled(true);
    adc_select_input(4);

    std::string ref_time_str;
    long long ref_time;

    while (true)
    {
        printf("PUSH THE BUTTON TO START, ONLY IF CODE FROM pico_ro.py IS RUNNING\n");
        if (gpio_get(14) == 0)
        { // Button pressed (LOW state)
            printf("START_MEASURING...\n");
            break;
        }
        sleep_ms(100);
    }

    while (true)
    {
        if (fgetc(stdin) != EOF)
        {
            char recieved_bit = getchar();
            // printf("%c\n", recieved_bit);
            // printf("I_am_finding_reftime\n");
            printf("Received bit: %c\n", recieved_bit);
            // gpio_put(PICO_DEFAULT_LED_PIN, 1);
            if (recieved_bit == 'n')
            {
                gpio_put(PICO_DEFAULT_LED_PIN, 1);
                ref_time = atoll(ref_time_str.c_str());
                break;
            }
            else
            {
                ref_time_str += recieved_bit;
            }
        }
    }
    while (true)
    {
        // read the temperature from the ADC, and convert to a float
        float temperature = read_onboard_temperature(TEMPERATURE_UNITS);
        // get the time at which the temperature data was obtained
        uint64_t sample_timestamp = time_us_64();
        sample_timestamp += ref_time;

        // send the temperature data along with its timestamp
        printf("Onboard temperature @ %llu = %.02f %c\n", sample_timestamp, temperature, TEMPERATURE_UNITS);
    }
}