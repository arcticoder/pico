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

### gpio_led_basic
- First output test
- GPIO drives LED through a resistor

### gpio_button_timing
- Adds button input with pull-down resistor
- Logs timing of button presses
- Demonstrates basic input → output loop

---

## Notes

- All circuits use 3.3V logic
- GPIO pins are not 5V tolerant
- Always use a resistor with LEDs

---

## Structure

```

gpio_led_basic/
main.py
diagram.json

gpio_button_timing/
main.py
diagram.json

```

---

## Next steps

Planned progression:

- PWM signal generation
- Interrupt-driven input
- Timing measurement with external instruments
- Sensor integration
