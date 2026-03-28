# Drift Measurement Guide

Drift is a *slow* baseline shift in readings over time when the input is
constant. It reveals thermal effects, component warm-up, or power-supply
instability — all of which degrade long-term measurement quality.

---

## What you're measuring

With the sensor at a **fixed, constant** illumination level, readings should
stay the same. Any trend (up or down) over minutes is drift.

Common sources:
* Resistor self-heating (especially the 10 kΩ fixed resistor)
* LDR temperature coefficient
* Pico internal temperature affecting ADC reference
* Breadboard contact resistance changing with temperature

---

## Setup

1. Place the circuit in a stable location (not in direct sunlight or near a vent)
2. Keep the LED (GP15) **off**, or tape it at a fixed position
3. Allow 5 minutes for warm-up before logging — especially if USB was just connected

---

## Running the measurement

```python
from calibration import measure_drift
log = measure_drift(adc_pin=26, duration_s=120, interval_s=5)
```

This samples every 5 seconds for 2 minutes. Output:

```
Drift measurement: 120s, sampling every 5s
time_s     voltage
   0.0      1.0978
   5.0      1.0981
  10.0      1.0979
  ...
```

---

## Interpreting the result

| Peak-to-peak drift (V) | Quality | Notes |
|------------------------|---------|-------|
| < 0.5 mV / 2 min       | Excellent | Suitable for precise calibration |
| 0.5–2 mV / 2 min       | Acceptable | Calibrate quickly after warm-up |
| > 2 mV / 2 min         | Poor | Investigate heating; consider averaging |

---

## Correcting for drift

If drift is monotonic (always increasing or decreasing), a simple linear
de-trending works:

```python
# Fit and subtract a line
n  = len(log)
t  = [row[0] for row in log]
v  = [row[1] for row in log]
slope  = (v[-1] - v[0]) / (t[-1] - t[0])
offset = v[0]
corrected = [row[1] - (slope * row[0] + offset) + v[0] for row in log]
```

---

## Warm-up protocol

For precision measurements:
1. Power up the Pico
2. Wait 5 minutes before logging any calibration data
3. Record the drift log first; if drift < 1 mV/2 min, proceed to calibration
4. If drift is high, record a baseline and subtract it from subsequent data

---

## Repeatability check

After drift is confirmed acceptable: block the LDR, wait 30 seconds, unblock.
Repeat five times. The reading should return to the same value (±noise floor)
each time. If it does not, the circuit has memory effects or mechanical
hysteresis (connector oxidation, etc.).
