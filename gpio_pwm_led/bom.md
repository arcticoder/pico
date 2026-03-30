# Stage 6 — GPIO PWM LED (`gpio_pwm_led/`)

PWM brightness control. **GP15** outputs a PWM signal; duty cycle controls LED brightness.

## Bill of materials

All parts are in [docs/inventory.md](../docs/inventory.md).

| Qty | Part | Value / notes |
|-----|------|--------------|
| 1 | White LED | 3.2 V forward voltage (typical) |
| 1 | Resistor | 220 Ω |
| 1 | Jump wire | Red, 2.5 cm (GP15 row → resistor) |
| 1 | Jump wire | Black, 1.5 cm (LED row → GND rail) |

## Planned files

```
gpio_pwm_led/
    main.py             MicroPython PWM duty-cycle sweep
    diagram.json        Wokwi layout
    gpio_pwm_led.spice  DC operating point (PWM mid-point approximation)
    gpio_pwm_led.gc     GnuCap batch script
    schematic.png       auto-generated schematic
    breadboard.md       step-by-step wiring guide
    README.md           build and run instructions
```
