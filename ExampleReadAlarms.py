import OMLibrary as OM
import time
import pandas as pd
#Using Library
# OM.ReadAlarms('USBtoUART','01') #Mac
# OM.ReadAlarms('usbserial','01') #Mac
COMPort='COM13'
OM.ReadAlarms(COMPort,'01') #Win

#Original Read Alarms
address='01'
fcode='03'
uregaddr='00'
legaddr='80'
unreg='00'
lnreg='02'

# [ser, ports] = OM.initSerial('USBtoUART')
# ser = OM.initSerial('usbserial')
[ser, ports] = OM.initSerial(COMPort) #Win
i=0
while True:
    start_time = time.time()
    [result, ser] = OM.ReadReg(ser, address, fcode, uregaddr, legaddr, unreg, lnreg, 20, 0.007)
    errorlist = pd.read_csv('OMErrorLookUp.txt')
    result = result.hex()
    e = errorlist[errorlist['Code'].str.contains(str(result[12:14]))]
    print(e)
    print("--- Program took %s seconds ---" % (time.time() - start_time))
    i=i+1
    if i >=2:
        break
ser.close()  # close port
