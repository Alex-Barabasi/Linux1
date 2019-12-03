Usage
-

Use the following command to send actions to robot

echo 'command' | socat - tcp:192.168.99.7:8080

Supported commands:
- Standard commands: gedist, getmotors, start, stop 
- Extra commands: inceasespeed, decreasespeed (increase/decrease speed by 10 % - will return the new speed) 
- Extra commands: increasekp, decreasekp (increase/decrease the proportional gain by 0.1 - will return the new speed) 
- Extra commands: increasekd, decreasekd (increase/decrease the differential gain by 0.1 - will return the new speed)


How the wall follower works
-
The controller is build as a PD-controller with a set goal distance. The default goal distance is 30 cm. 
The PD-controller gains can be increased/decreased through socket.  


System
-
- Distribution: Raspbian Buster 10 - Lite - https://www.raspberrypi.org/downloads/raspbian/
- Ptyhon version:2.7 
- Lib: gpiozero - For controlling the GPIO's - https://gpiozero.readthedocs.io/en/stable/
- CamJam EduKit 3 - https://camjam.me/?page_id=1035
