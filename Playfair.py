import math                 #올림함수 ceil()을 위해 선언

#키 조합 조건 검사 및 리턴
def key_match():
    while True:
        try:
            match=input("합칠 알파벳 [ex ([ch1]/[ch2] 단 ch1>ch2)]:").upper()
            check=list(match)
            if len(check)==3 and check[0].isalpha() and check[2].isalpha() and check[1]=='/' and check[0]<check[2]:
                return check
            else:
                print("형식에 맞게 다시 입력해주세요")
                
        except IndexError:
            continue

#암호화 테이블
def data_twin(data,match_list):
    twin_temp=[]
    c=0
    data=list(data)
    for i in range(len(data)):
        if data[i]==match_list[2]:
            data[i]=match_list[0]
         
    while True:
        try:
            if data[c]==data[c+1]:
                data.insert(c+1,'X')
                twin_temp.append(data[c:c+2])
                c+=2
            else:       
                twin_temp.append(data[c:c+2])
                c+=2
        except IndexError:
            if len(data)%2==1:
                data.append('X')
                twin_temp.append(data[c:c+2])
                break
            else:
                break
            
    return twin_temp

#암호화
def encrypt(Twin_list,Table):
    temp=[[],[]]#각 문자의 좌표 
    for _len in range(len(Twin_list)):
        for k in range(0,2):
            for i in range(0,5):
                for j in range(0,5):
                    if Twin_list[_len][k]==Table[i][j]:
                        temp[k].append([i,j])
    
    for i in range(len(Twin_list)):
        #두 좌표가 서로 대각일때
        if temp[0][i][0]!=temp[1][i][0] and temp[0][i][1]!=temp[1][i][1]: 
            Twin_list[i][0]=Table[temp[1][i][0]][temp[0][i][1]]
            Twin_list[i][1]=Table[temp[0][i][0]][temp[1][i][1]]
            
        #두 좌표가 수평일때
        elif temp[0][i][0]==temp[1][i][0]:
            
            if temp[0][i][1]+1>=5:
                Twin_list[i][0]=Table[temp[0][i][0]][0]
            else:
                Twin_list[i][0]=Table[temp[0][i][0]][temp[0][i][1]+1]
                
            if temp[1][i][1]+1>=5:
                Twin_list[i][1]=Table[temp[0][i][0]][0]
            else:
                Twin_list[i][1]=Table[temp[0][i][0]][temp[1][i][1]+1]
                
        #두 좌표가 수직일때
        elif temp[0][i][1]==temp[1][i][1]:
            if temp[0][i][0]+1>=5:
                Twin_list[i][0]=Table[0][temp[0][i][1]]
            else:   
                Twin_list[i][0]=Table[temp[0][i][0]+1][temp[0][i][1]]
                
            if temp[1][i][0]+1>=5:
                Twin_list[i][1]=Table[0][temp[0][i][1]]
            else:
                Twin_list[i][1]=Table[temp[1][i][0]+1][temp[0][i][1]]
                
    return Twin_list

#5X5 암호화 테이블 생성
def Matrix(key,match_list):
    key_list=list(key)
    temp_list=[]
    matrix_5x5 = [[0 for i in range (5)] for j in range(5)] 
    Table_file=open("Table.txt","w",encoding="utf-8")

    for c in key_list:
        if c not in temp_list:
            temp_list.append(c)
            
    for c in range(65,91):
        if chr(c) not in temp_list:
            temp_list.append(chr(c))
        else:
            pass
        
    for i,c in enumerate(temp_list):
        if c==match_list[0]:
            temp_list[i]=''.join(match_list)
        if c==match_list[2]:
            del temp_list[i]
            
    print("암호화 테이블")    
    for i in range(5):
        for j in range(5):
            matrix_5x5[i][j]=temp_list[(i*5)+j]
            print(matrix_5x5[i][j],end="\t")
            Table_file.write(matrix_5x5[i][j]+"\t")
            
            if len(matrix_5x5[i][j])==3:
                matrix_5x5[i][j]=match_list[0]
        Table_file.write(''.join('\n'))
        print("\n")
        
    Table_file.close()
    
    return matrix_5x5

def show(original_data,Twin_list,encrypt_data):
    
    print("원본:\t\t",end="")
    for i in range(len(original_data)):
        print(original_data[i],end="")
        if i%2==1:
            print(" ",end="")

    print("\n중간과정:\t",end="")
    for i in range(len(Twin_list)):
        for j in range(2):
            print(Twin_list[i][j],end="")
        print(" ",end="")

    print("\n암호문:\t\t",end="")
    for i in range(len(encrypt_data)):
        for j in range(2):
            print(encrypt_data[i][j],end="")
        print(" ",end="")

def save(data,enc_data):
    origin_file=open("original.txt","w",encoding="utf-8")
    enc_file=open("encode.txt","w",encoding="utf-8")
    for d in data:
        origin_file.write(d)
    for d in range(len(enc_data)):
        for i in range(2):
            enc_file.write(enc_data[d][i])

    origin_file.close()
    enc_file.close()
    
def main():

    #테스트용
    #key="assassinator".upper().replace(" ","")
    #data="be carefue for assassinator".upper().replace(" ","")
    
    key=""
    data=""
    while not key.encode().isalpha():
        key=input("키 입력:").upper().replace(" ","")

    while not data.encode().isalpha():
        data=input("평문 입력:").upper().replace(" ","")
        
    match_list=key_match()

    Twin_list=data_twin(data,match_list)
    Table=Matrix(key,match_list)#암호화 테이블 작성
    enc_data=encrypt(Twin_list,Table)
    show(data,data_twin(data,match_list),enc_data)
    save(data,enc_data)
    
if __name__ == "__main__":
    main()
