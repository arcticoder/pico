# Breadboard Wiring — gpio_led_basic

## Circuit overview

Pico **GP17** blinks a red LED via a **220 Ω** current-limiting resistor.
GP17 drives 3.3 V when HIGH; the resistor limits forward current to a safe
~5 mA.

**Equivalent to:** `gpio_led_basic/diagram.json` (Wokwi) and
`gpio_led_basic/gpio_led_basic.spice`

---

## Pico pinout reference (USB port faces up, cols 1–20)

Pico straddles the centre channel.  Left-column pins → row **c**
(cols 1–20).  Right-column pins → row **h** (cols 1–20).  Col 1 is the
USB end; col 20 is the opposite (chip) end.

| Col | Row c (left side)  | Row h (right side) |
|-----|--------------------|--------------------|
| 1   | VBUS               | (RUN / debug)      |
| 2   | VSYS               | GND                |
| 3   | **GND** ←          | GP0                |
| 4   | 3V3_EN             | GP1                |
| 5   | 3V3_OUT            | GP2                |
| … | …                  | …                  |
| 18  | **GP17** ← output  | GND                |
| 19  | GP16               | GP13               |
| 20  | GP15               | GP14               |

> GP17 is on the **left side**, col 18, row **c** → breadboard hole **c18**.

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
| Pico **GND** (c3)           | Top blue power rail (−)  | Black      |

### 2. Place the resistor (220 Ω)

- Insert one leg into **row 22, col a**
- Insert other leg into **row 24, col a**

Add signal wire from GP17 to resistor input:

| From                     | To             | Wire color |
|--------------------------|----------------|------------|
| Pico **GP17** (c18)      | Row 22, col a  | Green      |

### 3. Place the LED

| LED terminal   | Breadboard position | Notes                        |
|----------------|---------------------|------------------------------|
| **Anode (+)**  | Row 24, col a       | Longer leg; connects to R1 output |
| **Cathode (−)**| Row 26, col a       | Shorter leg; to GND          |

### 4. Connect LED cathode to ground

| From           | To                      | Wire color |
|----------------|-------------------------|------------|
| Row 26, col a  | Top blue power rail (−) | Black      |

---

## Summary diagram

```
Pico GP17 (c18) ──── [R1 220Ω]  rows 22–24, col a
                                  │
                               LED anode   row 24, col a
                                  │
                               LED cathode row 26, col a
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

See [README.md](README.md) for simulation run instructions.
