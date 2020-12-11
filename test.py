import serial
from time import sleep as wait

ser = serial.Serial('COM3', baudrate=115200, bytesize=serial.SEVENBITS, timeout=0.5, parity=serial.PARITY_EVEN)
i = 0
# test = (str(i) + ' ').encode('utf-8')
# print(type(test))
while 1:
    # i += 1
    # ser.write((str(i) + ' ').encode('utf-8'))
    # wait(0.00000001)
    data = ser.read().hex()
    print(data)
