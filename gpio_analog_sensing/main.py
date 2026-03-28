"""
gpio_analog_sensing/main.py
---------------------------
Analog sensing platform for Raspberry Pi Pico.

Hardware
--------
  GP26 (ADC0) — Photoresistor voltage-divider midpoint
                  3V3 → 10kΩ → (midpoint) → photoresistor → GND
                  100nF capacitor from midpoint to GND (low-pass filter)
  GP27 (ADC1) — Potentiometer wiper (0 → 10kΩ → 3.3V)
  GP15        — LED (controlled white light source for photoresistor)
  GP4  (SDA)  — I2C LCD 1602
  GP5  (SCL)  — I2C LCD 1602

What this measures
------------------
  * Raw ADC counts and converted voltage for each channel
  * Filtered voltage (moving average, configurable window)
  * Estimated sensor resistance (from voltage divider equation)
  * Calibration offset from potentiometer channel

Run from MicroPico (or rshell / mpremote):
  mpremote run main.py
"""

from machine import ADC, I2C, Pin, PWM
import time
import math

# ---------------------------------------------------------------------------
# Hardware configuration
# ---------------------------------------------------------------------------

ADC_LDR  = ADC(Pin(26))   # Photoresistor divider midpoint
ADC_POT  = ADC(Pin(27))   # Potentiometer calibration reference

LED_PIN  = Pin(15, Pin.OUT)  # Controlled light source (on/off; PWM optional)

I2C_BUS  = I2C(0, sda=Pin(4), scl=Pin(5), freq=400_000)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ADC_MAX   = 65535          # 16-bit ADC full scale
VREF      = 3.3            # Reference voltage (Pico 3V3_OUT)
R_FIXED   = 10_000         # Top resistor in voltage divider (Ω)
WINDOW    = 16             # Moving-average filter width (samples)
INTERVAL_MS = 100          # Sample interval

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def raw_to_voltage(raw: int) -> float:
    """Convert 16-bit ADC reading to voltage."""
    return raw * VREF / ADC_MAX


def voltage_to_resistance(v_out: float, v_in: float = VREF,
                           r_top: float = R_FIXED) -> float:
    """
    Voltage divider: 3V3 → R_top → (v_out) → R_sensor → GND
    Solve for R_sensor given v_out.
    """
    if v_out <= 0:
        return float("inf")
    if v_out >= v_in:
        return 0.0
    return r_top * (v_in - v_out) / v_out


def moving_average(buf: list) -> float:
    return sum(buf) / len(buf)


def measure_noise(adc: ADC, n: int = 200):
    """
    Measure noise floor: returns (mean_counts, std_dev_counts).
    Call at rest with stable illumination.
    """
    readings = [adc.read_u16() for _ in range(n)]
    mean = sum(readings) / n
    variance = sum((x - mean) ** 2 for x in readings) / n
    return mean, math.sqrt(variance)


def ldr_to_lux(r_sensor: float) -> float:
    """
    Rough lux estimate for a typical GL5528 photoresistor.
    Formula: lux ≈ (R0 / R_sensor) ** (1/gamma)
    with R0 = 10 kΩ at 10 lux, gamma ≈ 0.7 (empirical).
    Replace with calibrated values from your calibration_curve.py run.
    """
    R0    = 10_000.0
    lux0  = 10.0
    gamma = 0.7
    if r_sensor <= 0:
        return float("inf")
    return lux0 * (R0 / r_sensor) ** (1.0 / gamma)


# ---------------------------------------------------------------------------
# LCD helper (bare-metal I2C HD44780 via PCF8574 backpack)
# ---------------------------------------------------------------------------

LCD_ADDR = 0x27  # Common default; try 0x3F if not found

def _lcd_send(nibble: int, mode: int = 0) -> None:
    """Send a nibble to LCD via PCF8574."""
    backlight = 0x08
    byte = (nibble & 0xF0) | mode | backlight
    I2C_BUS.writeto(LCD_ADDR, bytes([byte | 0x04]))
    time.sleep_us(1)
    I2C_BUS.writeto(LCD_ADDR, bytes([byte & ~0x04]))
    time.sleep_us(50)


def lcd_cmd(cmd: int) -> None:
    _lcd_send(cmd & 0xF0, 0)
    _lcd_send((cmd << 4) & 0xF0, 0)


def lcd_char(ch: int) -> None:
    _lcd_send(ch & 0xF0, 1)
    _lcd_send((ch << 4) & 0xF0, 1)


def lcd_init() -> None:
    time.sleep_ms(50)
    for _ in range(3):
        _lcd_send(0x30, 0)
        time.sleep_ms(5)
    _lcd_send(0x20, 0)
    lcd_cmd(0x28)  # 4-bit, 2 lines, 5×8
    lcd_cmd(0x0C)  # display on, cursor off
    lcd_cmd(0x06)  # entry mode: increment, no shift
    lcd_cmd(0x01)  # clear
    time.sleep_ms(2)


def lcd_pos(col: int, row: int) -> None:
    offsets = [0x00, 0x40]
    lcd_cmd(0x80 | (offsets[row] + col))


def lcd_print(text: str) -> None:
    for ch in text:
        lcd_char(ord(ch))


def lcd_update(line1: str, line2: str) -> None:
    lcd_pos(0, 0)
    lcd_print(f"{line1:<16}"[:16])
    lcd_pos(0, 1)
    lcd_print(f"{line2:<16}"[:16])


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    # Initialise LCD (non-fatal if not connected)
    lcd_ok = False
    try:
        devices = I2C_BUS.scan()
        if LCD_ADDR in devices:
            lcd_init()
            lcd_ok = True
    except Exception as exc:
        print(f"LCD init failed: {exc}")

    LED_PIN.value(1)          # Turn on LED light source at startup

    ldr_buf: list  = []
    pot_buf: list  = []

    print("gpio_analog_sensing — press Ctrl-C to stop")
    print(f"{'ADC_RAW':>7}  {'V_raw':>6}  {'V_filt':>6}  "
          f"{'R_sens(Ω)':>10}  {'~lux':>6}  {'V_pot':>6}")

    while True:
        raw_ldr = ADC_LDR.read_u16()
        raw_pot = ADC_POT.read_u16()

        v_ldr = raw_to_voltage(raw_ldr)
        v_pot = raw_to_voltage(raw_pot)

        ldr_buf.append(v_ldr)
        if len(ldr_buf) > WINDOW:
            ldr_buf.pop(0)

        pot_buf.append(v_pot)
        if len(pot_buf) > WINDOW:
            pot_buf.pop(0)

        v_filtered = moving_average(ldr_buf)
        r_sense    = voltage_to_resistance(v_filtered)
        lux_est    = ldr_to_lux(r_sense)

        print(f"{raw_ldr:>7}  {v_ldr:>6.3f}  {v_filtered:>6.3f}  "
              f"{r_sense:>10.0f}  {lux_est:>6.1f}  {v_pot:>6.3f}")

        if lcd_ok:
            lcd_update(
                f"V={v_filtered:.3f} {lux_est:.0f}lx",
                f"R={r_sense:.0f}  Pot={v_pot:.2f}V"
            )

        time.sleep_ms(INTERVAL_MS)


if __name__ == "__main__":
    main()
