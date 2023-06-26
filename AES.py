
rcon_num_of_calls=0
last_round_const=""
round_keys_list=[[],[],[],[],[],[],[],[],[],[],[]]


def matrix_to_text(matrix):
    res=""
    for i in range(4):
        for o in range(4):
            res+= matrix[i][o]
    return res

def bits_to_num(list_):
    res=0
    for i in range(4):
        res+=int(list_[i])*(2**i)
    
    return res

def list_in_byte(list_):
    res=b''
    
    res=res.join(bytes(i,'ascii') for i in list_)
    
    return res

def rotate(list_,n):
    return list_[len(list_)-n:]+list_[:len(list_)-n]

def rotate_right(list_,n):
    return list_[n:]+list_[:n]

def list_to_str(list_):
    string=""
    
    for i in list_:
        string+=str(i)
    
    return string

def text_to_byte(text):
    res=''
    bit_text=""
    append_int=16 - (len(text))%16
    if len(text)%16!=0:
        for i in range(append_int):
            text+="_"
    #print(text)
    bit_text=''.join(format(ord(i), '08b') for i in text)
    
    return bit_text

def matrix_len(matrix):
    len_matr = [
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]
    ]
    
    for i in range(4):
        for o in range(4):
            len_matr[i][o]=len(matrix[i][o])
    print(len_matr)

def hex_to_bit(text):
    hex_dict = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}
    bit_text = ""
    
    if len(text) ==1:
        text="0"+text
    
    for o in text:
        bit_text+=hex_dict[o]
        
    return bit_text

def bit_to_polinom(bits):
    polinom = ""
    polinom_dict = {0:"128",1:"64",2:"32",3:"16",4:"8",5:"4",6:"2",7:"1"}
    #print(bits)
    for i in range(8):
        if (int(bits[i])==1):
            polinom+=polinom_dict[i]+" "
    
    if(polinom==""):
        polinom+="0"
             
    return polinom

def polinom_multiply(polinom_text,polinom_mix_matrix):
    res=[0,0,0,0,0,0,0,0]
    polinom_text=polinom_text.split(' ')
    polinom_mix_matrix=polinom_mix_matrix.split(' ')
    
    polinom_text = polinom_text[:len(polinom_text)-1]
    polinom_mix_matrix = polinom_mix_matrix[:len(polinom_mix_matrix)-1]
    
    for i in polinom_mix_matrix:
        for o in polinom_text:
            if int(i)*int(o)==1024:
                res[1]^=1
                res[2]^=1
                res[4]^=1
                res[5]^=1                 
            if int(i)*int(o)==512:
                res[2]^=1
                res[3]^=1
                res[5]^=1
                res[6]^=1                
            if int(i)*int(o)==256:
                res[3]^=1
                res[4]^=1
                res[6]^=1
                res[7]^=1
            if int(i)*int(o)==128:
                res[0]^=1
            if int(i)*int(o)==64:
                res[1]^=1    
            if int(i)*int(o)==32:
                res[2]^=1 
            if int(i)*int(o)==16:
                res[3]^=1  
            if int(i)*int(o)==8:
                res[4]^=1
            if int(i)*int(o)==4:
                res[5]^=1
            if int(i)*int(o)==2:
                res[6]^=1
            if int(i)*int(o)==1:
                res[7]^=1    
    
    return list_to_str(res)

def GetColumn(col_num,text_table):
    res=[]
    for i in text_table:
        res.append(i[col_num])
    
    return res

def ShiftRows(text_table):
    for i in range(4):
        text_table[i]=rotate(text_table[i],i)
    
    return text_table

def InvShiftRows(text_table):
    for i in range(4):
        text_table[i]=rotate_right(text_table[i],i)
    
    return text_table

