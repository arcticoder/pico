from machine import Pin
import time

button = Pin(16, Pin.IN)
led = Pin(17, Pin.OUT)

last_state = 0

while True:
    state = button.value()

    if state == 1 and last_state == 0:
        t = time.ticks_us()
        print("Pressed at:", t)

    led.value(state)

    last_state = state
    time.sleep_ms(1)