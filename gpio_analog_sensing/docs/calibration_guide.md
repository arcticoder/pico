# Calibration Guide

A calibration curve converts a raw ADC voltage into a meaningful physical
quantity (resistance, lux, temperature). Without it you have numbers; with
it you have measurements.

---

## Prerequisites

1. Noise floor measured and confirmed acceptable (see `noise_measurement.md`)
2. Drift confirmed < 1 mV / 2 min (see `drift_measurement.md`)
3. Warm-up time completed (≥ 5 minutes)

---

## Theory: voltage divider

```
3V3 ─── R_fixed(10kΩ) ─── V_mid ─── R_sensor ─── GND
```

At V_mid:

```
V_mid = 3.3 × R_sensor / (R_fixed + R_sensor)
```

Rearranged for R_sensor from V_mid:

```
R_sensor = R_fixed × V_mid / (3.3 − V_mid)
```

This is exact (given ideal components). Test it first with the potentiometer.

---

## Step 1 — Verify with the potentiometer

Use the potentiometer on GP27 (ADC1) as a known variable resistance:

1. Turn pot to minimum (≈ 0 Ω) → `V_pot` should be ≈ 0 V
2. Turn pot to maximum (≈ 10 kΩ) → `V_pot` should be ≈ 1.65 V
   (voltage divider: 10k/20k × 3.3 = 1.65 V)
3. Calculate predicted `V_mid` at several pot positions and compare to
   the live `V_pot` reading in `main.py`

If predicted ≠ measured by > 5%, your `R_fixed` may not be exactly 10 kΩ.
Measure it with a multimeter and update `R_FIXED` in `main.py`.

---

## Step 2 — Collect calibration points for the LDR

You need at least **3 points** across the operating range.
More is better; 5–8 is ideal.

### Method A — darkness/light control

| Condition | How to achieve |
|-----------|----------------|
| Very bright | Hold torch directly at LDR (2–3 cm) |
| Room light | Normal indoor overhead lighting |
| Dim | Tent the LDR with a cup |
| Dark | Opaque tape over LDR |

For each condition, call:

```python
from calibration import CalibrationCurve
cal = CalibrationCurve(adc_pin=26)
cal.capture_point(known_value=100)    # very bright → ~100 lux estimate
cal.capture_point(known_value=500)    # room light  → ~500 lux
cal.capture_point(known_value=5000)   # dim         → ~5000 lux? use resistance instead
```

### Method B — known resistance (more precise)

Temporarily replace the LDR with a known resistor from your kit and record
(voltage, resistance) pairs. Then fit the curve in resistance space and
apply it to LDR readings.

```python
# Replace LDR with 1kΩ resistor:
cal.add_point(voltage=0.30, known_value=1000)
# Replace with 10kΩ:
cal.add_point(voltage=1.65, known_value=10000)
# Replace with 100kΩ:
cal.add_point(voltage=2.97, known_value=100000)
```

---

## Step 3 — Fit the curve

```python
cal.fit()
# Prints: Calibration fit: y = 8421.3 * V ^ 2.14
```

The power-law fit (y = A × V^B) is appropriate because LDR resistance vs.
illuminance is itself a power law. If residuals are large, try more points
in the under-represented range.

---

## Step 4 — Validate

Test against a known point **not** used in the fit:

```python
v_test = 0.55   # measured voltage with known condition
predicted = cal.predict(v_test)
print(f"Predicted resistance: {predicted:.0f} Ω")
```

Target: within 10% of known value.

---

## Step 5 — Save and use

```python
cal.save("cal_ldr.json")
```

Load in `main.py` by adding:

```python
from calibration import CalibrationCurve
cal = CalibrationCurve()
cal.load("cal_ldr.json")
# Then replace ldr_to_lux() with:
# calibrated_value = cal.predict(v_filtered)
```

---

## What next?

Once you have a working calibration curve:
- Step through the response curve at known light levels and verify monotonicity
- Measure **response time**: flash the LED on/off, log how fast `V_mid` changes
- Extend to the thermistor (if functional) using the same framework
- Upgrade to a **lock-in style measurement**: modulate the LED at a fixed
  frequency using PWM and filter for only that frequency in software —
  this dramatically improves SNR for weak signals
