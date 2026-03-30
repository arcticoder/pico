# Breadboard Wiring — Single LED (test.spice / test.gc)

## Circuit overview

This is a **static 3.3 V LED test** — no GPIO control. It validates that a
470 Ω current-limiting resistor gives safe operating current for a standard
LED from the Pico's 3.3 V output rail.

**Equivalent to:** `test.spice` / `test.gc`

---

## Pico pin reference (USB port faces up, cols 1–20)

The Pico straddles the centre channel with the **USB port at the top**.
Left-column pins land in row **c** (holes c1–c20); right-column pins in row
**h** (h1–h20). Col 1 is the USB end; col 20 is the chip end.

A breadboard's terminal strips run **horizontally**: all five holes in a
single row (e.g. row 22 holes A–E) share one node. The centre channel
breaks the connection — row 22 A–E is isolated from row 22 F–J. Power
rails on the outer edges run **vertically** (the entire red column is one node).

| Col | Row c (left side) | Row h (right side) |
|-----|-------------------|--------------------------|
| 1   | VBUS              | RUN                      |
| 2   | VSYS              | GND                      |
| 3   | **GND.1** ←       | GP0                      |
| 4   | 3V3_EN            | GP1                      |
| 5   | **3V3** ←         | GP2                      |
| … | …                 | …                        |

> Rows 21+ (below the Pico) are free for components.

---

## Parts required

| Component                | Value | Quantity |
|--------------------------|-------|----------|
| LED (any color)          | —     | 1        |
| Resistor                 | 470 Ω | 1        |
| Jump wire — red, 2.5 cm  | —     | 1        |
| Jump wire — black, 1.5 cm| —     | 1        |

---

## Wiring steps

### 1. Power the breadboard rails

| From                  | To                      | Wire                        |
|-----------------------|-------------------------|--------------|
| Pico **3V3** (c5)     | Top red power rail (+)  | Red jump wire, 2.5 cm      |
| Pico **GND.1** (c3)   | Top blue power rail (−) | Black jump wire, 1.5 cm    |

### 2. Place the resistor (470 Ω)

- Insert one leg into **row 22, col a** (connects to + rail via short wire, below)
- Insert other leg into **row 22, col c** (signal node, connects to LED anode)

Add a short jumper:

| From             | To             | Wire                    |
|------------------|----------------|-------------------------|
| Top red rail (+) | Row 22, col a  | Red jump wire, 2.5 cm  |

### 3. Place the LED

| LED terminal | Breadboard position | Notes                            |
|--------------|---------------------|----------------------------------|
| **Anode (+)**    | Row 22, col c       | Same column as resistor output   |
| **Cathode (−)**  | Row 24, col c       | Long leg = anode; short leg = cathode |

### 4. Connect LED cathode to ground

| From          | To                 | Wire                     |
|---------------|--------------------|---------------------------|
| Row 24, col c | Top blue rail (−)  | Black jump wire, 1.5 cm  |

---

## Expected behavior

When power is applied (Pico connected via USB), the LED should illuminate
steadily. At 3.3 V with 470 Ω and a typical LED forward voltage of ~2.0 V:

```
I = (3.3 V − 2.0 V) / 470 Ω ≈ 2.8 mA
```

This is well within the 20 mA absolute maximum. If the LED is dim, try a
lower-value resistor (330 Ω). If it doesn't light at all, check polarity.

---

## Simulation vs. breadboard

Run the GnuCap simulation to verify expected current before building:

```bash
gnucap -b test.gc
```

The printed `i(D1)` column shows simulated diode current at each supply
voltage step. At 3.3 V the value should be a few milliamps.
