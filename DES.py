import math
import hashlib
import sys

def TransTextToBin(text):
    """
    Chuyển đổi Text sang Binary sử dụng bảng ASCII

    Parameters:
    text (string): Text cần chuyển 

    Returns: string tempbin: Chuỗi ở dạng Binary
    """
    tempbin=""
    standard_len=8
    for i in text:
        char=bin(ord(i)).replace("0b",'')
        char=char.zfill(standard_len)
        tempbin+=char
    return tempbin
def TransBinToText(bins):
    """
    Chuyển đổi Binary sang Text sử dụng bảng ASCII

    Parameters:
    bins (string): chuỗi Binary cần chuyển 

    Returns: string temptext: Chuỗi ở dạng Text
    """
    standard_len=8
    while len(bins)<standard_len:
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
    """
    Chuyển đổi Binary sang Decimal 

    Parameters:
    bin (string): chuỗi Binary cần chuyển 

    Returns: int deciaml: Số Decimal
    """
    decimal, index, n = 0, 0, 0
    while bin != 0:
        dec = bin % 10
        decimal = decimal + dec * pow(2, index)
        bin = bin//10
        index += 1
    return decimal
def TransDecToBin(dec):
    """
    Chuyển đổi Decimal sang Binary

    Parameters:
    dec (Any): Decimal cần chuyển 

    Returns: string deciaml: Chuỗi Binary
    """
    standard_len=4
    result = bin(int(dec)).replace("0b", "")
    while len(result)<standard_len:
        result='0'+result
    return result
def DoPermutation(input,table,out_bitnumber):
    """
    Thực hiện hoán vị theo bảng 

    Parameters:
    input (string): chuỗi cần hoán vị
    table (string): tên bảng hoán vị
    out_bitnumber: số bit của chuỗi đã hoán vị

    Returns: result (any): chuỗi sau khi đã hoán vị
    """
    result=""
    with open(table+".txt",'r') as _table:
        ipcontent=_table.read().split(",")
    for i in range(0,out_bitnumber):
        result+=input[int(ipcontent[i])-1]
    return result
def Key_DoPermutation(input,table,out_bitnumber):
    """
    Thực hiện hoán vị theo bảng dành cho khoá(Key)

    Parameters:
    input (string): chuỗi cần hoán vị
    table (string): tên bảng hoán vị
    out_bitnumber: số bit của chuỗi đã hoán vị

    Returns: result (any): chuỗi sau khi đã hoán vị
    """
    input=Key_SplitToN(input,len(input))
    result=""
    with open(table+".txt",'r') as _table:
        ipcontent=_table.read().split(",")
    for i in range(0,out_bitnumber):
        result+=input[int(ipcontent[i])-1]
    return result
def Split(input):
    """
    Chặt đôi chuỗi đầu vào 

    Parameters:
    input (string): chuỗi cần chặt đôi

    Returns: 2 chuỗi chặt ra từ chuỗi ban đầu
    """
    lenofblock=int(len(input)/2)
    leftblock=input[:lenofblock]
    rightblock=input[lenofblock:]
    return leftblock,rightblock
def Merge(input_1,input_2):
    """
    Hợp nhất 2 chuỗi

    Parameters:
    input_1 (string): chuỗi đầu tiên
    input_2 (string): chuỗi thứ hai

    Returns: string : chuỗi hợp nhất
    """
    return input_1+input_2
def Swap32(input):
    """
    Hoán đổi giá trị 2 nửa của chuỗi

    Parameters:
    input (string): chuỗi đầu vào

    Returns: string: chuỗi đã hoán đổi giá trị
    """
    leftblock,rightblock=Split(input)
    leftblock,rightblock=rightblock,leftblock
    return leftblock+rightblock
def SplitToN(input,number,lenofblock=0):
    """
    Chặt chuỗi thành N chuỗi

    Parameters:
    input (string): chuỗi cần chặt
    number (int): số chuỗi cần chặt ra
    lenofblock (int): độ dài của mỗi chuỗi khi chặt

    Returns: result (list): N chuỗi đã chặt
    """
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
def Key_SplitToN(input,number):
    """
    Chặt chuỗi thành N chuỗi dành cho khoá(Key)

    Parameters:
    input (string): chuỗi cần chặt
    number (int): số chuỗi cần chặt ra

    Returns: result (list): N chuỗi đã chặt
    """
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
def HashTo64bit(input):
    """
    Băm chuỗi chuỗi đầu vào thành chuỗi có độ dài 64 bit

    Parameters:
    input (string): chuỗi đầu vào

    Returns: string: chuỗi đã băm
    """
    len_hash=64
    if len(input)>len_hash:
        value = hashlib.md5(input.encode())
        value = value.hexdigest()
        basehex=16
        value = bin(int(value, basehex)).replace("0b","")
        value = value[:len_hash]
        value=value.zfill(len_hash)
    else: value=input.zfill(len_hash)
    return value
def CreateSbox1_8(filesbox):
    """
    Tạo Sbox từ 1 tới 8

    Parameters:
    filesbox (string): tên file chứa dữ liệu của 8 Sbox

    Returns: sbox1_8 (list): 8 sbox
    """
    row_num_each_sbox=4
    sbox_num=8
    sbox1_8=list()
    for i in range(0,sbox_num):
        tempbox=list()
        for j in range(0,row_num_each_sbox):
            row=filesbox.readline().replace("\n",'').split(",")
            tempbox.append(row)
        sbox1_8.append(tempbox)
    return sbox1_8
