import socket
import time
import struct
import binascii
import winsound


dof_parts=7 #つかうデータ=0,1,2,3==クォータニオン->dof=4
            #4,5,6=position->dof=7

host = ''
port = 52353

outfile=input("output file name?")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port))

# 受信用のバッファーサイズを設定
buffer_size = 8192
flames=1

print(f"UDP 受信開始。ホスト: {host}, ポート: {port}")
print('start recording')

while True:
    try:
        # データを受信
        
        data, addr = udp_socket.recvfrom(buffer_size)
        if(len(data)>1600):raise Exception()

        with open(outfile+'.dat', mode='ab') as f:
            f.write(data+b'\n')
            print("write!",flames)
            flames+=1
            f.close()
        if flames>90:
            exit()
    except OSError as e:
        # エラーが発生した場合は表示
        print(f"エラー: {e}")
    except Exception:
        continue