def InvMixColumns(text_table):
    MixMatrix = [
        ['0e','0b','0d','09'],
        ['09','0e','0b','0d'],
        ['0d','09','0e','0b'],
        ['0b','0d','09','0e']
        ]   
    
    res_matrix=[
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]
    ]
    
    disp_list_column=[]
    disp_list_row=[]
    
    
    for i in range(4):
        for o in range(4):
            disp_list_column=GetColumn(o,text_table)
            disp_list_row=MixMatrix[i]
            
            for t in range(4):
                GF_res = polinom_multiply( bit_to_polinom(disp_list_column[t]), bit_to_polinom(hex_to_bit(disp_list_row[t])))                
                #print(bit_to_polinom(disp_list_column[t]))
                #print(bit_to_polinom(hex_to_bit(disp_list_row[t])))
                if t==0:
                    res_matrix[i][o]=GF_res
                else:
                    res_matrix[i][o]= list_to_str([int(res_matrix[i][o][r]) ^ int(GF_res[r]) for r in range(8)])  
                
    return res_matrix

def MixColumns(text_table):
    MixMatrix = [
        ['02','03','01','01'],
        ['01','02','03','01'],
        ['01','01','02','03'],
        ['03','01','01','02']
        ]
    
    res_matrix=[
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]
    ]
    
    disp_list_column=[]
    disp_list_row=[]
    
    
    for i in range(4):
        for o in range(4):
            disp_list_column=GetColumn(o,text_table)
            disp_list_row=MixMatrix[i]
            
            for t in range(4):
                
                GF_res = polinom_multiply( bit_to_polinom(disp_list_column[t]), bit_to_polinom(hex_to_bit(disp_list_row[t])))                
                
                if t==0:
                    res_matrix[i][o]=GF_res
                else:
                    res_matrix[i][o]= list_to_str([int(res_matrix[i][o][r]) ^ int(GF_res[r]) for r in range(8)])  
    
    return res_matrix
    
def AddRoundKey(text_matrix,key_matrix):
    result_matrix = [
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]
    ]
    for i in range(4):
        for o in range(4):
            result_matrix[i][o]=list_to_str([ int(text_matrix[i][o][r]) ^ int(key_matrix[i][o][r]) for r in range(8)])
    
    #matrix_len(result_matrix)
    #print(matrix_to_text(result_matrix))
    return result_matrix

def InvSubBytes(text_matrix):
    
    result_matrix = [
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]
    ]
    
    Inversed_S_box=[
        ['52','09','6a','d5','30','36','a5','38','bf','40','a3','9e','81','f3','d7','fb'],
        ['7c','e3','39','82','9b','2f','ff','87','34','8e','43','44','c4','de','e9','cb'],
        ['54','7b','94','32','a6','c2','23','3d','ee','4c','95','0b','42','fa','c3','4e'],
        ['08','2e','a1','66','28','d9','24','b2','76','5b','a2','49','6d','8b','d1','25'],
        ['72','f8','f6','64','86','68','98','16','d4','a4','5c','cc','5d','65','b6','92'],
        ['6c','70','48','50','fd','ed','b9','da','5e','15','46','57','a7','8d','9d','84'],
        ['90','d8','ab','00','8c','bc','d3','0a','f7','e4','58','05','b8','b3','45','06'],
        ['d0','2c','1e','8f','ca','3f','0f','02','c1','af','bd','03','01','13','8a','6b'],
        ['3a','91','11','41','4f','67','dc','ea','97','f2','cf','ce','f0','b4','e6','73'],
        ['96','ac','74','22','e7','ad','35','85','e2','f9','37','e8','1c','75','df','6e'],
        ['47','f1','1a','71','1d','29','c5','89','6f','b7','62','0e','aa','18','be','1b'],
        ['fc','56','3e','4b','c6','d2','79','20','9a','db','c0','fe','78','cd','5a','f4'],
        ['1f','dd','a8','33','88','07','c7','31','b1','12','10','59','27','80','ec','5f'],
        ['60','51','7f','a9','19','b5','4a','0d','2d','e5','7a','9f','93','c9','9c','ef'],
        ['a0','e0','3b','4d','ae','2a','f5','b0','c8','eb','bb','3c','83','53','99','61'],
        ['17','2b','04','7e','ba','77','d6','26','e1','69','14','63','55','21','0c','7d']
    ]
    
    
    for i in range(4):
        for o in range(4):
            row = int( list_to_str(text_matrix[i][o][:4]),2)
            column = int( list_to_str(text_matrix[i][o][4:]),2)
            
            result_matrix[i][o]=hex_to_bit(Inversed_S_box[row][column])
    
    return result_matrix
    
