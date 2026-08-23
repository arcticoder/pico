# Component Inventory

Parts available from the **SunFounder Thales Kit** and other sources.
Update quantities as components are used or added.

---

## LEDs

| Component  | Quantity |
|------------|----------|
| Red LED    | 10       |
| Blue LED   | 10       |
| Green LED  | 10       |
| White LED  | 10       |
| Yellow LED | 10       |
| RGB LED    | 1        |

---

## Resistors

| Value   | Quantity |
|---------|----------|
| 10 Ω    | 10       |
| 100 Ω   | 10       |
| 220 Ω   | 10       |
| 330 Ω   | 10       |
| 1 kΩ    | 10       |
| 2 kΩ    | 10       |
| 5.1 kΩ  | 10       |
| 10 kΩ   | 10       |
| 100 kΩ  | 10       |
| 1 MΩ    | 10       |

---

## Active Components and Sensors

| Component                     | Quantity | Notes                              |
|-------------------------------|----------|------------------------------------|
| S8550 Transistor (PNP)        | 2        |                                    |
| S8050 Transistor (NPN)        | 2        |                                    |
| Tilt Switch                   | 1        |                                    |
| Potentiometer                 | 1        |                                    |
| 100 nF Capacitor              | 10       |                                    |
| 10 nF Capacitor               | 10       |                                    |
| Photoresistor (LDR)           | 2        |                                    |
| Thermistor (NTC)              | 1        | Suspect faulty — prefer photoresistor for initial analog experiments |
| 9G Servo                      | 1        |                                    |
| PIR Motion Sensor             | 1        |                                    |
| 74HC595 Shift Register        | 1        |                                    |

---

## Output and Interface

| Component               | Quantity | Notes                        |
|-------------------------|----------|------------------------------|
| Passive Buzzer          | 1        |                              |
| Active Buzzer           | 1        |                              |
| 7-Segment Display       | 1        |                              |
| I2C LCD 1602            | 1        |                              |
| WS2812 RGB LED Strip    | 1        | 8-LED strip                  |
| Slide Switch            | 5        |                              |
| Push Button             | 10       |                              |

---

## Prototyping and Cables

| Component              | Quantity | Notes                                                    |
|-------------------------|----------|-----------------------------------------------------------|
| Breadboard (full)      | 1        | 830-point                                                 |
| Breadboard (mini SYB-170) | 1     | 170-point, black; from a 6-in-1 color pack (AliExpress). See `lab/docs/orders.md` / `lab/docs/parts_reference.md` for full specs |
| Micro USB Cable        | 1        | For Pico power + data                                     |

---

## Jump Wires (solid-core, pre-bent 90°)

### Jump Wires Box — Left Side

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Orange | 2.25        | 14       |
| Red    | 2.5         | 10       |
| Black  | 1.5         | 14       |

### Jump Wires Box — Middle Left

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| White  | 1.5         | 14       |
| White  | 5           | 10       |
| Yellow | 2           | 12       |

### Jump Wires Box — Middle Right

| Colour      | Length (cm) | Quantity |
|-------------|-------------|----------|
| Black       | 0.4         | 10       |
| Yellow      | 0.6         | 10       |
| Green       | 1.0         | 10       |
| Blue        | 1.25        | 10       |
| Non-covered | 0.25        | 13       |

### Jump Wires Box — Middle Top

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Green  | 7.5         | 10       |
| Blue   | 10          | 10       |

### Jump Wires Box — Middle Bottom

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Red    | 12.6        | 10       |

---

## Jumper Wires (M-M Dupont, pre-cut)

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Blue   | 16          | 2        |
| Red    | 16          | 2        |
| Black  | 16          | 2        |
| Red    | 20          | 1        |
| Blue   | 20          | 1        |
| White  | 20          | 1        |
| Blue   | 25          | 1        |
| White  | 25          | 1        |
| Red    | 25          | 1        |
| Black  | 25          | 1        |
| White  | 12          | 7        |
| Black  | 12          | 7        |
| Orange | 12          | 7        |
| Blue   | 12          | 7        |
| Green  | 12          | 7        |
| Yellow | 12          | 7        |
| Red    | 12          | 7        |

---

## Dupont Wires (M-F)

| Colour | Length (cm) | Quantity |
|--------|-------------|----------|
| Red    | 22          | 1        |
| Yellow | 22          | 1        |
| Grey   | 22          | 1        |
| Orange | 22          | 1        |
| Green  | 22          | 1        |
| Blue   | 22          | 1        |
| Purple | 22          | 1        |
| Black  | 22          | 1        |
| White  | 22          | 1        |
| Beige  | 22          | 1        |
---

## Microcontroller

| Component              | Quantity | Notes                         |
|------------------------|----------|-------------------------------|
| Raspberry Pi Pico      | 1        | RP2040, no wireless           |

---

## Power Supply & Protection Components

For the `lab/` repo's spacetime research PSU tiers (`psu_ultralow`,
`psu_low`). Full specs and datasheets in `lab/docs/orders.md` and
`lab/docs/parts_reference.md`.

| Component                              | Quantity | Notes                                                           |
|------------------------------------------|----------|------------------------------------------------------------------|
| Polyfuse RXEF005 (0.05A / 50mA)         | 20       | Received 2026-08-21; untested — validate each unit with `lab/measurement_tools/fuse_test_voltmeter/` before trusting it near an LED |
| Polyfuse RXEF050 (0.5A / 500mA)         | 20       | Received 2026-08-21; untested — same validation step as above    |
| 1N5817 Schottky diode (1A 20V, DO-41)   | 20       | Received 2026-08-21; untested — verify forward drop/orientation per unit before use in `psu_low_v2` |
| AA battery holder (1×AA, single-cell)  | 5        | Received 2026-08-21; ready for direct use in `psu_ultralow_v1`/`psu_low_v2` |

---

## On Order (AliExpress — not yet received as of 2026-08-21)

Placed for the `lab/` repo's spacetime research build; not yet counted in
the tables above. Full specs, links, and datasheets in `lab/docs/orders.md`
and `lab/docs/parts_reference.md`. Move each row up into its proper table
above once physically received.

| Component                     | Quantity | Notes                                              |
|--------------------------------|----------|-----------------------------------------------------|
| Breadboard (mini SYB-170, 2pk) | 2        | Separate listing from the received black one above |
| Breadboard (MB-102, 400-point) | 1        | 300 terminal + 100 distribution-bar tie points      |
| CD4066BCN (quad bilateral switch, DIP-14) | 10 | Analog switch/mux                              |
| LM358P (dual op-amp, DIP-8)    | 10       | Budget op-amp for bring-up circuits                 |
| TYPE-C Female Test Board (USB3.1 16P → 2.54mm) | 1 | Blue variant                                   |
