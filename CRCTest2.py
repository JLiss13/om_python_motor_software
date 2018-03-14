import crc16_2 as c
address='03'
fcode='03'
uregaddr='00'
legaddr='80'
unreg='00'
lnreg='02'
hexval=address+fcode+uregaddr+legaddr+unreg+lnreg
crcsuffix =c.crc16(hexval)
suffix=crcsuffix[2:5]+crcsuffix[6]
print(suffix)
hexval=hexval+suffix
print(hexval)