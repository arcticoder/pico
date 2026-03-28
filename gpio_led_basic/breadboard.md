# Breadboard Wiring — gpio_led_basic

## Circuit overview

Pico **GP17** blinks a red LED via a **220 Ω** current-limiting resistor.
GP17 drives 3.3 V when HIGH; the resistor limits forward current to a safe
~5 mA.

**Equivalent to:** `gpio_led_basic/diagram.json` (Wokwi) and
`gpio_led_basic/gpio_led_basic.spice`

---

## Pico pinout reference (seated far left, rows 1–20)

Pico USB port faces **left**. Left-side pins are in col **e**; right-side
in col **f**.

| Row | Col e (left pins) | Col f (right pins) |
|-----|-------------------|--------------------|
|  3  | **GND** ←         | GND                |
|  5  | GP3               | 3V3_OUT            |
| ... | ...               | ...                |
| 19  | GP14              | **GP17** ←         |
| 20  | GP15              | GP16               |

> GP17 is on the **right side**, row 19, col f.

---

## Parts required

| Component          | Value | Quantity |
|--------------------|-------|----------|
| LED (red)          | —     | 1        |
| Resistor           | 220 Ω | 1        |
| Jumper wire (green)| —     | 1        |
| Jumper wire (black)| —     | 1        |

---

## Wiring steps

### 1. Connect GND to power rail

| From                        | To                       | Wire color |
|-----------------------------|--------------------------|------------|
| Pico **GND** (row 3, col e) | Top blue power rail (−)  | Black      |

### 2. Place the resistor (220 Ω)

- Insert one leg into **row 22, col e** (same breadboard half as GP17 side)
- Insert other leg into **row 24, col e**

Add signal wire from GP17 to resistor input:

| From                           | To             | Wire color |
|--------------------------------|----------------|------------|
| Pico **GP17** (row 19, col f)  | Row 22, col f  | Green      |
| Row 22, col f                  | Row 22, col e  | short wire |

> Or simply insert R1 directly straddling the gap (col e to col f) at row 22.

### 3. Place the LED

| LED terminal   | Breadboard position | Notes                        |
|----------------|---------------------|------------------------------|
| **Anode (+)**  | Row 24, col e       | Longer leg; connects to R1 output |
| **Cathode (−)**| Row 26, col e       | Shorter leg; to GND          |

### 4. Connect LED cathode to ground

| From           | To                      | Wire color |
|----------------|-------------------------|------------|
| Row 26, col e  | Top blue power rail (−) | Black      |

---

## Summary diagram

```
Pico GP17 (row 19, col f)
        │
       [R1 220Ω]  rows 22-24
        │
       LED anode  row 24
        │
       LED cathode  row 26
        │
     GND rail (−)
```

---

## Expected behavior

When `main.py` drives GP17 HIGH, the LED lights. Expected current:

```
I = (3.3 V − 2.0 V) / 220 Ω ≈ 5.9 mA
```

Well within the 20 mA LED limit and the Pico's 12 mA per-pin drive current.

---

## Simulation

```bash
gnucap -b gpio_led_basic/gpio_led_basic.gc
```

`i(D1)` at 3.3 V should print approximately `5.9e-03`.
