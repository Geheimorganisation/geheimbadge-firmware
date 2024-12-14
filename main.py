from animation import TestAnimation, GameOfLife, FlagCycleAnimation

from badge import Badge, ButtonPressType, ButtonPressDuration
from flags import flags
from machine import Timer
from random import choice
from util import wifi_connect
import webrepl

badge = Badge(np_pin_num=20, battsense_on_pin_num=14, button_pin_num=7)
tim = Timer(0)
test_animation = TestAnimation()

animation_idx = 0
animations = [
    {"animation": FlagCycleAnimation(), "delay_ms": 5000},
    {"animation": GameOfLife(), "delay_ms": 500},
    {"animation": TestAnimation(), "delay_ms": 200},
]


def start_animation(animation, delay_ms):
    tim.deinit()

    def timer_cb(t):
        badge.set_pixels(animation.canvas)
        badge.flush()
        animation.tick()
        tim.init(period=delay_ms, mode=Timer.ONE_SHOT, callback=timer_cb)

    timer_cb(tim)


def stop_animation():
    tim.deinit()
    badge.set_all([0, 0, 0])
    badge.flush()


def next_animation():
    global animation_idx, animations
    stop_animation()
    animation = animations[animation_idx]
    start_animation(animation["animation"], animation["delay_ms"])
    animation_idx = (animation_idx + 1) % len(animations)


def button_cb(press_type, press_duration):
    if press_type == ButtonPressType.PRESS:
        if press_duration == ButtonPressDuration.SHORT:
            next_animation()
        if press_duration == ButtonPressDuration.LONGER:
            badge.off()


badge.callback(button_cb)
next_animation()

connected = wifi_connect()
if connected:
    webrepl.start(password="geheim")
