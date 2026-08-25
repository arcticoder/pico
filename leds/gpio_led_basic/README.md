# gpio_led_basic

Blinks a red LED connected to Pico **GP17** via a 220 Ω current-limiting
resistor.  This is the first GPIO output experiment.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | MicroPython blink loop |
| `gpio_led_basic.spice` | ngspice netlist |
| `gpio_led_basic.gc` | GnuCap batch script |
| `schematic.png` | Generated schematic image |
| `breadboard.md` | Step-by-step breadboard wiring |

---

## Build

Follow **[breadboard.md](breadboard.md)** for the physical wiring.  
Short version:

1. Seat the Pico on the breadboard (USB port up, cols 1–20).
2. Connect GND (Pico c3) → blue power rail.
3. Insert 220 Ω resistor: one leg to the green wire from GP17, the other
   toward the LED anode.
4. Insert LED (long leg = anode, short leg = cathode → GND rail).

---

## Run on hardware

Upload `main.py` to the Pico with Thonny or MicroPico:

```
Open main.py → Save to Pico as main.py
```

The LED blinks every 0.5 s.

---

## Simulate

```bash
# GnuCap — sweeps supply from 0 V to 3.3 V in 0.1 V steps
gnucap -b leds/gpio_led_basic/gpio_led_basic.gc

# ngspice — DC operating-point at 3.3 V
ngspice -b leds/gpio_led_basic/gpio_led_basic.spice
```

Run from the **repo root**.  GnuCap output columns (in order): supply
voltage, LED forward voltage, LED current `i(D1)`.  At 3.3 V the current
should be approximately **5.9 mA**.

---

## Expected behaviour

```
I = (3.3 V − 2.0 V) / 220 Ω ≈ 5.9 mA
```

Within the 20 mA LED limit and the Pico's 12 mA per-pin drive rating.