def SubBytes(text_matrix):
    global rcon_num_of_calls
    result_matrix = [
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]
    ]
    
    s_box = [
        ['63','7c','77','7b','f2','6b','6f','c5','30','01','67','2b','fe','d7','ab','76'],
        ['ca','82','c9','7d','fa','59','47','f0','ad','d4','a2','af','9c','a4','72','c0'],
        ['b7','fd','93','26','36','3f','f7','cc','34','a5','e5','f1','71','d8','31','15'],
        ['04','c7','23','c3','18','96','05','9a','07','12','80','e2','eb','27','b2','75'],
        ['09','83','2c','1a','1b','6e','5a','a0','52','3b','d6','b3','29','e3','2f','84'],
        ['53','d1','00','ed','20','fc','b1','5b','6a','cb','be','39','4a','4c','58','cf'],
        ['d0','ef','aa','fb','43','4d','33','85','45','f9','02','7f','50','3c','9f','a8'],
        ['51','a3','40','8f','92','9d','38','f5','bc','b6','da','21','10','ff','f3','d2'],
        ['cd','0c','13','ec','5f','97','44','17','c4','a7','7e','3d','64','5d','19','73'],
        ['60','81','4f','dc','22','2a','90','88','46','ee','b8','14','de','5e','0b','db'],
        ['e0','32','3a','0a','49','06','24','5c','c2','d3','ac','62','91','95','e4','79'],
        ['e7','c8','37','6d','8d','d5','4e','a9','6c','56','f4','ea','65','7a','ae','08'],
        ['ba','78','25','2e','1c','a6','b4','c6','e8','dd','74','1f','4b','bd','8b','8a'],
        ['70','3e','b5','66','48','03','f6','0e','61','35','57','b9','86','c1','1d','9e'],
        ['e1','f8','98','11','69','d9','8e','94','9b','1e','87','e9','ce','55','28','df'],
        ['8c','a1','89','0d','bf','e6','42','68','41','99','2d','0f','b0','54','bb','16']        
    ]
    for i in range(4):
        for o in range(4):
            row = int( list_to_str(text_matrix[i][o][:4]),2)
            column = int( list_to_str(text_matrix[i][o][4:]),2)
            result_matrix[i][o]=hex_to_bit(s_box[row][column])
    
    #matrix_len(result_matrix)
    
    return result_matrix

def SubWord(list_):

    result = ["","","",""]
    
    s_box = [
        ['63','7c','77','7b','f2','6b','6f','c5','30','01','67','2b','fe','d7','ab','76'],
        ['ca','82','c9','7d','fa','59','47','f0','ad','d4','a2','af','9c','a4','72','c0'],
        ['b7','fd','93','26','36','3f','f7','cc','34','a5','e5','f1','71','d8','31','15'],
        ['04','c7','23','c3','18','96','05','9a','07','12','80','e2','eb','27','b2','75'],
        ['09','83','2c','1a','1b','6e','5a','a0','52','3b','d6','b3','29','e3','2f','84'],
        ['53','d1','00','ed','20','fc','b1','5b','6a','cb','be','39','4a','4c','58','cf'],
        ['d0','ef','aa','fb','43','4d','33','85','45','f9','02','7f','50','3c','9f','a8'],
        ['51','a3','40','8f','92','9d','38','f5','bc','b6','da','21','10','ff','f3','d2'],
        ['cd','0c','13','ec','5f','97','44','17','c4','a7','7e','3d','64','5d','19','73'],
        ['60','81','4f','dc','22','2a','90','88','46','ee','b8','14','de','5e','0b','db'],
        ['e0','32','3a','0a','49','06','24','5c','c2','d3','ac','62','91','95','e4','79'],
        ['e7','c8','37','6d','8d','d5','4e','a9','6c','56','f4','ea','65','7a','ae','08'],
        ['ba','78','25','2e','1c','a6','b4','c6','e8','dd','74','1f','4b','bd','8b','8a'],
        ['70','3e','b5','66','48','03','f6','0e','61','35','57','b9','86','c1','1d','9e'],
        ['e1','f8','98','11','69','d9','8e','94','9b','1e','87','e9','ce','55','28','df'],
        ['8c','a1','89','0d','bf','e6','42','68','41','99','2d','0f','b0','54','bb','16']        
    ]
    for i in range(4):
        row = int( list_[i][:4],2)
        #print(list_[i][4:])
        column = int( list_[i][4:],2)
        result[i]=  hex_to_bit( s_box[row][column])
    
    return result

