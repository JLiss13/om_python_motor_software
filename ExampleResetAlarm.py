import OMLibrary as OM
import time
#Using original code
start_time = time.time()
input=input("What alarm value do you want to implement?") #Check page 345 in AZ Series book:Maintenance Commands
address='01'
fcode='06'
uregaddr='01'
legaddr=str(input)
unumreg='00'
lnumreg='01'
numbytes=''
unreg=''
lnreg=''
[ser, ports] = OM.initSerial('USBtoUART')
hexval=OM.WriteMultiReg(ser,address, fcode, uregaddr, legaddr, unumreg, lnumreg, numbytes, unreg, lnreg,0.05)
print("--- Program took %s seconds ---" % (time.time() - start_time))

#Using Library function
OM.ResetAlarm('USBtoUART','01','81') #Alarm reset
# OM.ResetAlarm('01','85') #Clear alarm records
# OM.ResetAlarm('01','89') # Clearn communcation error records