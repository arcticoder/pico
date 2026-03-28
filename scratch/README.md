# pico/scratch — LED Circuit Simulation Workspace

This directory contains SPICE netlists, GnuCap batch scripts, and tooling for
simulating LED driver circuits and generating schematic diagrams from those
netlists.

---

## Directory layout

| File | Purpose |
|------|---------|
| `test.spice` | Single LED + 470 Ω resistor, 3.3 V supply |
| `test2.spice` | Two LEDs in parallel, each with 470 Ω resistor, 3.3 V supply |
| `led_test.gc` | GnuCap batch simulation for `test.spice` |
| `led_test2.gc` | GnuCap batch simulation for `test2.spice` |
| `spice_to_schematic.py` | Parses a SPICE netlist and renders a schematic PNG via schemdraw |
| `test.png` | Schematic image generated from `test.spice` |
| `test2.png` | Schematic image generated from `test2.spice` |

---

## Dependencies

| Tool | Install |
|------|---------|
| [GnuCap](http://www.gnucap.org/) | `sudo apt install gnucap` |
| Python 3.8+ | `conda` / `apt` |
| schemdraw | `pip install schemdraw matplotlib` |

---

## Running simulations

### Single-LED circuit (`test.spice`)

```bash
gnucap -b led_test.gc
```

### Two-LED parallel circuit (`test2.spice`)

```bash
gnucap -b led_test2.gc
```

Both scripts sweep the supply voltage from 0 V up to the rated supply and
print node voltages and per-LED currents at each step.  A clean run produces
**no error lines** — only the header row (`#`) followed by numeric voltage
steps.

---

## Generating / updating schematic images

Use `spice_to_schematic.py` to regenerate PNGs any time a netlist changes:

```bash
# Regenerate schematic for test.spice → test.png
python spice_to_schematic.py test.spice

# Regenerate schematic for test2.spice → test2.png
python spice_to_schematic.py test2.spice

# Custom output path
python spice_to_schematic.py test2.spice schematics/test2_v2.png
```

> **When to re-run:** After any change to a `.spice` file — new components,
> different voltage, adjusted resistor values — re-run the matching
> `spice_to_schematic.py` command above to keep the PNG in sync with the
> simulation.

### Supported SPICE elements

The parser understands:

| Prefix | Description | Rendered as |
|--------|-------------|-------------|
| `V` | DC voltage source | Voltage source circle |
| `R` | Resistor | Zigzag resistor symbol |
| `D` | Diode; LED if model name contains "LED" | Diode triangle / LED with arrows |

Unsupported elements (capacitors, transistors, etc.) are silently ignored in
the schematic but do not affect GnuCap simulation.

---

## Adding a new circuit

1. Create `<name>.spice` following the existing patterns.
2. Create `<name>.gc` mirroring the structure of `led_test.gc`:
   ```spice
   * Circuit title
   <elements>
   .model <ModelName> D is=<Isat>
   .dc V1 0 <Vmax> <step>
   .print dc <signals>
   .end
   ```
3. Run the simulation:
   ```bash
   gnucap -b <name>.gc
   ```
4. Generate the schematic:
   ```bash
   python spice_to_schematic.py <name>.spice
   ```

---

## Notes on GnuCap vs. SPICE syntax

GnuCap's batch (`.gc`) format diverges from standard SPICE in a few ways:

- `.model` parameters are **not** wrapped in parentheses:
  - ✅ `.model MyLED D is=1e-14`
  - ❌ `.model MyLED D(is=1e-14)`
- The `.dc` sweep **requires** the source name: `.dc V1 0 3.3 0.1`
- `eval` / `let` expressions are not supported in this GnuCap version; keep
  analysis in post-processing scripts instead.
- Inline comments use `;` in SPICE files and `*` at the start of a line in
  GnuCap batch files.
