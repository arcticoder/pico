# Breadboard Wiring — gpio_led_basic

## Circuit overview

Pico **GP17** blinks a red LED via a **220 Ω** current-limiting resistor.
GP17 drives 3.3 V when HIGH; the resistor limits forward current to a safe
~5 mA.

**Equivalent to:** `gpio_led_basic/diagram.json` (Wokwi) and
`gpio_led_basic/gpio_led_basic.spice`

---

## Pico pinout reference (USB port faces up, rows 1–20)

The Pico straddles the centre channel with the **USB port at the top**.
Left-column pins land in column **h** (holes h1–h20); right-column pins in
column **c** (c1–c20). Row 1 is the USB end; row 20 is the chip end.

A breadboard's terminal strips run **horizontally**: all five holes in a
single row (e.g. row 22 holes A–E) share one node. The centre channel
breaks the connection — row 22 A–E is isolated from row 22 F–J. Power
rails on the left and right edges run **vertically** (the entire red or blue
strip is one node).

| Row | Col h (left side)  | Col c (right side)  |
|-----|--------------------|---------------------|
| 1   | GP0                | VBUS                |
| 2   | GP1                | VSYS                |
| 3   | GND.1              | **GND.8** ←         |
| 4   | GP2                | 3V3_EN              |
| 5   | GP3                | 3V3                 |
| …   | …                  | …                   |
| 18  | GND.4              | GND.6               |
| 19  | GP14               | **GP17** ← output   |
| 20  | GP15               | GP16                |

> GP17 is on the **right side**, row 19, column **c** → breadboard hole **c19**.

---

## Parts required

| Component                  | Value | Quantity |
|----------------------------|-------|----------|
| LED (red)                  | —     | 1        |
| Resistor                   | 220 Ω | 1        |
| Jump wire — green, 1.0 cm  | —     | 1        |
| Jump wire — blue, 1.25 cm  | —     | 2        |

---

## Wiring steps

### 1. Connect GND to power rail

| From                  | To                       | Wire                     |
|-----------------------|--------------------------|---------------------------|
| Pico **GND.8** (c3)   | Right power rail (−)    | Blue jump wire, 1.25 cm  |

### 2. Place the resistor (220 Ω)

- Insert one leg into **row 22, col a**
- Insert other leg into **row 24, col a**

Add signal wire from GP17 to resistor input:

| From                     | To             | Wire                   |
|--------------------------|----------------|------------------------|
| Pico **GP17** (c19)      | Row 22, col A  | Green jump wire, 1.0 cm|

### 3. Place the LED

| LED terminal   | Breadboard position | Notes                        |
|----------------|---------------------|------------------------------|
| **Anode (+)**  | Row 24, col a       | Longer leg; connects to R1 output |
| **Cathode (−)**| Row 26, col a       | Shorter leg; to GND          |

### 4. Connect LED cathode to ground

| From           | To                       | Wire                     |
|----------------|--------------------------|---------------------------|
| Row 26, col A  | Right power rail (−)    | Blue jump wire, 1.25 cm  |

---

## Summary diagram

```
Pico GP17 (c19) ──── [R1 220Ω]  rows 22–24, col A
                                  │
                               LED anode   row 24, col A
                                  │
                               LED cathode  row 26, col A
                                  │
                              GND rail (−)
```

> Terminal strips connect horizontally (A–E share one node per row).
> The resistor and LED share col A because they are in the same row half.

---

## Expected behavior

When `main.py` drives GP17 HIGH, the LED lights. Expected current:

```
I = (3.3 V − 2.0 V) / 220 Ω ≈ 5.9 mA
```

Well within the 20 mA LED limit and the Pico's 12 mA per-pin drive current.

See [README.md](README.md) for simulation run instructions.
