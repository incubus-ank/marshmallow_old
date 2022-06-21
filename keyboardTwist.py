import keyboard
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)
print(ser.name) 

keyboard.add_hotkey("w", lambda: ser.write(b'1'))
keyboard.add_hotkey("d", lambda: ser.write(b'4'))
keyboard.add_hotkey("s", lambda: ser.write(b'3'))
keyboard.add_hotkey("a", lambda: ser.write(b'2'))
keyboard.add_hotkey("q", lambda: ser.write(b'5'))
keyboard.add_hotkey("e", lambda: ser.write(b'6'))
keyboard.add_hotkey("space", lambda: ser.write(b'0'))

while True:
    keyboard.wait("`")
    ser.write(b'0')
    ser.close()
    exit()