# Noise Measurement Guide

A clean noise characterisation is the first thing to do before any
measurement experiment. Without knowing your noise floor, you cannot tell
signal from artifact.

---

## What you're measuring

ADC noise = rapid, random variation in readings when the input is held steady.
Sources include:

* ADC quantisation (±½ LSB fundamental)
* Thermal (Johnson) noise in resistors
* Power-supply ripple coupling into VREF
* Ground bounce from high-frequency Pico operations
* Mains-frequency pickup (50/60 Hz) in long wires

---

## Equipment setup

1. Circuit wired as per `breadboard.md`
2. LED (GP15) **off** — eliminate self-generated light variation
3. Cover the photoresistor with a piece of opaque black tape or a coin
4. Do not touch the breadboard while measuring

---

## Running the measurement

Open a mpremote/rshell REPL session and run:

```python
from calibration import NoiseReport
nr = NoiseReport(adc_pin=26, n_samples=500)
report = nr.run()
```

Sample output:

```
--- Noise Report ---
  Samples    : 500
  Mean       : 21803.4 counts  (1.0978 V)
  Std-dev    : 3.72 counts  (0.187 mV)
  SNR        : 5865.4
```

---

## Interpreting the result

| Std-dev (counts) | Quality | Notes |
|-----------------|---------|-------|
| 1–3             | Excellent | Near quantisation limit |
| 3–8             | Good | Typical with 100 nF filter |
| 8–20            | Fair | Consider longer wire, better ground |
| > 20            | Poor | Check power supply, shielding |

---

## Effect of the 100 nF filter capacitor

Run the test twice — once with the capacitor fitted, once without:

```
Without cap: std-dev ≈ 15–25 counts
With 100 nF: std-dev ≈ 3–8 counts
```

Record both values. The difference is your filter improvement factor.

---

## What to do with this result

* Record std-dev in your experiment notes as the **noise floor**
* Signals smaller than ~3× the noise floor will be unreliable
* If noise is high, try: shorter wires, twist signal + ground pair, add
  10 Ω series resistor at ADC pin, move Pico USB away from signal wires

---

## Periodic noise (mains hum)

If you see a 50/60 Hz oscillation, it means your circuit is picking up mains
EMI. Remedies: shorter signal wire, capacitor closer to ADC pin, ferrite bead
on signal line, avoid running wires near power adaptors.

To detect it, log 1000 samples at ~1 ms intervals and look for a cyclic pattern.
