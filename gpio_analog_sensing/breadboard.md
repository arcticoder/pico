# Breadboard Wiring — gpio_analog_sensing

## Circuit overview

A **voltage-divider sensing platform** using the Pico's ADC inputs:

| Channel | Pin  | Signal |
|---------|------|--------|
| ADC0    | GP26 | Photoresistor divider midpoint (`V_mid`) |
| ADC1    | GP27 | Potentiometer wiper (calibration reference) |
| GPIO    | GP15 | Controlled white LED (light source for LDR) |
| I2C SDA | GP4  | LCD 1602 data |
| I2C SCL | GP5  | LCD 1602 clock |

**Topology:**
```
3V3 ─── R_fixed(10kΩ) ─── V_mid(GP26) ─── LDR(photoresistor) ─── GND
                                │
                          C_filter (100nF)
                                │
                               GND
```

The capacitor creates a low-pass RC filter (τ = 10 kΩ × 100 nF = 1 ms),
reducing high-frequency ADC noise.

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
| 6   | **GP4/SDA** ←           | ADC_VREF                |
| 7   | **GP5/SCL** ←           | GP28/ADC2               |
| 8   | GND.2                   | AGND                    |
| 9   | GP6                     | **GP27/ADC1** ←         |
| 10  | GP7                     | **GP26/ADC0** ←         |
| …   | …                       | …                       |
| 20  | **GP15** ←              | GP16                    |

---

## Parts required

| Component                    | Abbrev.  | Value  | Qty |
|------------------------------|----------|--------|-----|
| Photoresistor (LDR)          | LDR      | —      | 1   |
| Resistor (fixed, top)        | R_fixed  | 10 kΩ  | 1   |
| Capacitor (filter)           | C_filter | 100 nF | 1   |
| Potentiometer                | Pot      | 10 kΩ  | 1   |
| LED (white)                  | LED_src  | —      | 1   |
| Resistor (LED limit)         | R_led    | 220 Ω  | 1   |
| I2C LCD 1602                 | LCD      | —      | 1   |
| Jump wire — orange, 2.25 cm  | —        | —      | 4   |
| Jump wire — blue, 1.25 cm    | —        | —      | 4   |
| Jump wire — green, 1.0 cm    | —        | —      | 1   |
| Dupont wire — cyan, 22 cm    | —        | —      | 1   |
| Dupont wire — purple, 22 cm  | —        | —      | 1   |
| Dupont wire — blue, 22 cm    | —        | —      | 2   |
| Dupont wire — yellow, 22 cm  | —        | —      | 2   |

---

## Wiring steps

### 1. Power rails

| From                  | To                       | Wire                        |
|-----------------------|--------------------------|-----------------------------|
| Pico **3V3** (c5)     | Right power rail (+)     | Orange jump wire, 2.25 cm  |
| Pico **GND.8** (c3)   | Right power rail (−)     | Blue jump wire, 1.25 cm    |

---

### 2. Voltage divider (LDR sensing — rows 22–28)

The 10 kΩ fixed resistor sits **above** the midpoint; the LDR sits **below**.

| Step | Component             | From          | To            | Wire                    |
|------|-----------------------|---------------|---------------|-------------------------|
| a    | Wire                  | Right power rail (+)  | Row 22, col A | Orange jump wire, 2.25 cm  |
| b    | R_fixed (10 kΩ) leg 1 | Row 22, col A | Row 24, col A | —                       |
| c    | R_fixed leg 2         | Row 24, col A | = V_mid node  | —                       |
| d    | LDR leg 1             | Row 24, col B | = V_mid node  | —                       |
| e    | LDR leg 2             | Row 26, col B | Right power rail (−) | Blue jump wire, 1.25 cm|

**V_mid signal wire (to ADC0):**

| From          | To                  | Wire                      |
|---------------|---------------------|---------------------------|
| Row 24, col C | Pico **GP26** (c10) | Cyan dupont wire, 22 cm  |

---

### 3. Filter capacitor (100 nF — rows 24–26)

Connects V_mid to GND; bridging the gap is fine.

| Capacitor leg | Position            |
|---------------|---------------------|
| + (or any)    | Row 24, col D       |
| −             | Row 26, col D → Right power rail (−) |

---

### 4. Potentiometer (rows 32–36, calibration reference)

| Pot terminal | Connection             | Wire                       |
|--------------|------------------------|----------------------------|
| VCC          | Right power rail (+)   | Orange jump wire, 2.25 cm |
| GND          | Right power rail (−)   | Blue jump wire, 1.25 cm   |
| Wiper (SIG)  | Pico **GP27** (c9)     | Purple dupont wire, 22 cm |

---

### 5. White LED (controlled light source — rows 40–44)

Aim the LED toward the photoresistor for repeatable controlled illumination.

| Step | From                       | To             | Wire                      |
|------|----------------------------|----------------|---------------------------|
| a    | Pico **GP15** (h20)        | Row 40, col E  | Green jump wire, 1.0 cm  |
| b    | R_led (220 Ω) leg 1        | Row 40, col E  | —                         |
| c    | R_led leg 2                | Row 42, col E  | —                         |
| d    | LED anode (+)              | Row 42, col E  | —                         |
| e    | LED cathode (−)            | Row 44, col E  | —                         |
| f    | Row 44, col E              | Right power rail (−)  | Blue jump wire, 1.25 cm  |

---

### 6. I2C LCD 1602 (far right side of breadboard)

Use the **4-pin I2C backpack version**:

| LCD pin | Connection             | Wire                        |
|---------|------------------------|--------------|
| GND     | Right power rail (−)     | Blue jump wire, 1.25 cm    |
| VCC     | Right power rail (+)     | Orange jump wire, 2.25 cm  |
| SDA     | Pico **GP4** (h6)        | Blue dupont wire, 22 cm    |
| SCL     | Pico **GP5** (h7)        | Yellow dupont wire, 22 cm  |

---

## Expected readings

At room light (~500 lux), a typical GL5528 LDR has ~5 kΩ resistance:

```
V_mid = 3.3 × 5k / (10k + 5k) = 1.10 V
ADC   ≈ 21860 counts (16-bit)
```

In bright direct light (~3000 lux), LDR ≈ 1 kΩ → V_mid ≈ 0.30 V  
In near darkness, LDR ≈ 1 MΩ → V_mid ≈ 3.27 V

---

## Simulation

```bash
ngspice -b gpio_analog_sensing/gpio_analog_sensing.spice
```

Run from the repo root.  Node voltages are output with labeled column
headers corresponding to the `.print` directive node names.

| Signal | Meaning |
|--------|---------|
| `v(2)` | Bright-light node — R_fixed / R_bright (LDR ≈ 1 kΩ) |
| `v(3)` | Dim-light node — R_fixed / R_dim (LDR ≈ 50 kΩ) |
| `v(5)` | Potentiometer midpoint — R_fixed / R_pot (5 kΩ) |

At V_supply = 3.3 V, expected values: v(2) ≈ 0.30 V, v(3) ≈ 2.75 V,
v(5) ≈ 1.65 V.  Use these to predict ADC counts before building.
