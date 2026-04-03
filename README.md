# Raspberry Pi Pico — Electrogravitics Research Platform

A measurement and control platform built toward electrogravitics experiments —
specifically the Biefeld-Brown effect (asymmetric capacitor lift) and related
force-production phenomena documented in Valone (2008).  Starting from the
SunFounder Thales Kit with no prior hardware or knowledge, each stage adds an
instrumentation or control capability that feeds directly into later high-voltage
work.  See [docs/inventory.md](docs/inventory.md) for the component list and
[docs/related/](docs/related/) for reference literature.

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
mpremote cp gpio_analog_sensing/main.py :main.py
# mpremote: no device found
```

### Upload code with mpremote

[mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) is
the official MicroPython CLI tool for file transfer and REPL access.

```bash
# Install (conda / pip)
pip install mpremote        # version 1.27.0 used here

# Copy a project's main.py to the Pico
mpremote cp gpio_analog_sensing/main.py :main.py

# List files on the Pico
mpremote ls

# Run a script without copying it (useful for testing)
mpremote run gpio_analog_sensing/main.py
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

Work through these stages in order.  Each stage adds a measurement or control
capability that feeds into later high-voltage electrogravitics work.  Completed
stages include MicroPython code, a SPICE netlist, and a breadboard wiring guide.

---

### Stage 5 — Voltage divider + ADC measurement (`gpio_analog_sensing/`)

**The foundational measurement stage.**  A resistor divider feeds **GP26/ADC0**;
a potentiometer provides a calibration reference on **GP27/ADC1**.  This is the
exact skill set needed in later stages when a precision resistor network steps a
kilovolt-range HV signal down to the Pico's 3.3 V ADC window.  Optional I2C
LCD 1602 displays live readings.

See Valone (2008) §3 for how Brown and Woodward relied on careful voltage
measurement to characterise the F(V) curve of their dielectric capacitors.

| File | Purpose |
|------|---------|
| `main.py` | MicroPython ADC read + LCD display loop |
| `calibration.py` | Calibration helper script |
| `diagram.json` | Wokwi circuit layout |
| `gpio_analog_sensing.spice` | ngspice netlist (three divider conditions swept) |
| `schematic.png` | Auto-generated schematic |
| `breadboard.md` | Step-by-step wiring guide with abbreviations and wire selections |
| `README.md` | Build, calibration, and noise-measurement guides |
| `docs/` | `calibration_guide.md`, `noise_measurement.md`, `drift_measurement.md` |

---

## Planned stages

Stages 6–8 use parts already in [docs/inventory.md](docs/inventory.md).
Stages 9–10 require a high-voltage supply (not yet acquired).

| Stage | Folder | Topic | Electrogravitics relevance |
|-------|--------|-------|----------------------------|
| 6 | `gpio_pwm_led/` | PWM signal output | Drives HV boost-converter control pins; sets pulse timing for Woodward-effect experiments |
| 7 | `gpio_i2c_mpu6050/` | I2C IMU — MPU6050 | Measures deflection and vibration during torsion-balance or hanging-lifter tests |
| 8 | `gpio_i2c_lcd/` | I2C LCD live display | Real-time voltage and thrust readout during experiments |
| 9 | `hv_divider_adc/` | HV divider + ADC | Reads 1–30 kV safely via precision resistor divider; pre-req for all HV experiments |
| 10 | `biefeld_brown_lifter/` | Asymmetric capacitor baseline | Biefeld-Brown effect: measure lift onset voltage and the F(V) curve |

---

## Notes

- All circuits use 3.3 V logic; GPIO pins are not 5 V tolerant
- Stages 9–10 involve kilovolt-range signals — **do not proceed until HV
  safety precautions are in place**; see [docs/related/](docs/related/) for
  voltage and current levels reported in the literature
- See [micropico/README.md](micropico/README.md) for device-level scripts
- See [docs/inventory.md](docs/inventory.md) for the full component list and
  wire catalogue
- See [docs/related/Valone2008/](docs/related/Valone2008/) for the primary
  reference on the Biefeld-Brown effect, asymmetric capacitors, and Woodward
  effect experimental apparatus

---

## Running simulations

Stage folders that have an ngspice `.spice` netlist can be simulated before
building.  Run with `ngspice -b` to predict voltages and currents.

```bash
# Stage 5 — voltage divider + ADC
ngspice -b gpio_analog_sensing/gpio_analog_sensing.spice
```

Run from the repo root.  Output goes to stdout with labeled column headers.
HV-stage netlists will be added as those stages are designed.

---

## Repo structure

```
gpio_analog_sensing/        stage 5 — voltage divider + ADC (completed)
    main.py             ADC read + LCD display
    calibration.py      calibration helper
    diagram.json        Wokwi layout
    gpio_analog_sensing.spice
    schematic.png
    breadboard.md
    README.md
    docs/
        calibration_guide.md
        noise_measurement.md
        drift_measurement.md

gpio_pwm_led/               stage 6 — PWM output (planned)
    bom.md

gpio_i2c_mpu6050/           stage 7 — I2C IMU (planned)

gpio_i2c_lcd/               stage 8 — I2C LCD display (planned)
    bom.md

hv_divider_adc/             stage 9 — HV divider ADC (planned; requires HV supply)

biefeld_brown_lifter/       stage 10 — Biefeld-Brown asymmetric capacitor (planned)

micropico/
    main.py             general-purpose device entry point
    README.md

lib/
    lcd1602.py          I2C LCD 1602 driver
    ws2812.py           WS2812 RGB LED strip driver

docs/
    inventory.md        full component and wire catalogue
    related/
        Valone2008/     primary reference — electrogravitics and Biefeld-Brown effect

tools/
    spice_to_schematic.py   generate schematic.png from a .spice file
```
