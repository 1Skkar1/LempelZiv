import sys
import os
import math
from bitstring import Bits

args = sys.argv[1:]
argc = len(args)
input_file = ''
output_file = ''
L = {'':0}
L_index = 1
output = ''

# MAIN FUNCTION
def main():
    global input_file, output_file, output

    getFiles()
    file = open(input_file, 'rb')
    data = Bits(file)
    file.close()
    compress(data)
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
                input_file = args[0]

        if args[1]:
                if args[1].endswith('.lz'):
                    output_file = args[1]
                else:
                    sys.exit('Invalid output file format. Please use a .lz file!')
    else:
        sys.exit("Please provide an input and an output file! \nUsage: 'python3 compress.py inputfilename.[txt|bin] outputfilename.lz'")

# LEMPEL-ZIV COMPRESSION ALGORITHM
def compress(input):
    global L, L_index, output

    i = 1
    length = len(input.bin)

    while i <= length:
        seq = input[i-1:i].bin
        if seq in L:
            j = i + 1

            while j <= length:
                seq = input[i-1:j-1].bin
                if seq not in L:
                    break

                j += 1
            
            seq = input[i-1:j-1].bin
            addToOutput(seq)    
            i += (j - 1)

        else:
            if len(L) == 1:
                output += seq

            else:
                bitL = math.ceil(math.log2(len(L)))
                output += getC(0, bitL) + seq
            
            L[seq] = L_index
            L_index += 1
            i += 1

def addToOutput(seq):
    global L, L_index, output

    if seq in L:
        index = L.get(seq)
        bitL = math.ceil(math.log2(len(L)))
        output += getC(index, bitL)
    
    else:
        y = seq[0:len(seq) - 1]
        b = seq[len(seq) - 1]
        index = L.get(y)
        bitL = math.ceil(math.log2(len(L)))
        output += getC(index, bitL) + str(b)
        L[seq] = L_index
        L_index += 1

def getC(index, length):
    c = bin(int(index)).replace("0b", "")
    while len(c) < length:
        c = "0" + c
    return c

# WRITE RESULT TO .LZ FILE 
def writeFile():
    global output_file, output

    file = open(output_file, 'wb')
    bit = Bits(bin = output).tobytes()
    file.write(bit)
    file.close()


main()