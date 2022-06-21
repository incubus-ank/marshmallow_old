from inputs import get_gamepad
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)
print(ser.name) 

while 1:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)

        if (event.code == 'ABS_HAT0X'):
            if (event.state == 1):
                ser.write(b'4')
            if (event.state == -1):
                ser.write(b'2')

        if (event.code == 'ABS_HAT0Y'):
            if (event.state == 1):
                ser.write(b'1')
            if (event.state == -1):
                ser.write(b'3')
        
        if (event.code == 'BTN_SOUTH' and event.state == 1):
            ser.write(b'0')

        if (event.code == 'BTN_NORTH' and event.state == 1):
            ser.write(b'0')
            ser.close()
            exit()

