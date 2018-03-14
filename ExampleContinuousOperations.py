import OMLibrary as OM
import time
import random
import sys
def randhex():
    return str(random.choice("0123456789ABCDEF")) + str(random.choice("0123456789ABCDEF"))
print("COMPORT Selection: ", str(sys.argv[1]),"\n")
[ser, ports] = OM.initSerial(str(sys.argv[1]))
# [ser, ports] = OM.initSerial('COM13')
# ser = OM.initSerial('usbserial')
wt=0.07
addval='01'
#Set Position Example
address=addval
fcode='10'
uregaddr='00'
legaddr='58'
unumreg='00'
lnumreg='10'
numbytes='20'
opernum='00000000'
opertype='00000022' #Operation type see page 277 in AZ series book
posreg='00FFFF34'
velreg='00000FFE'
accelreg='000ACA00' #max accel is '009ACA00'
deccelreg='000ACA00' #max deccel is '009ACA00'
currreg='000000FA' # 25% current 
trigger='00000001'
if ser.isOpen():
    print('Open: ' + ser.portstr)
else:
    print("Was closed, now opening")
    ser.open()
# Write to register to do actuation, change alarm settings, etc.
# address of the device
# '030300800002C401' original checksum
# ser.write(b"0310040000020400000FFF8f67")
i=1
try:
    while True:
        start_time = time.time()
        hexval = address + fcode + uregaddr + legaddr + unumreg + lnumreg + numbytes + \
                 opernum + opertype + posreg + velreg + accelreg + deccelreg + currreg + trigger  # Check pg 276 in AZ series book
        hexval = OM.crc16(hexval)
        ser.write(bytearray.fromhex(hexval))
        print("To step position: " + str(int(posreg, 16)))
        time.sleep(wt)
        [out,ser]=OM.ReadMonitorCommands(ser,address, 'CE','02')
        print("--- Program took %s seconds ---" % (time.time() - start_time))
        i=i+1
        if i >=100:
            break
        b = randhex()+randhex() #Randomly change the position to simulate command position changes
        posreg=posreg[0:4]+b
except KeyboardInterrupt:
    velreg='00000000'
    hexval = address + fcode + uregaddr + legaddr + unumreg + lnumreg + numbytes + \
         opernum + opertype + posreg + velreg + accelreg + deccelreg + currreg + trigger  # Check pg 276 in AZ series book
    hexval = OM.crc16(hexval)
    ser.write(bytearray.fromhex(hexval))
    print("To step position: " + str(int(posreg, 16)))
    raise
# ser.flushInput()
# ser.flushOutput()
# ser.flush()
ser.close()  # close port

