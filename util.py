from ble_advertising import advertising_payload
from ble_uart_peripheral import BLEUART
from ble_uart_repl import BLEUARTStream
from bluetooth import BLE
from json import load
from micropython import const
from network import WLAN
import uos

# org.bluetooth.characteristic.gap.appearance.xml
ADV_APPEARANCE_GENERIC_COMPUTER = const(128)
ADV_APPEARANCE_GENERIC_HEART_RATE_SENSOR = const(832)

IRQ_CENTRAL_CONNECT = const(1)
IRQ_CENTRAL_DISCONNECT = const(2)

payload = advertising_payload(
    name="Geheimbadge", appearance=ADV_APPEARANCE_GENERIC_COMPUTER
)


def wifi_connect(ssid="", psk=""):

    wlan = WLAN(WLAN.IF_STA)
    wlan.active(True)

    if wlan.isconnected():
        wlan.disconnect()

    if not ssid:
        with open("sta.json") as sta_json:
            sta_dict = load(sta_json)

        scan_results = wlan.scan()
        scan_ssids = [scan_result[0].decode() for scan_result in scan_results]

        for dict_ssid in sta_dict:
            if dict_ssid in scan_ssids:
                ssid = dict_ssid
                psk = sta_dict[ssid]
                break

    if ssid:
        wlan.connect(ssid, psk)
        while not wlan.isconnected():
            pass
        print("network config:", wlan.ipconfig("addr4"))
        return True
    else:
        return False


def ble_repl():
    # Activate bluetooth
    ble = BLE()
    ble.active(True)
    connections = set()

    # Initialize UART REPL
    uart = BLEUART(ble, connections)
    stream = BLEUARTStream(uart)
    uos.dupterm(stream)

    def ble_irq_cb(event, data):
        # Track connections so we can send notifications.
        if event == IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            connections.add(conn_handle)
        elif event == IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in connections:
                connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            ble.gap_advertise(500000, adv_data=payload)
        else:
            if len(data) == 2:
                conn_handle, value_handle = data
                if conn_handle in connections:
                    if value_handle in uart.handles:
                        uart.irq_cb(event, data)

    ble.irq(ble_irq_cb)

    # All BLE services must be registered at once
    (uart.handles,) = ble.gatts_register_services((uart.service,))

    ble.gap_advertise(500000, adv_data=payload)
