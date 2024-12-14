from button import Button
from machine import ADC, Pin
from neopixel import NeoPixel
from time import sleep


class ButtonPressType:
    DOWN = 0
    PRESS = 1


class ButtonPressDuration:
    SHORT = 1000
    LONG = 2000
    LONGER = LONG + 1


class Badge:
    segments = (
        (31, 32, 33, 34),
        (26, 27, 28, 29, 30, 35),
        (19, 20, 21, 22, 23, 24, 25, 36, 37),
        (0, 1, 2, 3, 4, 5, 6, 17, 18),
        (7, 8, 9, 10, 11, 16),
        (12, 13, 14, 15),
    )

    # pixels = [
    #     [[12], [7, 8], [1, 2], [25, 36], [30, 35], [34]],
    #     [[13], [9], [0, 3], [24], [29], [33]],
    #     [[14, 15], [10], [4], [23, 37], [28], [31, 32]],
    #     [[], [11, 16], [5], [22], [26, 27], []],
    #     [[], [], [6, 18], [21], [], []],
    #     [[], [], [17], [19, 20], [], []],
    # ]

    # (0, 0) is in the lower left corner
    pixels = (
        ((), (), (), (14, 15), (13,), (12,)),
        ((), (), (11, 16), (10,), (9,), (7, 8)),
        ((17,), (6, 18), (5,), (4,), (0, 3), (1, 2)),
        ((19, 20), (21,), (22,), (23, 37), (24,), (25, 36)),
        ((), (), (26, 27), (28,), (29,), (30, 35)),
        ((), (), (), (31, 32), (33,), (34,)),
    )

    def __init__(self, np_pin_num=4, battsense_on_pin_num=5, button_pin_num=10):
        self.np = NeoPixel(Pin(np_pin_num), 38)

        self.battsense_on_pin = Pin(battsense_on_pin_num)
        # self.battsense = ADC(self.battsense_on_pin, atten=ADC.ATTN_11DB)

        self.button = Button(
            button_pin_num,
            thresholds_ms=[ButtonPressDuration.SHORT, ButtonPressDuration.LONG],
        )
        self.button.callback(self._button_cb)

    def _button_cb(self, state, threshold_idx):
        if state == 0:
            press_type = ButtonPressType.DOWN
        else:
            press_type = ButtonPressType.PRESS

        if threshold_idx == 0:
            press_duration = ButtonPressDuration.SHORT
        if threshold_idx == 1:
            press_duration = ButtonPressDuration.LONG
        if threshold_idx >= 2:
            press_duration = ButtonPressDuration.LONGER

        if self.callback_fn:
            self.callback_fn(press_type, press_duration)

    def callback(self, fn):
        self.callback_fn = fn

    # def get_vbat(self, sample_num=1000):
    #     value = 0
    #     for _ in range(sample_num):
    #         value += self.battsense.read_uv() * 2e-6
    #     value /= sample_num
    #     return value

    # power stuff
    def power(self, state=None):
        if state is None:
            # return self.get_vbat() > 1.0
            pass
        else:
            self.battsense_on_pin.init(Pin.OUT)
            self.battsense_on_pin(state)
            sleep(0.1)
            self.battsense_on_pin.init(Pin.IN)

    def off(self):
        self.power(0)

    def on(self):
        self.power(1)

    # neopixel stuff
    def set_pixels(self, data):
        for x in range(len(self.pixels)):
            for y in range(len(self.pixels[x])):
                for pixel in self.pixels[x][y]:
                    self.np[pixel] = data[x][y]

    def set_segment(self, segnum, color):
        for idx in self.segments[segnum]:
            self.np[idx] = color

    def set_segments(self, colors):
        for i in range(len(self.segments)):
            self.set_segment(i, colors[i])

    def set_all(self, color):
        self.np.fill(color)

    def flush(self):
        self.np.write()
