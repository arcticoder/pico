# Breadboard Wiring — Parallel LED Pair (test2.spice / test2.gc)

## Circuit overview

Two LEDs in **parallel** from the same 3.3 V supply, each with its own
470 Ω current-limiting resistor. This tests that both branches stay within
safe currents simultaneously, and that total draw from the 3.3 V rail stays
comfortable.

**Equivalent to:** `test2.spice` / `test2.gc`

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

---

## Parts required

| Component                    | Value | Quantity |
|------------------------------|-------|----------|
| LED (any color)              | —     | 2        |
| Resistor                     | 470 Ω | 2        |
| Jump wire — red, 2.5 cm      | —     | 2        |
| Jump wire — black, 1.5 cm    | —     | 2        |

---

## Wiring steps

### 1. Power the breadboard rails (same as single-LED)

| From                   | To                       | Wire                        |
|------------------------|--------------------------|-----------------------------|
| Pico **3V3** (c5)      | Top red power rail (+)   | Red jump wire, 2.5 cm      |
| Pico **GND.1** (c3)    | Top blue power rail (−)  | Black jump wire, 1.5 cm    |

### 2. LED branch 1 (left branch)

Place **R1 (470 Ω)**:
- One leg at row 22, col A  
- Other leg at row 22, col C

Because the terminal strip connects all holes in the same row horizontally,
cols A–C are on the same node (left half). The resistor body bridges them.

| From             | To             | Wire                    |
|------------------|----------------|-------------------------|
| Top red rail (+) | Row 22, col A  | Red jump wire, 2.5 cm  |

Place **LED1** (the centre channel separates the two halves):

| LED terminal  | Position      |
|---------------|---------------|
| Anode (+)     | Row 22, col C |
| Cathode (−)   | Row 24, col C |

| From          | To                  | Wire                     |
|---------------|---------------------|---------------------------|
| Row 24, col C | Top blue rail (−)   | Black jump wire, 1.5 cm  |

### 3. LED branch 2 (right branch)

Place **R2 (470 Ω)** on the **right half** of the breadboard (cols F–J).
The centre channel ensures this branch is electrically independent of branch 1.

- One leg at row 22, col F  
- Other leg at row 22, col H

| From             | To             | Wire                    |
|------------------|----------------|-------------------------|
| Top red rail (+) | Row 22, col F  | Red jump wire, 2.5 cm  |

Place **LED2**:

| LED terminal  | Position      |
|---------------|---------------|
| Anode (+)     | Row 22, col H |
| Cathode (−)   | Row 24, col H |

| From          | To                  | Wire                     |
|---------------|---------------------|---------------------------|
| Row 24, col H | Top blue rail (−)   | Black jump wire, 1.5 cm  |

---

## Expected behavior

Both LEDs illuminate simultaneously. Total current draw:

```
Each branch: I = (3.3 V − 2.0 V) / 470 Ω ≈ 2.8 mA
Total:        ≈ 5.6 mA  (well within Pico 3V3_OUT limit of ~300 mA)
```

If one LED is significantly brighter, check that both resistors are the same
value and both LEDs are the same type/color.

---

## Simulation vs. breadboard

```bash
gnucap -b led_parallel/test2.gc
```

The `i(D1)` and `i(D2)` columns should be equal (symmetric branches) and
stay below 20 mA at all sweep points.
