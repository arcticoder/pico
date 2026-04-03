# Raspberry Pi Pico — Single-Breadboard Project Series

A progressive series of experiments using one Raspberry Pi Pico and one
830-point breadboard.  Each stage builds directly on the previous one: the
same breadboard is reconfigured as new circuits are introduced.  Stages 1–5
are fully documented with MicroPython code, SPICE simulations, and step-by-step
breadboard wiring guides.  See [docs/inventory.md](docs/inventory.md) for the
complete component list; no extra purchases are required to complete stages 1–5.

---

## What is `diagram.json`?

`diagram.json` is a Wokwi circuit layout file (https://wokwi.com/).  It
defines the components and wiring for the online simulator.

### How to use it

1. Go to https://wokwi.com/projects/new
2. Replace the default `diagram.json` with the one from a project folder
3. Add `main.py` if the project has one
4. Run the simulation

---

## Schematics

Each project has a `schematic.png` generated from its `.spice` netlist.  To
regenerate any schematic after editing the netlist:

```bash
# from the repo root
python tools/spice_to_schematic.py led_single/test.spice
python tools/spice_to_schematic.py led_parallel/test2.spice
python tools/spice_to_schematic.py gpio_led_basic/gpio_led_basic.spice
python tools/spice_to_schematic.py gpio_button_timing/gpio_button_timing.spice
python tools/spice_to_schematic.py gpio_analog_sensing/gpio_analog_sensing.spice
```

Output is written as `schematic.png` in the same directory as the `.spice` file.
`tools/spice_to_schematic.py` uses **schemdraw** to parse SPICE `R`, `C`,
`V`, and `D` elements and render a schematic image.

---

## Running on real hardware

Requirements: Raspberry Pi Pico with MicroPython firmware, USB data cable.

### One-time firmware setup

1. Hold the BOOTSEL button on the Pico and plug into USB — it mounts as a
   drive.
2. Download the MicroPython UF2 from https://micropython.org/download/rp2/
3. Copy the UF2 onto the drive.  The Pico reboots into MicroPython.

### Running on WSL (Windows 11)

If you are running WSL on Windows 11, the Pico's USB serial port is not
automatically visible inside WSL.  You need `usbipd` on the Windows side:

```pwsh
# In a Windows PowerShell or CMD window (run once per session)
usbipd attach --busid <X-Y> --wsl --auto-attach
```

Replace `<X-Y>` with the bus ID shown by `usbipd list` for your Pico.  The
`--auto-attach` flag keeps the device attached if it resets.  When the
attachment succeeds, `/dev/ttyACM0` will appear inside WSL and `mpremote`
will find the device automatically.

Without this step you will see:

```bash
mpremote cp gpio_led_basic/main.py :main.py
# mpremote: no device found
```

### Upload code with mpremote

[mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) is
the official MicroPython CLI tool for file transfer and REPL access.

```bash
# Install (conda / pip)
pip install mpremote        # version 1.27.0 used here

# Copy a project's main.py to the Pico
mpremote cp gpio_led_basic/main.py :main.py

# List files on the Pico
mpremote ls

# Run a script without copying it (useful for testing)
mpremote run gpio_led_basic/main.py
```

To open the interactive REPL and see `print()` output:

```bash
mpremote repl
```

`mpremote repl` is an interactive session (exit with Ctrl-] or Ctrl-x).
Other `mpremote` sub-commands (`ls`, `cp`, `run`) are separate shell commands
— do **not** type them at the `>>>` REPL prompt.

The script stored as `main.py` on the Pico runs automatically on power-up.

---

## Stages (the project path)

Work through these stages in order.  Each stage has its own folder with simulation files and a breadboard
wiring guide; stages 3–5 also include a `README.md` and MicroPython code.  You can simulate
before building — run the ngspice script to predict voltages and
currents before placing a single component.

---

### Stage 1 — Static LED from 3.3 V rail (`led_single/`)

No firmware needed.  Validates that a 470 Ω resistor and a red LED draw a
safe current from the Pico's 3.3 V output pin when power is applied.

| File | Purpose |
|------|---------|
| `test.spice` | ngspice netlist — DC sweep 0 V → 3.3 V |
| `schematic.png` | Auto-generated schematic from `test.spice` |
| `breadboard.md` | Step-by-step wiring guide with wire selections |

---

### Stage 2 — Two parallel LEDs (`led_parallel/`)

Extends stage 1: two LED+resistor branches in parallel from the same 3.3 V
rail.  Confirms that two branches stay within safe current limits simultaneously.

| File | Purpose |
|------|---------|
| `test2.spice` | ngspice netlist |
| `schematic.png` | Auto-generated schematic |
| `breadboard.md` | Step-by-step wiring guide with wire selections |

---

### Stage 3 — GPIO-controlled LED (`gpio_led_basic/`)

