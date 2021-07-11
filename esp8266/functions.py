import time
from machine import Pin, PWM

pins = [12, 14, 13]

min_brightness = 0
max_brightness = 255


def pwm_change(pin, brightness, delay):
    pwm = PWM(Pin(pin), freq=20000, duty=brightness)
    time.sleep_ms(delay)


def all_on():
    for elements in pins:
        pwm_change(elements, max_brightness, 10)


def all_off():
    for elements in pins:
        pwm_change(elements, min_brightness, 10)


def all_fade_on():
    for duty_cycle in range(min_brightness, max_brightness + 1):
        for elements in pins:
            pwm_change(elements, duty_cycle, 3)


def all_fade_off():
    for duty_cycle in range(max_brightness + 1, min_brightness, -1):
        for elements in pins:
            pwm_change(elements, duty_cycle, 3)


def red_on():
    rgb = [255, 0, 0]
    for i in range(0, 3):
        pwm_change(pins[i], rgb[i], 10)


def green_on():
    rgb = [0, 255, 0]
    for i in range(0, 3):
        pwm_change(pins[i], rgb[i], 10)


def blue_on():
    rgb = [0, 0, 255]
    for i in range(0, 3):
        pwm_change(pins[i], rgb[i], 10)


def choose_color(r, g, b):
    rgb = [r, g, b]
    for i in range(0, 3):
        pwm_change(pins[i], rgb[i], 10)


def get_colors() -> [str, str, str]:
    return [PWM(Pin(pins[0])).duty(), PWM(Pin(pins[1])).duty(), PWM(Pin(pins[2])).duty()]

