echo "Restoring network interfaces configuration.\n"

echo "Deleting mon0 interface"
sudo iw dev mon0 del
if [ $? -eq 0 ]; then
    echo "> OK"
else
    echo "> FAIL"
fi
echo "Adding $1 to enable connectivity"
sudo iw phy phy0 interface add $1 type managed
if [ $? -eq 0 ]; then
    echo "> OK"
else
    echo "> FAIL"
fi

echo "\nNetwork interfaces configuration restored."

