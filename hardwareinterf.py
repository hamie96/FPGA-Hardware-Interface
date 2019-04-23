from serial import * 
from bitarray import bitarray 


serialPort = Serial("/dev/ttyUSB1", baudrate = 115200, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE,timeout=0.1)

def sendHashString(prehash):
    #CONVERT TO BIT ARRAY WITH UTF-8 ENCODING
    prehash = bitarray()
    prehash.frombytes(preHashstr.encode('utf-8'))

    #BEGIN NONCE IDENTIFICATION ALGORITHM
    L = len(prehash) #store L
    Q = L + 64 + 1 # store Q
    prehash.append(True) #add 1 True Bit
    for k in range(512): #find a k such that Q + k is the lowest multiple of 512
        y = Q + k
        if y % 512  == 0:
            prehash.extend([False] * k) #Add k number of 0 bits when found
            break
    #CREATE 64 BIT BIG ENDIAN OF L
    bigEndianBit = bitarray('{0:b}'.format(L),endian ='big')
    for x in range(64 - len(bigEndianBit)):
        bigEndianBit.append(False)
    #ADD ENDIAN BIT TO BIT ARRAY
    prehash.extend(bigEndianBit)

    #CONVERT BIT ARRAY TO RAW BYTES
    z = prehash.tobytes()

    #SEND RAW BYTES TO FPGA
    serialPort.write(z)



    #READ FROM FPGA
    result = serialPort.readline()

    #DECODE BYTES TO STRING
    Hashstr = result.decode("utf-8", 'ignore')
    #REMOVE NULL CHARS
    Hashstr = Hashstr.replace('\0', '')

    #COMPARE STRINGS
    print(preHashstr)
    print(Hashstr)
    return Hashstr



