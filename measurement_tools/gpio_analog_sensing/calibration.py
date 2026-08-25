"""
gpio_analog_sensing/calibration.py
------------------------------------
Build and apply calibration curves for the photoresistor voltage-divider.

Workflow
--------
1. Run `collect()` with known light levels (or block/expose the sensor)
   to gather (voltage, known_value) pairs.
2. Run `fit()` to compute a polynomial or power-law fit.
3. Run `apply()` to convert raw ADC readings to calibrated physical values.
4. Print/inspect the `noise_report()` before collecting — high noise
   will degrade your calibration.

Usage (interactive on Pico via mpremote REPL)
---------------------------------------------
  from calibration import NoiseReport, CalibrationCurve
  nr = NoiseReport(adc_pin=26)
  nr.run()               # prints mean, std-dev, SNR

  cal = CalibrationCurve(adc_pin=26)
  cal.add_point(voltage=0.35, known_value=1000)   # bright: ~1kΩ
  cal.add_point(voltage=1.65, known_value=10000)  # dark:  ~10kΩ
  cal.add_point(voltage=2.75, known_value=50000)  # very dark: ~50kΩ
  cal.fit(degree=1)       # fit log-log line (power law)
  print(cal.predict(1.20))
  cal.save("cal_ldr.json")
"""

import math
import json
import time
from machine import ADC, Pin


ADC_MAX = 65535
VREF    = 3.3


def raw_to_voltage(raw: int) -> float:
    return raw * VREF / ADC_MAX


# ---------------------------------------------------------------------------
# Noise characterisation
# ---------------------------------------------------------------------------

class NoiseReport:
    """Measure ADC noise floor at rest."""

    def __init__(self, adc_pin: int = 26, n_samples: int = 500):
        self.adc = ADC(Pin(adc_pin))
        self.n   = n_samples

    def run(self) -> dict:
        readings = [self.adc.read_u16() for _ in range(self.n)]
        mean  = sum(readings) / self.n
        var   = sum((x - mean) ** 2 for x in readings) / self.n
        std   = math.sqrt(var)
        snr   = mean / std if std > 0 else float("inf")
        v_mean = raw_to_voltage(int(mean))
        v_std  = raw_to_voltage(int(std))

        report = {
            "n_samples": self.n,
            "mean_counts": mean,
            "std_counts": std,
            "snr": snr,
            "mean_voltage": v_mean,
            "std_voltage": v_std,
        }
        print("--- Noise Report ---")
        print(f"  Samples    : {self.n}")
        print(f"  Mean       : {mean:.1f} counts  ({v_mean:.4f} V)")
        print(f"  Std-dev    : {std:.2f} counts  ({v_std*1000:.3f} mV)")
        print(f"  SNR        : {snr:.1f}")
        return report


# ---------------------------------------------------------------------------
# Multi-point calibration
# ---------------------------------------------------------------------------

class CalibrationCurve:
    """
    Power-law calibration: known_value = A * voltage ^ B
    Fit is done in log-log space (linear regression).
    """

    def __init__(self, adc_pin: int = 26, n_avg: int = 50):
        self.adc    = ADC(Pin(adc_pin))
        self.n_avg  = n_avg
        self.points = []   # list of (voltage, known_value)
        self._A     = None
        self._B     = None

    def _read_voltage(self) -> float:
        samples = [self.adc.read_u16() for _ in range(self.n_avg)]
        return raw_to_voltage(int(sum(samples) / self.n_avg))

    def capture_point(self, known_value: float) -> float:
        """Read current ADC voltage and pair with a known physical value."""
        v = self._read_voltage()
        self.add_point(v, known_value)
        print(f"  Captured: V={v:.4f}  known={known_value}")
        return v

    def add_point(self, voltage: float, known_value: float) -> None:
        self.points.append((voltage, known_value))

    def fit(self) -> tuple:
        """
        Power-law fit: y = A * x ^ B  →  log(y) = log(A) + B*log(x)
        Requires at least 2 data points.
        """
        if len(self.points) < 2:
            raise ValueError("Need at least 2 calibration points")

        xs = [math.log(v) for v, _ in self.points if v > 0]
        ys = [math.log(k) for _, k in self.points if k > 0]
        n  = len(xs)

        sx  = sum(xs)
        sy  = sum(ys)
        sxx = sum(x * x for x in xs)
        sxy = sum(x * y for x, y in zip(xs, ys))

        denom = n * sxx - sx * sx
        if abs(denom) < 1e-12:
            raise ValueError("Degenerate fit: all x values identical")

        B         = (n * sxy - sx * sy) / denom
        log_A     = (sy - B * sx) / n
        self._A   = math.exp(log_A)
        self._B   = B

        print(f"  Calibration fit: y = {self._A:.4f} * V ^ {self._B:.4f}")
        return self._A, self._B

    def predict(self, voltage: float) -> float:
        """Apply calibration curve to a measured voltage."""
        if self._A is None:
            raise RuntimeError("Call fit() first")
        return self._A * (voltage ** self._B)

    def save(self, filename: str = "cal_ldr.json") -> None:
        data = {
            "points": self.points,
            "A": self._A,
            "B": self._B,
        }
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"  Calibration saved to {filename}")

    def load(self, filename: str = "cal_ldr.json") -> None:
        with open(filename) as f:
            data = json.load(f)
        self.points = data["points"]
        self._A     = data["A"]
        self._B     = data["B"]
        print(f"  Calibration loaded from {filename}  "
              f"(A={self._A:.4f}, B={self._B:.4f})")


# ---------------------------------------------------------------------------
# Drift measurement utility
# ---------------------------------------------------------------------------

def measure_drift(adc_pin: int = 26, duration_s: int = 120,
                  interval_s: int = 5) -> list:
    """
    Log voltage every `interval_s` seconds for `duration_s` seconds.
    Returns list of (elapsed_s, voltage) tuples.
    Call with stable illumination to check for thermal or power-supply drift.
    """
    adc  = ADC(Pin(adc_pin))
    log  = []
    t0   = time.ticks_ms()
    print(f"Drift measurement: {duration_s}s, sampling every {interval_s}s")
    print(f"{'time_s':>7}  {'voltage':>8}")
    while True:
        elapsed = time.ticks_diff(time.ticks_ms(), t0) / 1000
        v = raw_to_voltage(adc.read_u16())
        log.append((elapsed, v))
        print(f"{elapsed:>7.1f}  {v:>8.4f}")
        if elapsed >= duration_s:
            break
        time.sleep(interval_s)
    return log
