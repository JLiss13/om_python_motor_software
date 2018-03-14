import OMLibrary as OM
import time
start_time = time.time()

ser = OM.initSerial('USBtoUART')
wt=0.007
addval='01'
#Set Position Example
address=addval
fcode='10'
uregaddr='04' #if relative 10, if absolute 04
legaddr='00' #if relative 48, if absolute 00
unumreg='00'
lnumreg='02'
numbytes='04'
unreg='0000'
lnreg='000F' #5000steps
if ser.isOpen():
    print('Open: ' + ser.portstr)
else:
    print("Was closed, now opening")
    ser.open()
# Write to register to do actuation, change alarm settings, etc.
# address of the device
# '030300800002C401' original checksum
hexval = address + fcode + uregaddr + legaddr + unumreg + lnumreg + numbytes + unreg + lnreg  # Check Pg 145 in AR series book
hexval = OM.crc16(hexval)
# ser.write(b"0310040000020400000FFF8f67")
ser.write(bytearray.fromhex(hexval))
time.sleep(wt)
# ser.flushInput()
# ser.flushOutput()
# ser.flush()
ser.close()  # close port

print("--- Program took %s seconds ---" % (time.time() - start_time))