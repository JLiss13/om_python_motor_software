def crc16(data, bits=8):
    crc = 0xFFFF
    for op, code in zip(data[0::2], data[1::2]):
        crc = crc ^ int(op+code, 16)
        for bit in range(0, bits):
            if (crc&0x0001)  == 0x0001:
                crc = ((crc >> 1) ^ 0xA001)
            else:
                crc = crc >> 1
    return typecasting(crc)

def typecasting(crc):
    msb = hex(crc >> 8)
    lsb = hex(crc & 0x00FF)
    return lsb + msb