def Rcon(list_):
    global rcon_num_of_calls,last_round_const
    rcon_num_of_calls+=1
    rcon_const=""
    rcon_const_dict = {1:"01",2:"02",3:"04",4:'08',5:'10',6:'20',7:'40',8:'80',9:'1b',10:'36',11:'6c'}
    
    if rcon_num_of_calls ==11:
        rcon_num_of_calls=1    
    
    rcon_const=hex_to_bit( rcon_const_dict[rcon_num_of_calls] )
    #print(rcon_const)
    list_[0]=list_to_str( [ int(rcon_const[i]) ^ int(list_[0][i]) for i in range(8) ] )
    
    return list_

def matrix_generator(text):
    matrix=[
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]        
    ]
    
    for o in range(4):
        for x in range(4):
            matrix[o][x]=text[:8]
            text=text[8:]
    #print(matrix)
    return matrix

def key_schedule(key_matrix):
    global round_keys_list,rcon_num_of_calls
    k1=GetColumn(0,key_matrix)
    k2=GetColumn(1,key_matrix)
    k3=GetColumn(2,key_matrix)
    k4=GetColumn(3,key_matrix)
    #print(k4)
    list_ =[k1,k2,k3,k4]
    round_key_list = [
        ["","","",""],
        ["","","",""],
        ["","","",""],
        ["","","",""]        
    ]
    
    
    initial_vector = Rcon(SubWord(rotate(k4,1)))
    
    for i in list_:
        for o in range(4):
            if list_.index(i)==0:
                list_[list_.index(i)][o]= list_to_str([int(i[o][x]) ^ int(initial_vector[o][x]) for x in range(8) ])
            else:
                list_[list_.index(i)][o]= list_to_str([int(i[o][x]) ^ int(list_[list_.index(i)-1][o][x]) for x in range(8) ])                
    
    for i in range(4):
        for o in range(4):
            round_key_list[o][i]=list_[i][o]
    
    round_keys_list[rcon_num_of_calls]=round_key_list
    #print(rcon_num_of_calls)
    return round_key_list

def AES_encrypt(plaintext,key):
    
    key_matrix = matrix_generator(key)
    text_matrix = matrix_generator(plaintext)
    
    text_matrix = AddRoundKey(text_matrix,key_matrix)
    #print(matrix_to_text(text_matrix))
    
    for i in range(9):
        key_matrix = key_schedule(key_matrix)
        text_matrix = AddRoundKey( MixColumns( ShiftRows( SubBytes(text_matrix) ) ), key_matrix)
        
    key_matrix = key_schedule(key_matrix)
    text_matrix = AddRoundKey( ShiftRows( SubBytes(text_matrix) ), key_matrix)
    
    return matrix_to_text(text_matrix)

def AES_decrypt(ciphertext,key):
    global round_keys_list
    key_matrix = matrix_generator(key)
    text_matrix = matrix_generator(ciphertext)
    #print(text_matrix)
    
    round_keys_list[0]=key_matrix
    
    for i in range(10):
        key_matrix=key_schedule(key_matrix)
    
    text_matrix = AddRoundKey(text_matrix,round_keys_list[10])
        
    for i in range(9):        
        text_matrix = InvMixColumns( AddRoundKey( InvSubBytes( InvShiftRows(text_matrix) ) , round_keys_list[9-i]))
        
        
    text_matrix = AddRoundKey( InvSubBytes( InvShiftRows(text_matrix) ) , round_keys_list[0])
    
    
    return matrix_to_text(text_matrix)

