# Raspberry Pi Pico Experiments

Small, self-contained experiments using a Raspberry Pi Pico and breadboard components.

Each folder is an independent experiment with:
- `main.py` → MicroPython code that runs on the Pico
- `diagram.json` → circuit layout for Wokwi simulator

---

## What is `diagram.json`?

`diagram.json` is used by the Wokwi simulator:
https://wokwi.com/

It defines:
- components (Pico, LED, resistors, etc.)
- wiring (breadboard connections)

### How to use it

1. Go to https://wokwi.com/projects/new
2. Open the project settings
3. Replace the default `diagram.json` with the one from this repo
4. Add `main.py` if needed
5. Run the simulation

---

## Running on real hardware

Requirements:
- Raspberry Pi Pico
- MicroPython firmware installed
- USB connection

### Setup (one-time)

1. Hold BOOTSEL on the Pico
2. Plug into USB
3. Copy MicroPython UF2 from:
   https://micropython.org/download/rp2/

---

### Upload code

Using Thonny:

1. Open Thonny
2. Select:
```

MicroPython (Raspberry Pi Pico)

```
3. Open `main.py` from a project folder
4. Save it to the Pico as:
```

main.py

```

The script runs automatically after saving.

---

## Projects

### gpio_led_single/
Single red LED, 470 Ω resistor, 3.3 V supply.
SPICE: `gpio_led_single/test.spice` · GnuCap: `gpio_led_single/test.gc`

### gpio_led_parallel/
Two parallel LEDs, one 470 Ω each, 3.3 V supply.
SPICE: `gpio_led_parallel/test2.spice` · GnuCap: `gpio_led_parallel/test2.gc`

### gpio_led_basic/
First Pico GPIO output test: GP17 drives a red LED via 220 Ω.
See [gpio_led_basic/README.md](gpio_led_basic/README.md) for build and run
instructions.

### gpio_button_timing/
Adds button input (GP16, pull-down) and logs press/release timestamps.
See [gpio_button_timing/README.md](gpio_button_timing/README.md).

### gpio_analog_sensing/
Photoresistor voltage-divider platform with potentiometer calibration
reference and controlled white LED light source.
See [gpio_analog_sensing/README.md](gpio_analog_sensing/README.md) for
full build, calibration, and noise-measurement guides.

---

## Notes

- All circuits use 3.3 V logic
- GPIO pins are not 5 V tolerant
- Always use a resistor with LEDs
- See [micropico/README.md](micropico/README.md) for MicroPython device
  scripts and the component inventory

---

## Structure

```
gpio_led_single/
    test.spice  test.gc  schematic.png  breadboard.md

gpio_led_parallel/
    test2.spice  test2.gc  schematic.png  breadboard.md

gpio_led_basic/
    main.py  diagram.json  gpio_led_basic.spice  gpio_led_basic.gc
    schematic.png  breadboard.md  README.md

gpio_button_timing/
    main.py  diagram.json  gpio_button_timing.spice  gpio_button_timing.gc
    schematic.png  breadboard.md  README.md

gpio_analog_sensing/
    main.py  calibration.py  diagram.json
    gpio_analog_sensing.spice  gpio_analog_sensing.gc
    schematic.png  breadboard.md  README.md
    docs/  (calibration_guide.md  noise_measurement.md  drift_measurement.md)

micropico/
    main.py  README.md

lib/
    lcd1602.py  ws2812.py

docs/
    inventory.md

tools/
    spice_to_schematic.py
```

---

## Running simulations

Each `gpio_*/` directory has matching SPICE and GnuCap batch files.

```bash
# GnuCap (batch mode)
gnucap -b gpio_led_basic/gpio_led_basic.gc
gnucap -b gpio_button_timing/gpio_button_timing.gc
gnucap -b gpio_analog_sensing/gpio_analog_sensing.gc

# ngspice (batch mode)
ngspice -b gpio_led_basic/gpio_led_basic.spice
ngspice -b gpio_button_timing/gpio_button_timing.spice
ngspice -b gpio_analog_sensing/gpio_analog_sensing.spice
```

Run from the repo root. Output goes to stdout.

---

## Next steps

Planned progression:

| Stage | Topic | Key files |
|-------|-------|-----------|
| 1 | GPIO output (LED) | `gpio_led_basic/main.py` |
| 2 | GPIO input + timing (button) | `gpio_button_timing/main.py` |
| 3 | ADC / analog sensing | `gpio_analog_sensing/main.py` |
| 4 | PWM signal generation | (planned) |
| 5 | Interrupt-driven input | (planned) |
| 6 | I2C / SPI peripherals | (planned) |
