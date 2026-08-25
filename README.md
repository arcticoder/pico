# Raspberry Pi Pico — Circuits & Experiments

A general-purpose collection of Raspberry Pi Pico circuits: MicroPython
code, SPICE netlists, and breadboard wiring guides, organized by category.
See [docs/inventory.md](docs/inventory.md) for the component list.

This repo is the general-purpose Pico infrastructure for the sibling
[arcticoder/lab](https://github.com/arcticoder/lab) repo, which builds
project-specific circuits (currently a physics-instrumentation lab bench)
on top of the patterns established here — see its
[spacetime_circuits_dependency.md](https://github.com/arcticoder/lab/blob/main/docs/spacetime_circuits_dependency.md)
and
[general_purpose_circuit_dependency.md](https://github.com/arcticoder/lab/blob/main/docs/general_purpose_circuit_dependency.md)
for where these circuits fit into a larger build.

---

## Schematics

Each project has a `schematic.png` generated from its `.spice` netlist.
`schematic.png` is **not committed** (see `.gitignore`) — it's a build
artifact, regenerated on demand:

```bash
# from the repo root
python tools/spice_to_schematic.py measurement_tools/gpio_analog_sensing/gpio_analog_sensing.spice
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
mpremote cp measurement_tools/gpio_analog_sensing/main.py :main.py
# mpremote: no device found
```

### Upload code with mpremote

[mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) is
the official MicroPython CLI tool for file transfer and REPL access.

```bash
# Install (conda / pip)
pip install mpremote        # version 1.27.0 used here

# Copy a project's main.py to the Pico
mpremote cp measurement_tools/gpio_analog_sensing/main.py :main.py

# List files on the Pico
mpremote ls

# Run a script without copying it (useful for testing)
mpremote run measurement_tools/gpio_analog_sensing/main.py
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

## Circuits (built)

Each circuit folder has MicroPython code (where applicable), a SPICE
netlist, a breadboard wiring guide, and a README.

| Folder | Circuit | Category |
|--------|---------|----------|
| `leds/led_single/` | Single LED + 470 Ω, static 3.3 V test | LEDs |
| `leds/led_parallel/` | Two parallel LEDs, 470 Ω each, 3.3 V | LEDs |
| `leds/gpio_led_basic/` | Pico GP17 → 220 Ω → LED, MicroPython blink loop | LEDs |
| `buttons/gpio_button_timing/` | Button input + LED, press/release timing | Buttons |
| `measurement_tools/gpio_analog_sensing/` | Voltage divider + ADC measurement, calibration, noise/drift analysis | Measurement tools |

### `measurement_tools/gpio_analog_sensing/` — Voltage divider + ADC measurement

The most complete stage here.  A resistor divider feeds **GP26/ADC0**; a
potentiometer provides a calibration reference on **GP27/ADC1**.  Optional
I2C LCD 1602 displays live readings.

| File | Purpose |
|------|---------|
| `main.py` | MicroPython ADC read + LCD display loop |
| `calibration.py` | Calibration helper script |
| `gpio_analog_sensing.spice` | ngspice netlist (three divider conditions swept) |
| `schematic.png` | Auto-generated schematic |
| `breadboard.md` | Step-by-step wiring guide with abbreviations and wire selections |
| `README.md` | Build, calibration, and noise-measurement guides |
| `docs/` | `calibration_guide.md`, `noise_measurement.md`, `drift_measurement.md` |

---

## Planned circuits

Parts already in [docs/inventory.md](docs/inventory.md) cover the next few
stages below. `hv_divider_adc/` requires a high-voltage supply (not yet
acquired).

| Folder | Circuit |
|--------|---------|
| `leds/gpio_pwm_led/` | PWM signal output — duty cycle controls LED brightness |
| `measurement_tools/gpio_i2c_mpu6050/` | I2C IMU — MPU6050, deflection/vibration measurement |
| `displays/gpio_i2c_lcd/` | I2C LCD live display |
| `buttons/gpio_interrupt_button/` | Interrupt-driven button input, no polling |
| `measurement_tools/hv_divider_adc/` | HV divider + ADC — reads high voltages safely via a precision resistor divider |

---

## Notes

- All circuits use 3.3 V logic; GPIO pins are not 5 V tolerant
- The `hv_divider_adc/` stage involves higher-voltage signals — do not
  proceed until appropriate safety precautions are in place
- See [micropico/README.md](micropico/README.md) for device-level scripts
- See [docs/inventory.md](docs/inventory.md) for the full component list and
  wire catalogue

---

## Running simulations

Circuit folders with an ngspice `.spice` netlist can be simulated before
building.  Run with `ngspice -b` to predict voltages and currents.

```bash
# Voltage divider + ADC
ngspice -b measurement_tools/gpio_analog_sensing/gpio_analog_sensing.spice

# LED circuits
ngspice -b leds/led_single/test.spice
ngspice -b leds/led_parallel/test2.spice
ngspice -b leds/gpio_led_basic/gpio_led_basic.spice

# Button timing
ngspice -b buttons/gpio_button_timing/gpio_button_timing.spice
```

Run from the repo root. Output goes to stdout with labeled column headers.

---

## Repo structure

```
leds/
    led_single/          static 3.3 V LED test (built)
    led_parallel/         two parallel LEDs, 3.3 V (built)
    gpio_led_basic/        Pico GP17 → 220 Ω → LED, MicroPython blink (built)
    gpio_pwm_led/           PWM brightness control (planned)

buttons/
    gpio_button_timing/    button input + LED, press/release timing (built)
    gpio_interrupt_button/ interrupt-driven button input (planned)

measurement_tools/
    gpio_analog_sensing/   voltage divider + ADC + calibration (built)
        main.py             ADC read + LCD display
        calibration.py      calibration helper
        gpio_analog_sensing.spice
        schematic.png
        breadboard.md
        README.md
        docs/
            calibration_guide.md
            noise_measurement.md
            drift_measurement.md
    gpio_i2c_mpu6050/      I2C IMU (planned)
    hv_divider_adc/        HV divider + ADC (planned; requires HV supply)

displays/
    gpio_i2c_lcd/          I2C LCD 1602 display (planned)

micropico/
    main.py             general-purpose device entry point
    README.md

lib/
    lcd1602.py          I2C LCD 1602 driver
    ws2812.py           WS2812 RGB LED strip driver

docs/
    inventory.md        full component and wire catalogue
    kb/                 process notes for future LLM sessions, not end-user docs

tools/
    spice_to_schematic.py   generate schematic.png from a .spice file
```
