import OMLibrary as OM
import time
start_time = time.time()

#Read Feedback Commands
postype=input("What value to monitor?")
address='01'
fcode='03'
uregaddr='00'
legaddr=postype #CC for Feedback Position, C6 for Command Position, C8 for speed, CE for feedback speed
unreg='00'
lnreg='02'
[ser, ports] = OM.initSerial('USBtoUART')
[result, ser] = OM.ReadReg(ser, address, fcode, uregaddr, legaddr, unreg, lnreg, 20, 0.007)
out = result.hex()
outnew = out[6:14]
print("Monitor: " + str(postype) + ":" + str(int(outnew, 16)))
ser.close()
print("--- Program took %s seconds ---" % (time.time() - start_time))