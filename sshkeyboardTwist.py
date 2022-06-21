from sshkeyboard import listen_keyboard
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)
print(ser.name) 

keyout = 0

def press(key):
    if ( key == 'w'):
        ser.write(b'1')
    if ( key == 's'):
        ser.write(b'3')
    if ( key == 'd'):
        ser.write(b'4')
    if ( key == 'a'):
        ser.write(b'2')
    if ( key == 'q'):
        ser.write(b'5')
    if ( key == 'e'):
        ser.write(b'6')
    if ( key == 'h'):
        ser.write(b'7')
    if ( key == 'j'):
        ser.write(b'8')
    if ( key == 'k'):
        ser.write(b'9')
    if ( key == 'space'):
        ser.write(b'0')
    if ( key == '`'):
        ser.write(b'0')
        ser.close()
        exit()
    
    keyout = key
    print(f"'{key}' is pressed")

def release(key):
    print(f"'{key}' released")
    ser.write(b'0')

listen_keyboard(on_press=press, on_release=release)

while (1):
    print(keyout)
