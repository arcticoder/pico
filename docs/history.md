All 7 tasks complete. Here's a summary:

---

### ✅ Done

| Task | Result |
|------|--------|
| Install schemdraw | Installed into active conda env |
| Schematic script | spice_to_schematic.py — parses V/R/D elements, renders LED symbols |
| `test2.spice` | test2.spice — two parallel LED branches off the same 3.3 V rail |
| `led_test2.gc` | led_test2.gc — sweeps 0→3.3 V, prints `v(2) v(3) i(D1) i(D2)`, no errors |
| Schematic images | test.png · test2.png — both verified visually |
| README | README.md — covers simulation workflow, when to regenerate images, adding new circuits, and GnuCap vs. SPICE syntax gotchas |

To regenerate a schematic after editing a netlist:
```bash
python spice_to_schematic.py <name>.spice
```
<!-- ------ -->
---
Hardware:
  GP26 (ADC0) — photoresistor voltage divider + 100nF low-pass filter
  GP27 (ADC1) — potentiometer calibration reference
  GP15        — white LED controlled light source
  GP4/5       — I2C LCD 1602 readout

Files:
  gpio_analog_sensing.spice  — SPICE voltage divider (bright/dim/pot conditions)
  gpio_analog_sensing.gc     — GnuCap batch simulation (3 operating points)
  schematic.png              — generated schematic
  diagram.json               — Wokwi simulation layout
  breadboard.md              — step-by-step wiring for Pico at far-left
  main.py                    — MicroPython: ADC read loop, filter, lux estimate, LCD
  calibration.py             — NoiseReport, CalibrationCurve (power-law fit), drift log
  README.md                  — usage guide, success criteria, unlock path
  docs/noise_measurement.md  — noise floor characterisation guide
  docs/drift_measurement.md  — drift measurement and compensation guide
  docs/calibration_guide.md  — full calibration workflow with examples" && git push 2>&1 | tail -3

Completed: *Create gpio_analog_sensing platform* (7/7)

All 9 tasks done across 7 commits, all pushed. Here's the final repo layout:

```
pico/
├── gpio_led_single/          test.spice · test.gc · schematic.png · breadboard.md
├── gpio_led_parallel/        test2.spice · test2.gc · schematic.png · breadboard.md
├── gpio_led_basic/           + gpio_led_basic.spice · .gc · schematic.png · breadboard.md
├── gpio_button_timing/       + gpio_button_timing.spice · .gc · schematic.png · breadboard.md
├── gpio_analog_sensing/      (new) SPICE · GnuCap · MicroPython · calibration · 3 guide docs
├── micropico/                lcd1602.py · ws2812.py · main.py · inventory.md (was scratch/)
└── tools/
    └── spice_to_schematic.py
```

Key things to note for your first build session:
- **Start with noise_measurement.md** — characterise your ADC before calibrating
- The photoresistor is the recommended first sensor (thermistor noted as suspect)
- `mpremote run gpio_analog_sensing/main.py` drops straight into the live ADC readout loop
<!-- ------ -->
---