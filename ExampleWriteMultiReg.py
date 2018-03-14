import OMLibrary as OM
import time
start_time = time.time()

ser = OM.initSerial('USBtoUART')
wt=0.007
addval='03'
#Set Operation Mode
print('Set position')
address=addval
fcode='10'
uregaddr='05'
legaddr='00'
unumreg='00'
lnumreg='02'
numbytes='04'
unreg='0000'
lnreg='0001' # 0 Incremental and 1 for Absolute
OM.WriteMultiReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,unreg,lnreg,wt)

time.sleep(wt)

#Set Position Register Value
print('Set position')
address=addval
fcode='10'
uregaddr='04' #if relative 10, if absolute 04
legaddr='00' #if relative 48, if absolute 00
unumreg='00'
lnumreg='02'
numbytes='04'
unreg='0000'
lnreg='FFFF' #5000steps
OM.WriteMultiReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,unreg,lnreg,wt)

#Set Velocity Register Value
print('Set Velocity')
address=addval
fcode='10'
uregaddr='04' #04 for absolute and 02 for relative
legaddr='80' # 80 for absolute and 86 for relative
unumreg='00'
lnumreg='02'
numbytes='04'
unreg='0000'
lnreg='0E10' #255 steps per second
OM.WriteMultiReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,unreg,lnreg,wt)

#Set Acceleration Register Value
print('Set Acceleration')
address=addval
fcode='10'
uregaddr='06'
legaddr='00'
unumreg='00'
lnumreg='02'
numbytes='04'
unreg='0000'
lnreg='2328' #255 steps per second^2
OM.WriteMultiReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,unreg,lnreg,wt)


#Set Decceleration Register Value
print('Set Decceleration')
address=addval
fcode='10'
uregaddr='06'
legaddr='80'
unumreg='00'
lnumreg='02'
numbytes='04'
unreg='0000'
lnreg='0000' #255 steps per second^2
OM.WriteMultiReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,unreg,lnreg,wt)


#Start Motor
print('Turn On Motors')
address=addval
fcode='10'
uregaddr='00'
legaddr='7C'
unumreg='00'
lnumreg='02'
numbytes='04'
unreg='0000'
lnreg='0008' #0008 for Absolute moves, 1000 for + Jog moves, 2000 for - Jog moves
OM.WriteMultiReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,unreg,lnreg,wt)

print("--- Program took %s seconds ---" % (time.time() - start_time))