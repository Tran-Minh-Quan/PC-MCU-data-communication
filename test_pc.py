import serial
from time import sleep as wait
from time import time as this_time
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
    return crc.to_bytes(1, 'big')


ser = serial.Serial('COM19', baudrate=1000000, bytesize=serial.EIGHTBITS)
receive = None
while receive != '06':
    receive = ser.read(1).hex()

len_wire = 0.5
process_time = 0.003
num_send = 0
num_success = 0
num_error = 0
num_crc_error = 0
num_timeout_error = 0

start_time = this_time()

while 1:
    # data = bytearray(input('Input string: '), 'utf-8')
    data = np.random.bytes(randint(250, 251))
    len_data = len(data).to_bytes(1, 'big')
    crc = crc8(databytes=len_data + data)
    transmit = len_data + data + crc
    ser.timeout = 2*((8 * (len(transmit) + 1)) / ser.baudrate + 2*len_wire/3/10**8 + process_time)
    ser.write(transmit)
    num_send += 1

    # print(f'Transmitted data: {transmit}')
    print(f'Number of send data: {num_send}')

    receive = ser.read(1).hex()
    # print(f'Received data: {receive}, status: {receive == "06"}')

    while receive != '06':
        num_error += 1
        if receive == '30':
            num_crc_error += 1
        elif receive == '31':
            num_timeout_error += 1
        ser.write(transmit)
        num_send += 1
        # print(f'Transmitted data: {transmit}')
        print(f'Number of send data: {num_send}')
        receive = ser.read(1).hex()
        # print(f'Received data: {receive}, status: {receive == "06"}')

    num_success += 1
    print(f'Speed: {(len(transmit) * 8)/(this_time() - start_time):.2f}bps')
    start_time = this_time()
    percent_error = num_error * 100 // num_send
    # print(f'Number of crc error: {num_crc_error}')
    # print(f'Number of timeout error: {num_timeout_error}')
    # print(f'Number of error data: {num_error}')
    # print(f'Percent_error: {percent_error}%')