def main():
    while True:
        text=input("Enter text: ")
        key_int=int(input("Enter key: "))
        enc_decr=int(input("Encrypt - 1, Decrypt - 0 "))
        ciphertext=""
        plaintext=""
        hexStr=""
        key=[None]*128
        
        for i in range(128):
            key[127-i] = key_int % 2
            key_int = key_int // 2
        
        key=list_to_str(key)
            
        if(enc_decr==1):
            text=text.replace(' ', '_')
            bit_str=text_to_byte(text)
            #print(bit_str)
            #print(len(bit_str))
            res=""
            if(len(bit_str)%128!=0):
                loop_len = len(bit_str)//128+1
            else:
                loop_len = len(bit_str)//128
            
            for i in range(loop_len):
                res += AES_encrypt(bit_str[:128],key) 
                bit_str=bit_str[128:]
            
            for i in range(len(res)//8):
                if int(res[:8],2)>15:
                    hexStr+=hex(int(res[:8],2))
                else:
                    hexStr+="0"+hex(int(res[:8],2))
                res=res[8:]
            
            hexStr=hexStr.replace('0x','')
            print("Your ciphertext: "+hexStr)
        else:
            text=hex_to_bit(text)
            #print(text)
            res=""
            
            text_len=int(len(text)/8)            
            
            if(len(text)%128!=0):
                loop_len = len(text)//128+1
            else:
                loop_len = len(text)//128            
            
            for i in range(loop_len):
                plaintext+=AES_decrypt(text[:128],key)
                text=text[128:]            
            
            for i in range(text_len):
                res+=chr(int(plaintext[:8],2))
                plaintext=plaintext[8:]
            res=res.replace("_"," ")
            #print(len(res))
            print("Your plaintext: "+res)
    
    
main()






"""
if rcon_num_of_calls==1:
        rcon_const=hex_to_bit('01')
        last_round_const=rcon_const
        list_[0]=list_to_str( [int(list_[0][i]) ^ int(rcon_const[i]) for i in range(8)])
    elif rcon_num_of_calls==10:
        if int(last_round_const,2)>= int('80',16):
            string = hex_to_bit( str( hex( int(last_round_const,2) * 2)))
            
            hex_str=hex_to_bit('11b')
            
            rcon_const=list_to_str( [int(string[i]) ^ int(hex_str[i]) for i in range(8)])
            
            last_round_const=rcon_const                       
            
            list_[0]= list_to_str( [int(string[i]) ^ int(list_[0][i]) for i in range(8)])
            rcon_num_of_calls=0
        else:  
            
            string = hex_to_bit( str( hex( int(last_round_const,2) * 2)).replace('0x',''))
            
            last_round_const=string            
             
            list_[0]= list_to_str( [int(string[i]) ^ int(list_[0][i]) for i in range(8)] )        
    else:
        if int(last_round_const,2)>= int('80',16):
            string = hex_to_bit( str( hex( int(last_round_const,2) * 2 )).replace('0x',''))
            
            hex_str=hex_to_bit('11b')
            
            rcon_const=list_to_str( [int(string[i]) ^ int(hex_str[i]) for i in range(8)])
            
            last_round_const=rcon_const
                        
            list_[0]= list_to_str( [int(rcon_const[i]) ^ int(list_[0][i]) for i in range(8)])  
        else:
            string = str(hex_to_bit( str( hex( int(last_round_const,2) )*2).replace('0x','')))
            print("\n"+last_round_const)
            print(int(last_round_const,2))
            print(int(last_round_const,2)*2)
            print(hex( int(last_round_const,2)*2))
            print(str( hex( int(last_round_const,2)*2)).replace('0x',''))
            print(hex_to_bit( str( hex( int(last_round_const,2)*2)).replace('0x','')))
            
            last_round_const=string
            
            list_[0]= list_to_str([int(string[i]) ^ int(list_[0][i]) for i in range(8)])
    """
