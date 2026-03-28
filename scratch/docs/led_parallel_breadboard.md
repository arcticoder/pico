# Breadboard Wiring — Parallel LED Pair (test2.spice / test2.gc)

## Circuit overview

Two LEDs in **parallel** from the same 3.3 V supply, each with its own
470 Ω current-limiting resistor. This tests that both branches stay within
safe currents simultaneously, and that total draw from the 3.3 V rail stays
comfortable.

**Equivalent to:** `test2.spice` / `test2.gc`

---

## Pico pin reference (seated far left, rows 1–20)

Same Pico placement as the single-LED circuit (see `led_single_breadboard.md`).

| Row | Col e (left pins) | Col f (right pins) |
|-----|-------------------|--------------------|
|  3  | **GND** ←         | GND                |
|  5  | GP3               | **3V3_OUT** ←      |

---

## Parts required

| Component           | Value | Quantity |
|---------------------|-------|----------|
| LED (any color)     | —     | 2        |
| Resistor            | 470 Ω | 2        |
| Jumper wire (red)   | —     | 2        |
| Jumper wire (black) | —     | 2        |

---

## Wiring steps

### 1. Power the breadboard rails (same as single-LED)

| From                            | To                       | Wire color |
|---------------------------------|--------------------------|------------|
| Pico **3V3_OUT** (row 5, col f) | Top red power rail (+)   | Red        |
| Pico **GND** (row 3, col e)     | Top blue power rail (−)  | Black      |

### 2. LED branch 1 (left branch)

Place **R1 (470 Ω)**:
- One leg at Row 22, col a  
- Other leg at Row 22, col c

| From             | To              | Wire color |
|------------------|-----------------|------------|
| Top red rail (+) | Row 22, col a   | Red        |

Place **LED1**:
| LED terminal  | Position       |
|---------------|----------------|
| Anode (+)     | Row 22, col c  |
| Cathode (−)   | Row 24, col c  |

| From          | To                   | Wire color |
|---------------|----------------------|------------|
| Row 24, col c | Top blue rail (−)    | Black      |

### 3. LED branch 2 (right branch)

Place **R2 (470 Ω)**:
- One leg at Row 22, col f  
- Other leg at Row 22, col h

| From             | To              | Wire color |
|------------------|-----------------|------------|
| Top red rail (+) | Row 22, col f   | Red        |

Place **LED2**:
| LED terminal  | Position       |
|---------------|----------------|
| Anode (+)     | Row 22, col h  |
| Cathode (−)   | Row 24, col h  |

| From          | To                   | Wire color |
|---------------|----------------------|------------|
| Row 24, col h | Top blue rail (−)    | Black      |

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
gnucap -b test2.gc
```

The `i(D1)` and `i(D2)` columns should be equal (symmetric branches) and
stay below 20 mA at all sweep points.
