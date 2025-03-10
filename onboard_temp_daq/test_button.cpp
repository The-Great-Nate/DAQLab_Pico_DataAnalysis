#include "pico/stdlib.h"
#include <stdio.h>

#define BUTTON_PIN 5  // GPIO 5 for the button

int main() {
    stdio_init_all();  // Initialize serial output (USB serial)

    // Initialize GPIO 5 (button) as input with a pull-up resistor
    gpio_init(BUTTON_PIN);           // Initialize GPIO pin
    gpio_set_dir(BUTTON_PIN, GPIO_IN);  // Set as input
    gpio_pull_up(BUTTON_PIN);        // Enable pull-up resistor

    printf("Press the button connected to GPIO 5.\n");

    while (true) {
        // Check the state of the button (GPIO 5)
        if (gpio_get(BUTTON_PIN) == 0) {  // Button is pressed (LOW)
            printf("Button is pressed!\n");
        } else {  // Button is not pressed (HIGH)
            printf("Button is not pressed.\n");
        }

        sleep_ms(500);  // Delay to avoid flooding the serial output
    }

    return 0;
}
