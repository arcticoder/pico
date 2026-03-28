# Breadboard Wiring — Single LED (test.spice / test.gc)

## Circuit overview

This is a **static 3.3 V LED test** — no GPIO control. It validates that a
470 Ω current-limiting resistor gives safe operating current for a standard
LED from the Pico's 3.3 V output rail.

**Equivalent to:** `test.spice` / `test.gc`

---

## Pico pin reference (seated far left, rows 1–20)

Pico USB port faces **left**. Left-side pins occupy column **e**; right-side
pins occupy column **f**.

| Row | Col e (left pins) | Col f (right pins)  |
|-----|-------------------|---------------------|
|  1  | GP0               | VBUS (5 V)          |
|  2  | GP1               | VSYS                |
|  3  | **GND** ←         | GND                 |
|  4  | GP2               | 3V3_EN              |
|  5  | GP3               | **3V3_OUT** ←       |
|  6  | GP4 (SDA)         | ADC_VREF            |
| ... | ...               | ...                 |

> Rows 21+ are free for components.

---

## Parts required

| Component          | Value | Quantity |
|--------------------|-------|----------|
| LED (any color)    | —     | 1        |
| Resistor           | 470 Ω | 1        |
| Jumper wire (red)  | —     | 1        |
| Jumper wire (black)| —     | 1        |

---

## Wiring steps

### 1. Power the breadboard rails

| From                         | To                      | Wire color |
|------------------------------|-------------------------|------------|
| Pico **3V3_OUT** (row 5, col f) | Top red power rail (+)  | Red        |
| Pico **GND** (row 3, col e)     | Top blue power rail (−) | Black      |

### 2. Place the resistor (470 Ω)

- Insert one leg into **row 22, col a** (connects to + rail via short wire, below)
- Insert other leg into **row 22, col c** (signal node, connects to LED anode)

Add a short jumper:

| From             | To                  | Wire color |
|------------------|---------------------|------------|
| Top red rail (+) | Row 22, col a       | Red        |

### 3. Place the LED

| LED terminal | Breadboard position | Notes                            |
|--------------|---------------------|----------------------------------|
| **Anode (+)**    | Row 22, col c       | Same column as resistor output   |
| **Cathode (−)**  | Row 24, col c       | Long leg = anode; short leg = cathode |

### 4. Connect LED cathode to ground

| From             | To                     | Wire color |
|------------------|------------------------|------------|
| Row 24, col c    | Top blue rail (−) or Pico GND | Black |

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
