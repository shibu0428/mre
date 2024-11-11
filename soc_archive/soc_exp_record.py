import socket
import struct

# UDPの受信設定
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("192.168.68.54", 5002))  # IPアドレスを指定してバインド

filename=input("ファイル名")
print("Waiting for UDP data")
nframe=0
dataframe=2000
minframe=300

maxframe=dataframe+minframe



with open(filename+'.csv',mode='a') as f:
    while True:
        data, addr = udp_socket.recvfrom(1024)  # データを受信
        if nframe == 0:
            print("300フレーム後に開始します")
        nframe+=1

        #開始のフレームより早いなら処理しない
        if nframe<minframe:
            continue

        #終了フレームを過ぎたらレコーディングを終了してデバック表示&exit
        if nframe>maxframe:
            print("レコーディング完了\n",
                  "ファイル名",filename,".csv\n",
                  "フレーム数",dataframe,"\n",
                  "終了します\n")
            f.close()
            exit()
        if nframe%50 == 0:
            print(nframe-300)
        #バイト列を処理して書き込み
        for i in range(6):
            f.write(str(struct.unpack('<ffffffff', data[i*40:i*40+32])).replace(")(", ",").replace("(", "").replace(")", ""))
            f.write(",")
            f.write(str(struct.unpack('<q', data[i*40+32:i*40+40])).replace(")(", ",").replace("(", "").replace(")", ""))
        f.write(f"\n")
