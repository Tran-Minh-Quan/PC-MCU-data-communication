import serial
from time import sleep as wait
import numpy as np

ser = serial.Serial('COM3', baudrate=921600, bytesize=serial.EIGHTBITS, timeout=2)
i = 0
buffer = np.random.randint(9, size=10).astype(np.uint8)
wait(2)
while 1:
    received = None
    while received != '06':
        transmitted = bytearray(buffer)
        ser.write(transmitted)
        received = ser.read(1).hex()
        print(f'transmitted data: {transmitted}')
        print(f'received data: {received}')
    buffer = np.random.randint(9, size=10).astype(np.uint8)
