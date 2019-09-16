BASEDIR=$(dirname "$0")
parentdir="$(dirname "$BASEDIR")"

rfkill unblock bluetooth

$HOME/.cache/pypoetry/virtualenvs/bluetooth-ble-sniffer-py2.7/bin/python $parentdir/main.py