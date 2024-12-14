from json import load
from network import WLAN


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
