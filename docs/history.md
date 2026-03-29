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
Completed: *Commit and push all changes* (9/9)

All 15 tasks done in commit `2f41606`, pushed to `origin/main`. Summary of what changed:

**README.md (tasks 1–5)** — now lists all 5 project directories with cross-refs to sub-READMEs, a `gnucap -b`/`ngspice -b` simulation section, and a progression table in "Next steps" with file links.

**README.md (task 4)** — new file covering build steps, MicroPython upload, and simulation run instructions.

**Breadboard reorientation (tasks 6–8, 13)** — all four breadboard.md files updated from "USB faces left / col e / col f" to:
- "USB port faces UP" convention
- Wokwi row **c** (left rail, cols 1–20) and row **h** (right rail, cols 1–20)
- Correct pin positions: GP17 → c18, GP16 → c19, GP15 → c20, GP26 → c10, GP27 → c9, GP4 → h7, GP5 → h9

**breadboard.md (task 9)** — `R_pull` renamed to "pull-down resistor (10 kΩ)" matching the inventory.

**breadboard.md (task 14)** — BOM table gains an `Abbrev.` column (LDR, R_fixed, C_filter, Pot, LED_src, R_led, LCD).

**GnuCap output labels (task 15)** — breadboard.md Simulation section now has an explicit column-order table; gpio_analog_sensing.gc has a matching comment: `V_3v3_A | v(2) bright | v(3) dim | v(5) pot-mid`.

**File relocations (tasks 10–11)** — `micropico/inventory.md` → inventory.md; `micropico/lcd1602.py` and `ws2812.py` → lib.

**scratch/led_test.gc (task 12)** — deleted (was untracked; scratch is gitignored).
<!-- ------ -->
---