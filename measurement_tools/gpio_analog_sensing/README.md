# gpio_analog_sensing

**Read, stabilize, and interpret analog signals from resistance-based sensors.**

This is the foundational measurement platform for the pico/ project —
establishing noise floor, calibration discipline, and stable ADC readout
before advancing to amplification stages or modulated detection experiments.

---

## What this builds

| Layer | Component | Purpose |
|-------|-----------|---------|
| Sensor | Photoresistor (LDR) + 10 kΩ + 100 nF | Voltage-divider with noise filtering |
| Calibration | Potentiometer on ADC1 | Known resistance sweep to verify math |
| Perturbation | White LED on GP15 | Repeatable controllable light source |
| Readout | I2C LCD 1602 + serial | Voltage, resistance, estimated lux |
| Analysis | `calibration.py` | Power-law fit, drift logging, noise report |

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | ADC read loop — prints and displays filtered voltage, resistance, lux |
| `calibration.py` | `NoiseReport`, `CalibrationCurve`, `measure_drift` utilities |
| `gpio_analog_sensing.spice` | SPICE netlist of voltage divider (3 operating conditions) |
| `gpio_analog_sensing.gc` | GnuCap batch simulation |
| `schematic.png` | Schematic diagram (run `tools/spice_to_schematic.py` to regenerate) |
| `breadboard.md` | Step-by-step physical wiring guide |
| `docs/noise_measurement.md` | Guide: characterising ADC noise |
| `docs/drift_measurement.md` | Guide: measuring and interpreting signal drift |
| `docs/calibration_guide.md` | Guide: building a calibration curve |

---

## Quick start

### 1. Run the simulation

```bash
gnucap -b measurement_tools/gpio_analog_sensing/gpio_analog_sensing.gc
```

Check `v(2)` (bright), `v(3)` (dim), `v(5)` (pot mid) match expected values.

### 2. Build the circuit

Follow `breadboard.md`.

### 3. Deploy and run

```bash
mpremote connect /dev/ttyACM0 run measurement_tools/gpio_analog_sensing/main.py
```

Output:
```
ADC_RAW    V_raw  V_filt   R_sens(Ω)    ~lux  V_pot
  21800    1.098   1.101        4987.   502.3  1.651
```

### 4. Characterise noise

```python
from calibration import NoiseReport
nr = NoiseReport(adc_pin=26)
nr.run()
```

Expected: std-dev < 5 counts (< 0.25 mV) when using the 100 nF filter.

### 5. Build a calibration curve

```python
from calibration import CalibrationCurve
cal = CalibrationCurve(adc_pin=26)

# With your torch/phone light at known distance:
cal.add_point(voltage=0.35, known_value=1000)   # bright ~1kΩ
cal.add_point(voltage=1.10, known_value=5000)   # room   ~5kΩ
cal.add_point(voltage=2.75, known_value=50000)  # dark   ~50kΩ
cal.fit()
print(cal.predict(1.50))   # estimated resistance at 1.5V
cal.save("cal_ldr.json")
```

---

## Minimal success criteria

Before moving on, verify you can:

- [ ] Predict voltage within ±5% from known resistance (voltage divider math)
- [ ] Reduce ADC noise std-dev measurably (with/without 100 nF cap)
- [ ] Produce a calibration curve with R² > 0.99
- [ ] Observe and explain drift over a 2-minute measurement window

---

## What this unlocks

Once calibrated:
- **Lock-in detection** — modulate LED with GP15 PWM; detect weak
  light-dependent signals above the noise floor
- **Low-noise amplification** — add transistor S8050/S8550 stage
- **Thermal measurements** — swap LDR for thermistor (or add both)
- **Optical experiments** — intensity vs. distance, filtering

---

## Schematic regeneration

```bash
python tools/spice_to_schematic.py measurement_tools/gpio_analog_sensing/gpio_analog_sensing.spice
```
