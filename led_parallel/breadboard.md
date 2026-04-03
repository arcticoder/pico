# Breadboard Wiring — Parallel LED Pair (test2.spice)

## Circuit overview

Two LEDs in **parallel** from the same 3.3 V supply, each with its own
470 Ω current-limiting resistor. This tests that both branches stay within
safe currents simultaneously, and that total draw from the 3.3 V rail stays
comfortable.

**Equivalent to:** `test2.spice`

---

## Pico pin reference (USB port faces up, rows 1–20)

The Pico straddles the centre channel with the **USB port at the top**.
Left-column pins land in column **h** (holes h1–h20); right-column pins in
column **c** (c1–c20). Row 1 is the USB end; row 20 is the chip end.

A breadboard's terminal strips run **horizontally**: all five holes in a
single row (e.g. row 22 holes A–E) share one node. The centre channel
breaks the connection — row 22 A–E is isolated from row 22 F–J. Power
rails on the left and right edges run **vertically** (the entire red or blue
strip is one node).

| Row | Col h (left side) | Col c (right side)        |
|-----|-------------------|---------------------------|
| 1   | GP0               | VBUS                      |
| 2   | GP1               | VSYS                      |
| 3   | GND.1             | **GND.8** ←               |
| 4   | GP2               | 3V3_EN                    |
| 5   | GP3               | **3V3** ←                 |
| …   | …                 | …                         |

---

## Parts required

| Component                    | Value | Quantity |
|------------------------------|-------|----------|
| LED (any color)              | —     | 2        |
| Resistor                     | 470 Ω | 2        |
| Jump wire — orange, 2.25 cm  | —     | 3        |
| Jump wire — blue, 1.25 cm    | —     | 3        |

---

## Wiring steps

### 1. Power the breadboard rails (same as single-LED)

| From                   | To                       | Wire                        |
|------------------------|--------------------------|-----------------------------|
| Pico **3V3** (c5)      | Right power rail (+)    | Orange jump wire, 2.25 cm  |
| Pico **GND.8** (c3)    | Right power rail (−)    | Blue jump wire, 1.25 cm    |

### 2. LED branch 1 (right branch)

Place **R1 (470 Ω)**:
- One leg at row 22, col A  
- Other leg at row 22, col C

Because the terminal strip connects all holes in the same row horizontally,
cols A–C are on the same node (right half, cols A–E). The resistor body bridges them.

| From             | To             | Wire                    |
|------------------|----------------|-------------------------|
| Right power rail (+) | Row 22, col A  | Orange jump wire, 2.25 cm  |

Place **LED1** (the centre channel separates the two halves):

| LED terminal  | Position      |
|---------------|---------------|
| Anode (+)     | Row 22, col C |
| Cathode (−)   | Row 24, col C |

| From          | To                      | Wire                     |
|---------------|-------------------------|---------------------------|
| Row 24, col C | Right power rail (−)    | Blue jump wire, 1.25 cm  |

### 3. LED branch 2 (left branch)

Place **R2 (470 Ω)** on the **left half** of the breadboard (cols F–J).
The centre channel ensures this branch is electrically independent of branch 1.

- One leg at row 22, col F  
- Other leg at row 22, col H

| From             | To             | Wire                    |
|------------------|----------------|-------------------------|
| Right power rail (+) | Row 22, col F  | Orange jump wire, 2.25 cm  |

Place **LED2**:

| LED terminal  | Position      |
|---------------|---------------|
| Anode (+)     | Row 22, col H |
| Cathode (−)   | Row 24, col H |

| From          | To                      | Wire                     |
|---------------|-------------------------|---------------------------|
| Row 24, col H | Right power rail (−)    | Blue jump wire, 1.25 cm  |

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
ngspice -b led_parallel/test2.spice
```

The `i(D1)` and `i(D2)` columns should be equal (symmetric branches) and
stay below 20 mA at all sweep points.
