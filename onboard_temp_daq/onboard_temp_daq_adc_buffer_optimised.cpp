/**
 * Copyright (c) 2021 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hardware/clocks.h"
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/rtc.h"
#include "pico/util/datetime.h"

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

    gpio_put(PICO_DEFAULT_LED_PIN, 1);
    unsigned char align = 0xAA;
    while (true)
    {
        // read the temperature from the ADC, and convert to a float
        uint16_t temperature = adc_read();

        // get the time at which the temperature data was obtained
        uint64_t sample_timestamp = time_us_64();

        // Write all data to buffer. before sending to DAQ
        uint8_t buffer[sizeof(align) + sizeof(sample_timestamp) + sizeof(temperature)];
        uint8_t *ptr = buffer; //Memory Location that points to buffer.

        memcpy(ptr, &align, sizeof(align));
        ptr += sizeof(align);

        memcpy(ptr, &sample_timestamp, sizeof(sample_timestamp));
        ptr += sizeof(sample_timestamp);

        memcpy(ptr, &temperature, sizeof(temperature));

        // SEND EVERYTHING
        fwrite(buffer, sizeof(buffer), 1, stdout);

    }
}