echo "Setting up network interfaces\n"

echo "Adding mon0 monitor interface"
sudo iw phy phy0 interface add mon0 type monitor
if [ $? -eq 0 ]; then
    echo "> OK"
else
    echo "> FAIL"
fi
echo "Deleting $1 (might fail if network is named differently)"

sudo iw dev $1 del
if [ $? -eq 0 ]; then
    echo "> OK"
else
    echo "> FAIL"
fi
echo "Starting mon0 interface"
sudo ifconfig mon0 up
if [ $? -eq 0 ]; then
    echo "> OK"
else
    echo "> FAIL"
fi
echo "Set mon0 frequency to 2437Hz"
sudo iw dev mon0 set freq 2437
if [ $? -eq 0 ]; then
    echo "> OK"
else
    echo "> FAIL"
fi

echo "\nFinished setting up network interfaces"
