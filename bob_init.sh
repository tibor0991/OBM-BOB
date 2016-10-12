#! /bin/bash
# by starting multiple python instances instead of stuffing them together
# in one process I can sidestep the GIL and the multiprocessing limitations
sudo killall python
echo "OBM B.O.B. - Baby On Board"
sudo python bob-main/main.py &
sleep 3
sudo python bob-lcdgui/main.py &
sudo python bob-7seg/main.py &
sudo python bob-mqtt/main.py &
sudo python bob-ext/main.py &
sudo python restarter.py &

