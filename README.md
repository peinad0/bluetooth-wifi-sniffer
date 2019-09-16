# Bluetooth and Wi-Fi Sniffer

Scripts to listen for Bluetooth and Wi-Fi packets and send the hashed address to a configured IOT Agent.

## Requirements

* Orion context broker running and configured.
* IOTAgent Ultralight running and configured.

## Usage

### Wi-Fi

```
sudo ./wifi/scripts/run.sh
```

It is recommended to restore network interfaces after running the script.

```
sudo ./wifi/scripts/restore.sh
```


### Bluetooth

```
sudo ./bluetooth/scripts/run.sh
```

### Bluetooth low energy

```
sudo ./bluetooth-ble/scripts/run.sh
```