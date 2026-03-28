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

## Pico pinout reference (seated far left, rows 1–20)

| Row | Col e (left)  | Col f (right)    |
|-----|---------------|------------------|
|  3  | **GND** ←     | GND              |
|  5  | GP3           | **3V3_OUT** ←    |
|  6  | **GP4 (SDA)**←| ADC_VREF         |
|  7  | **GP5 (SCL)**←| GP28 (ADC2)      |
|  8  | GND           | AGND             |
|  9  | GP6           | **GP27 (ADC1)**← |
| 10  | GP7           | **GP26 (ADC0)**← |
| 20  | **GP15** ←    | GP16             |

---

## Parts required

| Component              | Value  | Qty |
|------------------------|--------|-----|
| Photoresistor (LDR)    | —      | 1   |
| Resistor (fixed, top)  | 10 kΩ  | 1   |
| Capacitor (filter)     | 100 nF | 1   |
| Potentiometer          | 10 kΩ  | 1   |
| LED (white)            | —      | 1   |
| Resistor (LED limit)   | 220 Ω  | 1   |
| I2C LCD 1602           | —      | 1   |
| Jumper wires           | —      | ~12 |

---

## Wiring steps

### 1. Power rails

| From                              | To                       | Wire |
|-----------------------------------|--------------------------|------|
| Pico **3V3_OUT** (row 5, col f)   | Top red rail (+)         | Red  |
| Pico **GND** (row 3, col e)       | Top blue rail (−)        | Black|

---

### 2. Voltage divider (LDR sensing — rows 22–28)

The 10 kΩ fixed resistor sits **above** the midpoint; the LDR sits **below**.

| Step | Component       | From        | To            | Wire   |
|------|-----------------|-------------|---------------|--------|
| a    | Wire             | Red rail (+) | Row 22, col a | Red    |
| b    | R_fixed (10 kΩ) leg 1 | Row 22, col a | Row 24, col a | — |
| c    | R_fixed leg 2   | Row 24, col a | = V_mid node  | —      |
| d    | LDR leg 1       | Row 24, col b | = V_mid node  | —      |
| e    | LDR leg 2       | Row 26, col b | Blue rail (−) | Black  |

**V_mid signal wire (to ADC0):**

| From              | To                          | Wire   |
|-------------------|-----------------------------|--------|
| Row 24, col c     | Pico **GP26** (row 10, col f) | Cyan |

---

### 3. Filter capacitor (100 nF — rows 24–26)

Connects V_mid to GND; bridging the gap is fine.

| Capacitor leg | Position       |
|---------------|----------------|
| + (or any)    | Row 24, col d  |
| −             | Row 26, col d → blue rail |

---

### 4. Potentiometer (rows 32–36, calibration reference)

| Pot terminal | Connection             | Wire   |
|--------------|------------------------|--------|
| VCC          | Red rail (+)           | Red    |
| GND          | Blue rail (−)          | Black  |
| Wiper (SIG)  | Pico **GP27** (row 9, col f) | Purple |

---

### 5. White LED (controlled light source — rows 40–44)

Aim the LED toward the photoresistor for repeatable controlled illumination.

| Step | From                       | To              | Wire   |
|------|----------------------------|-----------------|--------|
| a    | Pico **GP15** (row 20, col e) | Row 40, col e | Green  |
| b    | R_led (220 Ω) leg 1        | Row 40, col e   | —      |
| c    | R_led leg 2                | Row 42, col e   | —      |
| d    | LED anode (+)              | Row 42, col e   | —      |
| e    | LED cathode (−)            | Row 44, col e   | —      |
| f    | Row 44, col e              | Blue rail (−)   | Black  |

---

### 6. I2C LCD 1602 (far right side of breadboard)

Use the **4-pin I2C backpack version**:

| LCD pin | Connection             | Wire   |
|---------|------------------------|--------|
| GND     | Blue rail (−)          | Black  |
| VCC     | Red rail (+)           | Red    |
| SDA     | Pico **GP4** (row 6, col e) | Blue |
| SCL     | Pico **GP5** (row 7, col e) | Yellow |

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
gnucap -b gpio_analog_sensing/gpio_analog_sensing.gc
```

Compare `v(2)` (bright), `v(3)` (dim), `v(5)` (pot mid) in the output to
predict expected ADC readings before building.
