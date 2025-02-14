# This example demonstrates a peripheral implementing the Nordic UART Service (NUS).

import bluetooth
from ble_advertising import advertising_payload

from micropython import const

_IRQ_GATTS_WRITE = const(3)

_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class BLEUART:
    def __init__(self, ble, connections, rxbuf=100):
        self._ble = ble
        self._rxbuf = rxbuf
        self._rx_buffer = bytearray()
        self._connections = connections
        self._handler = None

    @property
    def handles(self):
        return (self._tx_handle, self._rx_handle)

    @handles.setter
    def handles(self, handles):
        self._tx_handle, self._rx_handle = handles
        # Increase the size of the rx buffer and enable append mode.
        self._ble.gatts_set_buffer(self._rx_handle, self._rxbuf, True)

    @property
    def service(self):
        return _UART_SERVICE

    def irq(self, handler):
        self._handler = handler

    def irq_cb(self, event, data):
        if event == _IRQ_GATTS_WRITE:
            _, value_handle = data
            if value_handle == self._rx_handle:
                self._rx_buffer += self._ble.gatts_read(self._rx_handle)
                if self._handler:
                    self._handler()

    def any(self):
        return len(self._rx_buffer)

    def read(self, sz=None):
        if not sz:
            sz = len(self._rx_buffer)
        result = self._rx_buffer[0:sz]
        self._rx_buffer = self._rx_buffer[sz:]
        return result

    def write(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def close(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
