BASEDIR=$(dirname "$0")
parentdir="$(dirname "$BASEDIR")"
NETWORK_INTERFACE=${1:-wlp2s0}    

$BASEDIR/configure.sh $NETWORK_INTERFACE

$HOME/.cache/pypoetry/virtualenvs/wifi-sniffer-py2.7/bin/python $parentdir/main.py

$BASEDIR/restore.sh $NETWORK_INTERFACE