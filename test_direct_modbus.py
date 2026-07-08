#!/usr/bin/env python3
from pymodbus.client import ModbusSerialClient
import logging

# communicate with the Autoslide door opener using a locally connected
# RS485-to-serial converter

# opener's dipswitch #6 should be in the off position to use its modbus port

devnum = 1 # default slave addr

def run():
    client = ModbusSerialClient(
        port='/dev/cu.usbserial-10',
        baudrate=9600, #96000 also worked
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=5, # seconds
        framer='rtu'
    )
    client.connect()

    # read door opener's position & locking status
    rr = client.read_holding_registers(slave=devnum, address=0x4, count=1)
    if rr.isError():
        logging.error("ERROR: pymodbus returned an error!")
    else:
        if rr.registers[0] == 0:
            print("Door's closed & unlocked!")
        elif rr.registers[0] == 1:
            print("Door's closed & locked!")
        elif rr.registers[0] == 2:
            print("Door's open!")

    # read door opener's position & locking status
    rr = client.read_holding_registers(slave=devnum, address=0x2, count=1)
    if rr.isError():
        logging.error("ERROR: pymodbus returned an error!")
    else:
        if rr.registers[0] == 0:
            print("Auto mode")
        elif rr.registers[0] == 1:
            print("Stacker mode")
        elif rr.registers[0] == 2:
            print("Security mode")
        elif rr.registers[0] == 3:
            print("Pet mode")

    client.close()

if __name__ == "__main__":
    run()
