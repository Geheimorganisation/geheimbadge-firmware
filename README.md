# Geheimbadge Firmware
This is the Geheimbadge firmware.
It wares the Geheimbadge firm.

## Deployment
Run `nix-shell` in this repo to enter an environment with all necessary tools.
Replace `/dev/ttyACM0` with the correct port for your system.

### Micropython
Download the latest [Firmware Release](https://micropython.org/download/esp32c6/) .bin file.
Flash the firmware using [esptool](https://github.com/espressif/esptool).

```shell
esptool.py --chip esp32c6 --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32c6 --port /dev/ttyACM0 write_flash -z 0x0 esp32c6-20241129-v1.24.1.bin
```

### Scripts
Deployment via [rshell](https://github.com/dhylands/rshell) is recommendet.

```shell
rshell --port /dev/ttyACM0 "cp ./*.py /pyboard"
```

### WiFi Config
Copy `sta-template.json` to `sta.json` and edit.
```shell
rshell --port /dev/ttyACM0 "cp ./sta.json /pyboard"
```
