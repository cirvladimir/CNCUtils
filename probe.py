import serial
import time
import re

serialPort = serial.Serial(
    port="COM9", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)

def readLine():
    return serialPort.readline().decode("Ascii").strip()
    # serialString = ""  # Used to hold data coming over UART
    # while True:
    #     # Wait until there is data waiting in the serial buffer
    #     if serialPort.in_waiting > 0:

    #         # Read data out of the buffer until a carraige return / new line is found
    #         serialString = serialPort.readline()

    #         # Print the contents of the serial data
    #         try:
    #             return serialString.decode("Ascii").strip()
    #         except:
    #             pass


def readAll():
    tot = ""
    l = ""
    while l != "ok":
        tot = tot + "\n" + l
        l = readLine()
    return tot.strip()

def initCon():
    while True:
        l = readLine()
        print(l)
        if l == "Grbl 1.1f ['$' for help]":
            return

def writeLine(ln):
    serialPort.write((ln + "\n").encode())

def sendCommand(com):
    writeLine(com)
    readAll()
    # print(com)

def getState():
    writeLine("?")
    return readAll()

def getPosition():
    # MPos:5.000,0.000,0.000
    return getState().split("|")[1].split(":")[1]

def waitForIdle():
    while True:
        time.sleep(0.050)
        if getState()[1:5] == "Idle":
            return

def probe():
    sendCommand("G38.2 F20 Z-30")
    waitForIdle()

def scanRoutine(x, w, y, h, num_x = 15, num_y = 10):
    sendCommand("G0 Z1")
    sendCommand("G90")
    for x_i in range(0, num_x):
        print('[')
        for y_i in range(0, num_y):
            cur_x = x + w / (num_x - 1) * x_i
            cur_y = y + h / (num_y - 1) * y_i
            sendCommand(f'X{cur_x:.3f} Y{cur_y:.3f}')
            waitForIdle()
            probe()
            print(f'[{getPosition()}],')
            sendCommand("G0 Z1")
            waitForIdle()
            sendCommand("G90")
        print(']')
    sendCommand(f'X0 Y0')

def moveRoutine():
    sendCommand("G91")
    print("moving: wasd rf (q). a - .1mm aa - 1mm. aaa - 10mm, aaaa - 100mm")
    while True:
        com = input(">").lower().strip()
        if com == 'q':
            return
        dist = ['0.1', '1', '10', '100'][len(com) - 1]
        direction = com[0]
        if direction == 'a':
            gcode = "X-" + dist
        elif direction == 'd':
            gcode = "X" + dist
        elif direction == 'w':
            gcode = "Y" + dist
        elif direction == 's':
            gcode = "Y-" + dist
        elif direction == 'r':
            gcode = "Z" + dist
        elif direction == 'f':
            gcode = "Z-" + dist
        else:
            print("Invalid command")
            continue
        
        print(gcode)
        sendCommand(gcode)
        waitForIdle()

initCon()

sendCommand("G21")

# moveRoutine()

scanRoutine(2, 90, 2, 59)
# sendCommand("G38.2 F30 Z-30")

# sendCommand("F10 X-20")


# # sendCommand("X20")
# print("get ok")

# # time.sleep(3)
# waitForIdle()
# print("Is idle")

# writeLine("?")
# print(readAll())


# while True:
#     print(readLine())
# serialString = ""  # Used to hold data coming over UART
# while 1:
#     # Wait until there is data waiting in the serial buffer
#     if serialPort.in_waiting > 0:

#         # Read data out of the buffer until a carraige return / new line is found
#         serialString = serialPort.readline()

#         # Print the contents of the serial data
#         try:
#             print(serialString.decode("Ascii"))
#         except:
#             pass