from machine import Pin, Timer
from time import ticks_ms


class Button:
    def __init__(self, pin_num, pull=Pin.PULL_UP, thresholds_ms=[1000, 3000]):
        self.pin = Pin(pin_num, Pin.IN, pull)
        self.pin_state = 1 if Pin.PULL_UP else 0
        self.thresholds_ms = thresholds_ms
        self.threshold_idx = 0
        self.timer = Timer(2)

        self.pin.irq(self._isr)

    def _timer_cb(self, timer):
        self.threshold_idx += 1
        if self.threshold_idx < len(self.thresholds_ms):
            timer.init(
                period=self.thresholds_ms[self.threshold_idx]
                - self.thresholds_ms[self.threshold_idx - 1],
                mode=Timer.ONE_SHOT,
                callback=self._timer_cb,
            )

        if self.callback_fn:
            self.callback_fn(self.pin_state, self.threshold_idx)

    def _isr(self, pin):
        pin_state = pin()
        if pin_state != self.pin_state:
            self.pin_state = pin_state

            if pin_state == 0:
                self.threshold_idx = 0
                self.timer.init(
                    period=self.thresholds_ms[self.threshold_idx],
                    mode=Timer.ONE_SHOT,
                    callback=self._timer_cb,
                )
            else:
                self.timer.deinit()

            if self.callback_fn:
                self.callback_fn(pin_state, self.threshold_idx)

    def callback(self, fn):
        self.callback_fn = fn
