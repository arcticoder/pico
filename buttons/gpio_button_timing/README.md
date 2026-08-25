# gpio_button_timing

## Purpose
Button input controls LED and logs press timing.

## Hardware
- Raspberry Pi Pico
- LED + 220Ω resistor
- Pushbutton
- 10kΩ pull-down resistor

## Simulation
```bash
ngspice -b buttons/gpio_button_timing/gpio_button_timing.spice
```

## Run
Upload `main.py` to Pico as `main.py`.