import math
import hashlib
plantext="hello world"
key="alloo123asjdfjdsdddaflr"
def TransTextToBin(text):
    tempbin=""
    for i in text:
        char=bin(ord(i)).replace("0b",'')
        char=char.zfill(8)
        tempbin+=char
    return tempbin
def TransBinToText(bins):
    while len(bins)<8:
        bins='0'+bins
    round=int(len(bins)/8)
    temptext=""
    for i in range(0,round):
        decimal=0
        index=0
        bin=int(bins[i*8:(i+1)*8])
        while bin!=0:
            dec = bin % 10
            decimal = decimal + dec * pow(2, index)
            bin = bin//10
            index += 1
        temptext+=chr(decimal)
    return temptext
def TransBinToDec(bin):
    decimal, index, n = 0, 0, 0
    while bin != 0:
        dec = bin % 10
        decimal = decimal + dec * pow(2, index)
        bin = bin//10
        index += 1
    return decimal
def TransDecToBin(dec):
    result = bin(int(dec)).replace("0b", "")
    while len(result)<4:
        result='0'+result
    return result
def DoPermutation(input,table,out_bitnumber):
    result=""
    with open(table+".txt",'r') as _table:
        ipcontent=_table.read().split(",")
    for i in range(0,out_bitnumber):
        result+=input[int(ipcontent[i])-1]
    return result
def Key_DoPermutation(input,table,out_bitnumber):
    input=Key_SplitToN(input,len(input))
    result=""
    with open(table+".txt",'r') as _table:
        ipcontent=_table.read().split(",")
    for i in range(0,out_bitnumber):
        result+=input[int(ipcontent[i])-1]
    return result
def Split(input):
    lenofblock=int(len(input)/2)
    leftblock=input[:lenofblock]
    rightblock=input[lenofblock:]
    return leftblock,rightblock
def Merge(input_1,input_2):
    return input_1+input_2
def Swap32(input):
    leftblock,rightblock=Split(input)
    leftblock,rightblock=rightblock,leftblock
    return leftblock+rightblock
def SplitToN(input,number,lenofblock=0):
    if lenofblock==0:
        lenofblock=int(len(input)/number)
    result=list()
    for i in range(0,number):
        index=i*lenofblock+0
        count=0
        block=""
        while count<lenofblock:
            if(index>=len(input)): 
                break
            block+=input[index]
            index+=1
            count+=1
        block=block.zfill(lenofblock)
        result.append(block)
    return result
def HashTo64bit(string):
    if len(string)>64:
        value = hashlib.md5(string.encode())
        value = value.hexdigest()
        value = bin(int(value, 16)).replace("0b","")
        value = value[:64]
        value=value.zfill(64)
    else: value=string.zfill(64)
    return value
def Key_SplitToN(input,number):
    result=list()
    lenofblock=int(len(input)/number)
    for i in range(0,number):
        index=i*lenofblock+0
        count=0
        block=""
        while count<lenofblock:
            block+=input[index]
            index+=1
            count+=1
        result.append(block)
    return result
def CreateSbox1_8(filesbox):
    sbox1_8=list()
    for i in range(0,8):
        tempbox=list()
        for j in range(0,4):
            row=filesbox.readline().replace("\n",'').split(",")
            tempbox.append(row)
        sbox1_8.append(tempbox)
    return sbox1_8
def Substitution(input,table):
    sbox1_8=list()
    with open(table+".txt",'r') as sbox:
        sbox1_8=CreateSbox1_8(sbox)
    Arr_Sboxes=SplitToN(input,8,6)
    for i in range(0,8):
        row=Arr_Sboxes[i][0]+Arr_Sboxes[i][5]
        row=TransBinToDec(int(row))
        col=Arr_Sboxes[i][1:5]
        col=TransBinToDec(int(col))
        Arr_Sboxes[i]=TransDecToBin(sbox1_8[i][row][col])
    result=''
    for i in Arr_Sboxes:
        result+=i
    return result
def DoXOR(input_1,input_2,out_len):
    result=int(input_1,2) ^ int(input_2,2)
    return bin(result).replace("0b","").zfill(out_len)
def ShiftLeft(input,num_shift):
    number=len(input)
    result=""
    input=Key_SplitToN(input,len(input))
    first=0
    for i in range(0,num_shift):
        temp=input[first]
        for j in range(1,len(input)):
            input[j-1]=input[j]
        end=len(input)-1
        input[end]=temp
    for i in input:
        result+=i
    return result
def KeyGenaration(key):
    key=TransTextToBin(key)
    key=HashTo64bit(key)
    keys=list()
    key=Key_DoPermutation(key,"paritydrop_table",56)
    leftkey,rightkey=Split(key)
    rounds=16
    for i in range(0,rounds):
        if i==0 or i==1 or i==8 or i==15:
            number=1
        else: number=2
        leftkey=ShiftLeft(leftkey,number)
        rightkey=ShiftLeft(rightkey,number)
        key=Merge(leftkey,rightkey)
        key=Key_DoPermutation(key,"key_compresstion_table",48)
        keys.append(key)
    return keys
def DESFuntion(input,key):
    input=DoPermutation(input,"etable",48)
    input=DoXOR(input,key,48)  
    input=Substitution(input,"sbox")
    input=DoPermutation(input,"ptable",32)
    return input
def DoRoundMix(leftblock,rightblock,key):
    next_leftblock=rightblock
    rightblock=DESFuntion(rightblock,key)
    next_rightblock=DoXOR(leftblock,rightblock,32)
    return next_leftblock,next_rightblock
def DES_Encryption(plantext,key):
    temp=""
    plantext=TransTextToBin(plantext)
    number=len(plantext)/64
    number=math.ceil(number)
    plantext=SplitToN(plantext,number,64)
    for i in plantext:
        rounds=16
        keys=KeyGenaration(key)
        i=DoPermutation(i,"iptable",64)
        leftblock,rightblock=Split(i)
        for round in range(0,rounds):
            leftblock,rightblock=DoRoundMix(leftblock,rightblock,keys[round])
        i=Merge(leftblock,rightblock)
        i=Swap32(i)
        i=DoPermutation(i,"fptable",64)
        temp+=i
    plantext=temp
    plantext=TransBinToText(plantext)
    return plantext
def DES_Decryption(plantext,key):
    temp=""
    plantext=TransTextToBin(plantext)
    number=len(plantext)/64
    number=math.ceil(number)
    plantext=SplitToN(plantext,number,64)
    for i in plantext:
        rounds=15
        keys=KeyGenaration(key)
        i=DoPermutation(i,"iptable",64)
        leftblock,rightblock=Split(i)
        for round in range(rounds,-1,-1):
            leftblock,rightblock=DoRoundMix(leftblock,rightblock,keys[round])
        i=Merge(leftblock,rightblock)
        i=Swap32(i)
        i=DoPermutation(i,"fptable",64)
        temp+=i
    plantext=temp
    plantext=TransBinToText(plantext)
    return plantext
print(plantext)
plantext=DES_Encryption(plantext,key)
print(plantext)
plantext=DES_Decryption(plantext,key)
print(plantext)