First use of a GPIO pin: **GP17** drives a red LED via 220 Ω.  MicroPython
runs a blink loop.

| File | Purpose |
|------|---------|
| `main.py` | MicroPython blink loop |
| `diagram.json` | Wokwi circuit layout |
| `gpio_led_basic.spice` | ngspice netlist |
| `schematic.png` | Auto-generated schematic |
| `breadboard.md` | Step-by-step wiring guide |
| `README.md` | Build and run instructions |

---

### Stage 4 — Button input + LED timing (`gpio_button_timing/`)

Adds a push button on **GP16** with a 10 kΩ pull-down.  `main.py` turns the
LED on while the button is held and logs press/release timestamps to the REPL.

| File | Purpose |
|------|---------|
| `main.py` | MicroPython button-timing loop |
| `diagram.json` | Wokwi circuit layout |
| `gpio_button_timing.spice` | ngspice netlist |
| `schematic.png` | Auto-generated schematic |
| `breadboard.md` | Step-by-step wiring guide |
| `README.md` | Build and run instructions |

---

### Stage 5 — Analog sensing (voltage divider + ADC) (`gpio_analog_sensing/`)

Photoresistor voltage-divider platform.  **GP26/ADC0** reads the LDR midpoint;
**GP27/ADC1** reads a potentiometer calibration reference; **GP15** drives a
white LED as a controlled light source.  Optional I2C LCD 1602 displays live
readings.

| File | Purpose |
|------|---------|
| `main.py` | MicroPython ADC read + LCD display loop |
| `calibration.py` | Calibration helper script |
| `diagram.json` | Wokwi circuit layout |
| `gpio_analog_sensing.spice` | ngspice netlist (three LDR conditions swept) |
| `schematic.png` | Auto-generated schematic |
| `breadboard.md` | Step-by-step wiring guide with abbreviations and wire selections |
| `README.md` | Build, calibration, and noise-measurement guides |
| `docs/` | `calibration_guide.md`, `noise_measurement.md`, `drift_measurement.md` |

---

## Planned stages

These stages use only parts already in [docs/inventory.md](docs/inventory.md):

| Stage | Topic | Key new parts |
|-------|-------|---------------|
| 6 | PWM LED brightness control | LED (already have), 220 Ω (already have) |
| 7 | Interrupt-driven button input | Push button (already have), 10 kΩ (already have) |
| 8 | I2C LCD display | I2C LCD 1602 (already have — also used in stage 5) |

---

## Notes

- All circuits use 3.3 V logic
- GPIO pins are not 5 V tolerant
- Always use a current-limiting resistor with LEDs
- See [micropico/README.md](micropico/README.md) for device-level scripts
- See [docs/inventory.md](docs/inventory.md) for the full component list and
  wire catalogue

---

## Running simulations

Each stage folder contains an ngspice `.spice` netlist.  Run it with
`ngspice -b` to predict voltages and currents before building that stage.

```bash
# Stage 1 — static LED
ngspice -b led_single/test.spice

# Stage 2 — parallel LEDs
ngspice -b led_parallel/test2.spice

# Stage 3 — GPIO LED
ngspice -b gpio_led_basic/gpio_led_basic.spice

# Stage 4 — button timing
ngspice -b gpio_button_timing/gpio_button_timing.spice

# Stage 5 — analog sensing
ngspice -b gpio_analog_sensing/gpio_analog_sensing.spice
```

Run from the repo root.  Output goes to stdout with labeled column headers.

---

## Repo structure

```
led_single/
    test.spice          ngspice netlist
    schematic.png       auto-generated schematic
    breadboard.md       wiring guide

led_parallel/
    test2.spice         ngspice netlist
    schematic.png
    breadboard.md

gpio_led_basic/
    main.py             MicroPython blink loop
    diagram.json        Wokwi layout
    gpio_led_basic.spice
    schematic.png
    breadboard.md
    README.md

gpio_button_timing/
    main.py             MicroPython button-timing loop
    diagram.json
    gpio_button_timing.spice
    schematic.png
    breadboard.md
    README.md

gpio_analog_sensing/
    main.py             ADC read + LCD display
    calibration.py      calibration helper
    diagram.json
    gpio_analog_sensing.spice
    schematic.png
    breadboard.md
    README.md
    docs/
        calibration_guide.md
        noise_measurement.md
        drift_measurement.md

gpio_pwm_led/           (stage 6 — planned)
    bom.md

gpio_interrupt_button/  (stage 7 — planned)
    bom.md

gpio_i2c_lcd/           (stage 8 — planned)
    bom.md

micropico/
    main.py             general-purpose device entry point
    README.md

lib/
    lcd1602.py          I2C LCD 1602 driver
    ws2812.py           WS2812 RGB LED strip driver

docs/
    inventory.md        full component and wire catalogue

tools/
    spice_to_schematic.py   generate schematic.png from a .spice file
```
