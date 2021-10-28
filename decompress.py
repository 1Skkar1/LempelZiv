import sys
import os
import math
from bitstring import Bits

args = sys.argv[1:]
argc = len(args)
input_file = ''
output_file = ''
L = ['']
output = ''

# MAIN FUNCTION
def main():
    global input_file, output_file, output

    getFiles()
    file = open(input_file, 'rb')
    data = Bits(file)
    file.close()
    decompress(data)
    writeFile()
    #print("INPUT:", data)
    #print("OUTPUT:", output)

# CHECK ARGUMENTS OF CALL AND GET FILES
def getFiles():
    global args, argc
    global input_file, output_file

    if argc == 2:
        if args[0]:
            if os.path.exists(args[0]):
                if args[0].endswith('.lz'):
                    input_file = args[0]
                else:
                    sys.exit('Invalid input file format. Please use a .lz file!')

        if args[1]:
            output_file = args[1]
    else:
        sys.exit("Please provide an input and an output file! \nUsage: 'python3 decompress.py inputfilename.lz outputfilename.[txt|bin]'")

# LEMPEL-ZIV DECOMPRESSION ALGORITHM
def decompress(input):
    global L, output

    i = 1
    length = len(input.bin)
    L.append(input[0:1].bin)
    output += input[0:1].bin

    while i < length:
        sizeL = len(L)

        bitL = math.ceil(math.log2(sizeL))
        c = addToOutput(input, bitL, i)

        output += c
        L.append(c)        
        i += bitL + 1
    
    fixEndBits()

# DECOMPRESS SEQ AND ADD TO OUTPUT
def addToOutput(input, bitL, i):
    global L, output

    seq = input[i:i + bitL].bin             # seq read for y
    ypos = int(seq,2)                       # pos of seq for y in L
    y = L[ypos]                             # value in L
    b = input[i + bitL:i + bitL + 1].bin    # seq read for b                 
    return y + b

def fixEndBits():
    global output

    #lbit = data.rindex('1')
    #data = data[0:lbit + 1]
    nBits = len(output) - (len(output) % 4)
    output = output[0:nBits+1]

# WRITE RESULT TO .TXT FILE 
def writeFile():
    global output_file, output

    file = open(output_file, 'wb')
    bit = Bits(bin = output).tobytes()
    file.write(bit)
    file.close()


main()