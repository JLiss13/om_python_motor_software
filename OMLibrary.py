import sys
import glob
import crc16_2 as c
import serial
import time
import pandas as pd
def serial_ports(uid):
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system that are usbserial
    """
    if sys.platform.startswith('win'): #Windows device
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'): #Linux device
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'): #Mac device
        ports = glob.glob('/dev/cu*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        if str(uid) in port:
            result.append(port)
    return result, ports
def initSerial(uid):
    #Open Serial Port with non-blocking handshake
    devtitle, ports = serial_ports(str(uid))
    print(devtitle)
    ser = serial.Serial(str(devtitle[0]), 115200, timeout=0.003,parity=serial.PARITY_EVEN)  #timeout for 3ms
    return ser, ports
def crc16(hexval):
    crcsuffix = c.crc16(hexval)
    print(crcsuffix)
    if len(crcsuffix) == 8:
        suffix = crcsuffix.replace('0x', '')
        hexval = hexval + suffix
    elif len(crcsuffix) == 7:
        suffix = crcsuffix.replace('x','')
        hexval = hexval + suffix[1:len(suffix)]
    elif len(crcsuffix) == 6:
        suffix = crcsuffix.replace('x', '')
        hexval = hexval + suffix
    else:
        print('There is a CRC16 error')
        sys.exit('There is a CRC16 error')
    print(suffix)
    print(hexval)
    return str(hexval)
def ReadReg(ser,address,fcode,uregaddr,legaddr,unreg,lnreg,bytes2read,wt):
    if ser.isOpen():
        print('Open: ' + ser.portstr)
    else:
        print("Was closed, now opening")
        ser.open()
    hexval=address+fcode+uregaddr+legaddr+unreg+lnreg #Check Pg 144 in AR series book
    hexval = crc16(hexval)
    ser.write(bytearray.fromhex(hexval))
    time.sleep(wt)
    out = ser.read(bytes2read)
    print('Output: ' +str(out))
    return [out, ser]
def WriteMultiReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,unreg,lnreg,wt):
    if ser.isOpen():
        print('Open: ' + ser.portstr)
    else:
        print("Was closed, now opening")
        ser.open()
    hexval=address+fcode+uregaddr+legaddr+unumreg+lnumreg+numbytes+unreg+lnreg #Check Pg 145 in AR series book
    hexval = crc16(hexval)
    ser.write(bytearray.fromhex(hexval))
    time.sleep(wt)
    return hexval
def DDWriteReg(ser,address,fcode,uregaddr,legaddr,unumreg,lnumreg,numbytes,opernum,opertype,posreg,velreg,accelreg,deccelreg,currreg,trigger,wt):
    if ser.isOpen():
        print('Open: ' + ser.portstr)
    else:
        print("Was closed, now opening")
        ser.open()
    hexval = address + fcode + uregaddr + legaddr + unumreg + lnumreg + numbytes + \
             opernum + opertype + posreg + velreg + accelreg + deccelreg + currreg + trigger  # Check pg 276 in AZ series book
    hexval = crc16(hexval)
    ser.write(bytearray.fromhex(hexval))
    time.sleep(wt)
    return hexval
def ReadMonitorCommands(ser,address,postype,numofbytes):
    fcode = '03'
    uregaddr = '00'
    legaddr = postype  # C6 for Command Position, C8 for speed, CC for Feedback Position, CE for feedback speed
    unreg = '00'
    lnreg = numofbytes
    [result,ser]=ReadReg(ser,address,fcode,uregaddr,legaddr,unreg,lnreg,20,0.007)
    out = result.hex()
    outnew = out[6:14]
    print("Monitor: "+str(postype)+":"+str(int(outnew, 16)))
    return out, ser
def ReadAlarms(uid,address):
    fcode = '03'
    uregaddr = '00'
    legaddr = '80'
    unreg = '00'
    lnreg = '02'
    [ser, ports] = initSerial(uid)
    [result, ser] = ReadReg(ser, address, fcode, uregaddr, legaddr, unreg, lnreg, 20, 0.005)
    errorlist = pd.read_csv('OMErrorLookUp.txt')
    result=result.hex()
    e = errorlist[errorlist['Code'].str.contains(str(result[12:14]))]
    print(e)
    return [result, ser, e]
def ReadAlarmsLabview(address):
    uid='COM13'
    fcode = '03'
    uregaddr = '00'
    legaddr = '80'
    unreg = '00'
    lnreg = '02'
    [ser, ports] = initSerial(uid)
    [result, ser] = ReadReg(ser, str(address), fcode, uregaddr, legaddr, unreg, lnreg, 20, 0.005)
    errorlist = pd.read_csv('OMErrorLookUp.txt')
    result=result.hex()
    e = errorlist[errorlist['Code'].str.contains(str(result[12:14]))]
    print(e)
    return result
def ResetAlarm(uid,address, input):
    fcode = '06'
    uregaddr = '01'
    legaddr = str(input)
    unumreg = '00'
    lnumreg = '01'
    numbytes = ''
    unreg = ''
    lnreg = ''
    [ser,port] = initSerial(uid)
    hexval = WriteMultiReg(ser, address, fcode, uregaddr, legaddr, unumreg, lnumreg, numbytes, unreg, lnreg, 0.05)
    return hexval, ser