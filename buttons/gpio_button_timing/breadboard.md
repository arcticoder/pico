# Breadboard Wiring — gpio_button_timing

## Circuit overview

* **GP17** drives a red LED via a 220 Ω resistor (output)
* **GP16** reads a push button using a 10 kΩ pull-down resistor (input, active high)

When the button is pressed, GP16 reads 3.3 V (HIGH). When released, it is
pulled to GND through R_pull (LOW). `main.py` turns the LED on whenever the
button is held and logs press/release timestamps.

**Equivalent to:** `buttons/gpio_button_timing/gpio_button_timing.spice`

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

| Row | Col h (left side)       | Col c (right side)      |
|-----|-------------------------|-------------------------|
| 1   | GP0                     | VBUS                    |
| 2   | GP1                     | VSYS                    |
| 3   | GND.1                   | **GND.8** ←             |
| 4   | GP2                     | 3V3_EN                  |
| 5   | GP3                     | **3V3** ←               |
| …   | …                       | …                       |
| 18  | GND.4                   | GND.6                   |
| 19  | GP14                    | **GP17** ← LED out      |
| 20  | GP15                    | **GP16** ← btn in       |

---

## Parts required

| Component                  | Value  | Quantity |
|----------------------------|--------|----------|
| LED (red)                  | —      | 1        |
| Resistor                   | 220 Ω  | 1        |
| Push button                | —      | 1        |
| Resistor (pull-down)       | 10 kΩ  | 1        |
| Jump wire — green, 1.0 cm  | —      | 1        |
| Jump wire — orange, 2.25 cm | —      | 2        |
| Jump wire — blue, 1.25 cm   | —      | 4        |

---

## Wiring steps

### 1. Power rails

| From                      | To                       | Wire                        |
|---------------------------|--------------------------|-----------------------------|
| Pico **3V3** (c5)         | Right power rail (+)    | Orange jump wire, 2.25 cm  |
| Pico **GND.8** (c3)       | Right power rail (−)    | Blue jump wire, 1.25 cm    |

---

### 2. LED branch (GP17 output)

All holes in the same row half share one node. Place the 220 Ω resistor across
rows 22–24 in col F (right half); the LED follows below it.

| Step | From                     | To                | Wire                       |
|------|--------------------------|-------------------|---------|
| a    | Pico **GP17** (c19)      | Row 22, col F     | Green jump wire, 1.0 cm   |
| b    | Resistor 220 Ω leg 1    | Row 22, col F     | —                          |
| c    | Resistor 220 Ω leg 2    | Row 24, col E     | —                          |
| d    | **LED anode (+)**        | Row 24, col E     | —                          |
| e    | **LED cathode (−)**      | Row 26, col E     | —                          |
| f    | Row 26, col E            | Right power rail (−)   | Blue jump wire, 1.25 cm    |

---

### 3. Button branch (GP16 input, active-high pull-down)

The button bridges the 3.3 V rail to GP16.  A 10 kΩ pull-down resistor
ensures GP16 reads 0 V when the button is open.

| Step | From                     | To                  | Wire                        |
|------|--------------------------|---------------------|-----------------------------||
| a    | Right power rail (+)     | Row 30, col f       | Orange jump wire, 2.25 cm   |
| b    | Push button pin 2 (right)| Row 30, col f       | —                           |
| c    | Push button pin 1 (left) | Row 30, col a       | —                           |
| d    | Pico **GP16** (c20)      | Row 30, col a       | Blue jump wire, 1.25 cm     |
| e    | Pull-down resistor (10 kΩ) leg 1 | Row 30, col a | —                     |
| f    | Pull-down resistor leg 2 | Row 32, col a       | —                           |
| g    | Row 32, col a            | Right power rail (−)  | Blue jump wire, 1.25 cm   |

---

## Summary diagram

```
Pico GP17 (c19)
      │
   [R_limit 220Ω]   rows 22–24, col F (left half)
      │
   LED anode        row 24, col E (right half)
      │
   LED cathode      row 26, col E
      │
   GND rail (−)

Pico 3V3 (c5) ────> Right power rail
                         │
                   [Button closed]
                         │
Pico GP16 (c20) ──> Row 30, col A ── [R_pull 10kΩ] ── GND
```

---

## Expected behavior

| Button state | GP16 reads | LED state        |
|--------------|------------|------------------|
| Released     | 0 V (LOW)  | Off              |
| Pressed      | 3.3 V (HIGH) | On (via firmware) |

---

## Simulation

```bash
ngspice -b buttons/gpio_button_timing/gpio_button_timing.spice
```

* `i(D_led)` at 3.3 V ≈ 5.9 mA (safe)
* `v(3)` (GP16 when button pressed) ≈ 3.3 V
