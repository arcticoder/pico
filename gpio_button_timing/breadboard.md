# Breadboard Wiring — gpio_button_timing

## Circuit overview

* **GP17** drives a red LED via a 220 Ω resistor (output)
* **GP16** reads a push button using a 10 kΩ pull-down resistor (input, active high)

When the button is pressed, GP16 reads 3.3 V (HIGH). When released, it is
pulled to GND through R_pull (LOW). `main.py` turns the LED on whenever the
button is held and logs press/release timestamps.

**Equivalent to:** `gpio_button_timing/diagram.json` (Wokwi) and
`gpio_button_timing/gpio_button_timing.spice`

---

## Pico pinout reference (Pico seated far left, rows 1–20)

| Row | Col e (left pins) | Col f (right pins) |
|-----|-------------------|--------------------|
|  3  | **GND** ←         | GND                |
|  5  | GP3               | **3V3_OUT** ←      |
| 19  | GP14              | **GP17** ← LED out |
| 20  | GP15              | **GP16** ← btn in  |

---

## Parts required

| Component           | Value  | Quantity |
|---------------------|--------|----------|
| LED (red)           | —      | 1        |
| Resistor            | 220 Ω  | 1        |
| Push button         | —      | 1        |
| Resistor (pull-down)| 10 kΩ  | 1        |
| Jumper wires        | —      | ~5       |

---

## Wiring steps

### 1. Power rails

| From                             | To                       | Wire color |
|----------------------------------|--------------------------|------------|
| Pico **3V3_OUT** (row 5, col f)  | Top red power rail (+)   | Red        |
| Pico **GND** (row 3, col e)      | Top blue power rail (−)  | Black      |

---

### 2. LED branch (GP17 output)

| Step | From                          | To                | Wire color |
|------|-------------------------------|-------------------|------------|
| a    | Pico **GP17** (row 19, col f) | Row 22, col f     | Green      |
| b    | Resistor 220 Ω leg 1          | Row 22, col f     | —          |
| c    | Resistor 220 Ω leg 2          | Row 24, col e     | —          |
| d    | **LED anode (+)**             | Row 24, col e     | —          |
| e    | **LED cathode (−)**           | Row 26, col e     | —          |
| f    | Row 26, col e                 | Blue rail (−)     | Black      |

---

### 3. Button branch (GP16 input, active-high pull-down)

The button bridges the 3.3 V rail to GP16. The 10 kΩ pull-down ensures GP16
reads 0 V when the button is open.

| Step | From                          | To                  | Wire color |
|------|-------------------------------|---------------------|------------|
| a    | Red rail (+) / 3V3            | Row 30, col f       | Red        |
| b    | Push button pin 2 (right)     | Row 30, col f       | —          |
| c    | Push button pin 1 (left)      | Row 30, col a       | —          |
| d    | Pico **GP16** (row 20, col f) | Row 30, col a       | Blue       |
| e    | R_pull 10 kΩ leg 1            | Row 30, col a       | —          |
| f    | R_pull 10 kΩ leg 2            | Row 32, col a       | —          |
| g    | Row 32, col a                 | Blue rail (−)       | Black      |

---

## Summary diagram

```
Pico GP17 (row 19, col f)
      │
   [R_limit 220Ω]   rows 22–24
      │
   LED anode        row 24
      │
   LED cathode      row 26
      │
   GND rail (−)

Pico 3V3 (row 5, col f) ────> Red rail
                                    │
                              [Button closed]
                                    │
Pico GP16 (row 20, col f) ────> Row 30, col a ─── [R_pull 10kΩ] ─── GND
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
gnucap -b gpio_button_timing/gpio_button_timing.gc
```

* `i(D_led)` at 3.3 V ≈ 5.9 mA (safe)
* `v(3)` (GP16 when button pressed) ≈ 3.3 V
