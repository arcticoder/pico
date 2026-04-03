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
Summary of what was delivered across this session:

**Renames** — `gpio_led_single/` → led_single, `gpio_led_parallel/` → led_parallel

**All 5 breadboard.md files** — USB-up orientation paragraph, `GND.1`, `3V3`, exact wire specs from inventory (colour + length per step)

**inventory.md** — wire section reformatted into proper markdown tables

**README.md** — fully rewritten:
- New title ("Single-Breadboard Project Series")
- Per-stage tables listing every file with its purpose
- New Schematics section (spice_to_schematic.py usage)
- mpremote upload section (replaces Thonny)
- GnuCap vs ngspice comparison table with per-stage simulation commands
- Repo structure tree with per-file annotations
- Planned stages 6–8 with inventory feasibility notes

**New `bom.md` files** — gpio_pwm_led, gpio_interrupt_button, gpio_i2c_lcd each with a parts table and planned file list
<!-- ------ -->
---
The working tree is clean — commit `bddc867` plus a subsequent history.md update (`6ba9135`) are all pushed. Everything on the todo list was completed in the previous response. Let me mark the list current: 

Completed: *Rewrite README.md* (4/7)

All 7 tasks are complete and pushed. The repo is clean at `6ba9135`. Nothing remains from the previous session's task list.
<!-- ------ -->
---
All 20 issues resolved, pushed as `5ba6258`. Summary of what was done:

**Issue 1** — spice_to_schematic.py now outputs `schematic.png` in the same directory as the input `.spice` file (instead of `<basename>.png`). No more duplicate PNGs.

**Issue 2** — README has a new "### Running on WSL (Windows 11)" section documenting `usbipd attach --busid <X-Y> --wsl --auto-attach` before the mpremote section.

**Issue 3** — README mpremote block split: `mpremote repl` is in its own code block with an explicit note that it's interactive and other `mpremote` commands must be run from the shell, not the REPL.

**Issue 4** — All 5 `.gc` GnuCap files removed from the repo (`git rm`). README simulation section now ngspice-only. All breadboard.md simulation commands updated to `ngspice -b`.

**Issues 5–20** — All 5 breadboard.md files fixed:
- Section headers: `cols 1–20` → `rows 1–20`
- Intro text: `row c/h` → `column h/c`, `Col 1` → `Row 1`
- Power rails: `outer edges` → `left and right edges`
- Pin tables: completely rewritten — left=column h (GP0/GP1/GND.1...), right=column c (VBUS/VSYS/GND.8/3V3...) with correct signal assignments at correct rows
- GND pin: `GND.1 (c3)` → `GND.8 (c3)` (GND.8 is the pin adjacent to VSYS on the right side)
- GP17: row 18 → row 19; GP16: row 19 → row 20; GP15: `c20` → `h20`; GP4/SDA: `h7` → `h6`; GP5/SCL: `h9` → `h7`
- Power rail references: `Top red/blue power rail` → `Right power rail (+)/(−)` throughout
- led_parallel: branch labels corrected (cols A–C are the right half, cols F–J are the left half after rotation)
<!-- ------ -->
---
All done, pushed as `bcb7c3d`. Summary:

**Task 1** — README line 40: `<netlist-basename>.png` → `schematic.png` (matches actual tool behaviour).

**Task 2** — README stages intro: removed the claim that every stage has a README.md. New text: *"Each stage has its own folder with simulation files and a breadboard wiring guide; stages 3–5 also include a README.md and MicroPython code."*

**Task 3** — All power-rail positive connections across all 5 files: `Red jump wire, 2.5 cm` → `Orange jump wire, 2.25 cm`. Parts tables updated.

**Task 4** — All power-rail negative connections across all 5 files: `Black jump wire, 1.5 cm` → `Blue jump wire, 1.25 cm`. Parts tables updated. gpio_button_timing button-branch table also had the `Wire color` column heading replaced with `Wire` and colour-only values filled in with full specs.
<!-- ------ -->
---