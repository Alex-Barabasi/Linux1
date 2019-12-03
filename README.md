Usage
-

Use the following command to send actions to robot

echo 'command' | socat - tcp:192.168.99.7:8080

Supported commands:
- Standard commands: gedist, getmotors, start, stop 
- Extra commands: inceasespeed, decreasespeed (increase/decrease speed by 10 % - will also return the new speed) 
- Extra commands: increasep, decreasep (increase/decrease the proportional gain by 0.1) 
- Extra commands: increased, decreased (increase/decrease the differential gain by 0.25)


How the wall follower works
-
The controller is build as a PD-controller with a set goal distance. The default goal distance is 30 cm. 
The PD-controller gaints can be increased/decreased through socket.  


System
-
- Distribution: Raspbian Buster 10 - Lite
- Ptyhon version:2.7 
- Lib: gpiozero - For controlling the GPIO's 
