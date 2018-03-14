import OMLibrary as OM
import time
import serial
start_time = time.time()

#Read Alarms
address='03'
fcode='01'
uregaddr='00'
legaddr='80'
unreg='00'
lnreg='02'
# Open Serial Port with non-blocking handshake
devtitle = OM.serial_ports('USBtoUART')
# [ser, ports] = OM.initSerial('USBtoUART')

# print("--- Program took serial ports %s seconds ---" % (time.time() - start_time))
print(devtitle)
ser = serial.Serial(str(devtitle[0]), 19200, parity=serial.PARITY_EVEN, rtscts=1)  # timeout for 30ms
ser.open()
# Write to register to request for information about a register
# '030300800002C401' original checksum for alarm codes
hexval = address + fcode + uregaddr + legaddr + unreg + lnreg  ##Check Pg 144 in AR series book
hexval = OM.crc16(hexval)
ser.write(bytearray.fromhex(hexval))
out = ser.read(9)
print('Output: ' + str(out))
ser.close()  # close port
print("--- Program took %s seconds ---" % (time.time() - start_time))