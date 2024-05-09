#mocopiの送信側を偽装するクライアントプログラム

import socket

HOST='localhost'
PORT=42842

frames=0
fp='rawdata/sample.txt'

data=[]

# バイナリファイルを読み込みモードでオープンする
with open(fp, 'rb') as f:
    for one_data in f:
        data.append(one_data)
print(data)
print(len(data))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: 
    s.connect((HOST, PORT)) 
    
    while True:
        print(frames)
        s.send(data[frames]+b'\n')
        frames+=1
        
        if frames>9:
            frames=0
