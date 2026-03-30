# Stage 8 — I2C LCD 1602 display (`gpio_i2c_lcd/`)

Drive an I2C LCD 1602 (PCF8574 backpack) from the Pico.  **GP4/SDA** and
**GP5/SCL** carry the I2C bus; the library in `lib/lcd1602.py` handles the
protocol.

## Bill of materials

All parts are in [docs/inventory.md](../docs/inventory.md).

| Qty | Part | Value / notes |
|-----|------|--------------|
| 1 | I2C LCD 1602 | PCF8574T backpack; default I2C address 0x27 |
| 2 | Dupont wire | Red 22 cm M-F (VCC) |
| 2 | Dupont wire | Black 22 cm M-F (GND) |
| 1 | Dupont wire | Yellow 22 cm M-F (SDA — Pico GP4) |
| 1 | Dupont wire | Blue 22 cm M-F (SCL — Pico GP5) |

## Planned files

```
gpio_i2c_lcd/
    main.py             MicroPython I2C scan + LCD write
    diagram.json        Wokwi layout
    gpio_i2c_lcd.spice  I2C bus pull-up DC netlist
    gpio_i2c_lcd.gc     GnuCap batch script
    schematic.png       auto-generated schematic
    breadboard.md       step-by-step wiring guide
    README.md           build and run instructions
```

## Notes

- Default backpack contrast trim-pot position may need adjusting before text is visible.
- Run `i2c.scan()` first to confirm the device address (expect `[39]` = 0x27).
- `lib/lcd1602.py` is already present in the repo root `lib/` directory.
