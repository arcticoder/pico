# Interrupt-driven button input (`buttons/gpio_interrupt_button/`)

Interrupt (IRQ) handler on **GP16**.  The handler fires on the rising edge
(button press) and falling edge (release) without polling.

## Bill of materials

All parts are in [docs/inventory.md](../../docs/inventory.md).

| Qty | Part | Value / notes |
|-----|------|--------------|
| 1 | Push button | SPDT tactile, fits breadboard |
| 1 | Resistor | 10 kΩ (pull-down) |

## Planned files

```
gpio_interrupt_button/
    main.py                     MicroPython IRQ handler + debounce
    gpio_interrupt_button.spice DC netlist (pull-down divider operating point)
    gpio_interrupt_button.gc    GnuCap batch script
    schematic.png               auto-generated schematic
    breadboard.md               step-by-step wiring guide
    README.md                   build and run instructions
```