def Substitution(input,table):
    """
    Thực hiện thay thế các vị trị của chuỗi đầu vào

    Parameters:
    input (string): chuỗi cần thay thế
    table (string): tên bảng thay thế

    Returns: result (string): Chuỗi đã thay thế
    """
    sbox_num=8
    bit_len_block=6
    sbox1_8=list()
    row_index_start=0
    row_index_end=col_index_end=5
    col_index_start=1
    with open(table+".txt",'r') as sbox:
        sbox1_8=CreateSbox1_8(sbox)
    Arr_Sboxes=SplitToN(input,sbox_num,bit_len_block)
    for i in range(0,sbox_num):
        row=Arr_Sboxes[i][row_index_start]+Arr_Sboxes[i][row_index_end]
        row=TransBinToDec(int(row))
        col=Arr_Sboxes[i][col_index_start:col_index_end]
        col=TransBinToDec(int(col))
        Arr_Sboxes[i]=TransDecToBin(sbox1_8[i][row][col])
    result=''
    for i in Arr_Sboxes:
        result+=i
    return result
def DoXOR(input_1,input_2,out_len):
    """
    Thực hiện phép XOR giữa 2 chuỗi

    Parameters:
    input_1 (string): chuỗi thứ nhất
    input_2 (string): chuỗi thứ hai
    out_len (string): độ dài bit của kết quả

    Returns:  Chuỗi Binary kết quả sau khi XOR
    """
    base_binary=2
    result=int(input_1,base_binary) ^ int(input_2,base_binary)
    return bin(result).replace("0b","").zfill(out_len)
def ShiftLeft(input,num_shift):
    """
    Thực hiện dịch trái chuỗi đầu vào

    Parameters:
    input (string): chuỗi cần dịch trái
    num_shift (int): số bit muốn dịch trái

    Returns: result (string): Chuỗi dịch trái
    """
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
    """
    Thực hiện sinh 16 khoá(Key) cho 16 Round từ khoá đầu vào

    Parameters:
    key (string): khoá đầu vào (64 bit)

    Returns: keys (list): bộ 16 khoá cho 16 Round(48 bit)
    """
    key=TransTextToBin(key)
    key=HashTo64bit(key)
    keys=list()
    key=Key_DoPermutation(key,"paritydrop_table",56)
    leftkey,rightkey=Split(key)
    rounds=16
    one_shift_round=[0,1,8,15]
    for i in range(0,rounds):
        if i in one_shift_round:
            number=1
        else: number=2
        leftkey=ShiftLeft(leftkey,number)
        rightkey=ShiftLeft(rightkey,number)
        key=Merge(leftkey,rightkey)
        key=Key_DoPermutation(key,"key_compresstion_table",48)
        keys.append(key)
    return keys
def DESFuntion(input,key):
    """
    Thực hiện trộn ở khối phải mỗi Round

    Parameters:
    input (string): chuỗi cần trộn
    key (string): khoá của Round

    Returns: input (string): Chuỗi sau khi thực hiện trộn
    """
    input=DoPermutation(input,"etable",48)
    input=DoXOR(input,key,48)  
    input=Substitution(input,"sbox")
    input=DoPermutation(input,"ptable",32)
    return input
def DoRoundMix(leftblock,rightblock,key):
    """
    Thực hiện thao tác ở mỗi Round

    Parameters:
    leftblock (string): Khối bên trái
    rightblock (string): Khối bên phải
    key (string): khoá của Round để đưa vào trộn ở khối phải

    Returns: 2 khối trái và phải sau khi thực hiện thao tác
    """
    next_leftblock=rightblock
    rightblock=DESFuntion(rightblock,key)
    next_rightblock=DoXOR(leftblock,rightblock,32)
    return next_leftblock,next_rightblock
def DES_Encryption(plantext,key):
    """
    Thực hiện mã hoá bằng DES

    Parameters:
    plantext (string): dữ liệu cần mã hoá
    key (string): khoá đầu vào (64 bit)

    Returns: Dữ liệu đã mã hoá bằng DES ở dạng Binary
    """
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
    return plantext
def DES_Decryption(plantext,key):
    """
    Thực hiện giải mã bằng DES

    Parameters:
    plantext (string): dữ liệu cần giải mã
    key (string): khoá đầu vào (64 bit)

    Returns: Dữ liệu đã giải mã bằng DES
    """
    temp=""
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
def EncryptFile(input_file, output_file,key):
    """
    Thực hiện mã hoá file bằng DES

    Parameters:
    input_file (string): tên file cần mã hoá
    output_file (string):  tên file chứa nội dung đã mã hoá
    key (string): khoá đầu vào (64 bit)

    Returns: File chứa nội dung đã mã hoá
    """
    with open(input_file,"r") as data:
        plantext=data.read()
    plantext=DES_Encryption(plantext,key)
    with open(output_file,'w') as data:
        data.write(plantext)
def DecryptFile(input_file, output_file,key):
    """
    Thực hiện giải mã file đã được mã hoá bằng DES

    Parameters:
    input_file (string): tên file cần giải mã
    output_file (string):  tên file chứa nội dung đã giải mã
    key (string): khoá đầu vào (64 bit)

    Returns: File chứa nội dung đã giải mã
    """
    with open(input_file,"r") as data:
        plantext=data.read()
    plantext=DES_Decryption(plantext,key)
    with open(output_file,'w') as data:
        data.write(plantext)
if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv)>5:
        print("Usage: python DES.py [encrypt/decrypt] input_file output_file key")
        sys.exit(1)
    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key=sys.argv[4]
    if action == "encrypt":
        EncryptFile(input_file, output_file,key)
    elif action == "decrypt":
        DecryptFile(input_file, output_file,key)
    else:
        print("Program don't know what do you want to do. Please use 'encrypt' or 'decrypt'.")
        sys.exit(1)
print("Demo Docker")