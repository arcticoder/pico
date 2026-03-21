from machine import Pin
import time

button = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(17, Pin.OUT)

while True:
    v = button.value()
    print(v)
    led.value(0 if v else 1)
    time.sleep_ms(20)