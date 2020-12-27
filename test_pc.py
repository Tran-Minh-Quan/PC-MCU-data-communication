import serial
from time import sleep as wait
from time import time
import numpy as np
import cv2
from numpy.random import randint

def crc8_1byte(databyte, generator=285):
    generator -= 256
    crc = databyte
    for bit in range(7, -1, -1):
        if crc & 0b10000000:
            crc = crc << 1 & 255 ^ generator
        else:
            crc <<= 1
    return crc


crc8_dict = {databyte: crc8_1byte(databyte=databyte) for databyte in range(256)}


def crc8(databytes):
    crc = 0
    for byte in databytes:
        crc = crc8_dict[byte ^ crc]
    return bytearray([crc])


ser = serial.Serial('COM2', baudrate=921600, bytesize=serial.EIGHTBITS)
len_wire = 0.5
process_time = 0.5
i = 0
wait(3)
receive = ''
num_send = 0
num_success = 0
num_error = 0
num_crc_error = 0
num_timeout_error = 0

while 1:
    if num_success:
        # data = bytearray(input('Input string: '), 'utf-8')
        data = np.random.bytes(randint(5, 6))
    else:
        data = bytearray([1])
    len_data = len(data).to_bytes(1, 'big')
    crc = crc8(databytes=len_data + data)
    transmit = len_data + data + crc
    ser.timeout = 2*((8 * (len(transmit) + 1)) / ser.baudrate + 2*len_wire/3/10**8 + process_time)
    ser.write(transmit)

    receive = ser.read(1).hex()
    num_send += 1
    if num_success:
        # print(f'Transmitted data: {transmit}')
        print(f'Received data: {receive}, status: {receive == "06"}')
        print(f'Number of send data: {num_send}')

    while receive != '06':
        num_error += 1
        if receive == '30':
            num_crc_error += 1
        elif receive == '31':
            num_timeout_error += 1
        ser.write(transmit)
        receive = ser.read(1).hex()
        num_send += 1
        if num_success:
            # print(f'Transmitted data: {transmit}')
            print(f'Received data: {receive}, status: {receive == "06"}')
            print(f'Number of send data: {num_send}')
        # wait(0.002)

    num_success += 1
    percent_error = num_error * 100 // num_send
    # print(f'Number of crc error: {num_crc_error}')
    # print(f'Number of timeout error: {num_timeout_error}')
    # print(f'Number of error data: {num_error}')
    # print(f'Percent_error: {percent_error}%')
    # wait(0.002)
