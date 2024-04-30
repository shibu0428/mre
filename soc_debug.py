import socket
import time
import struct
import winsound
import mocopi_parser as mp



dof_parts=7 #つかうデータ=0,1,2,3==クォータニオン->dof=4
            #4,5,6=position->dof=7

host = ''
port = 52353

outfile=input("output file name?")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port))

# 受信用のバッファーサイズを設定
buffer_size = 8192

print(f"UDP 受信開始。ホスト: {host}, ポート: {port}")
max_sec=5
max_frame=max_sec*30
sum=0
flag=0
n=0
flames=1
ijou_time=time.time()
last_time = time.time()
time.sleep(1.5)
winsound.Beep(1400, 500)

while True:
    try:
        # データを受信
        
        data, addr = udp_socket.recvfrom(buffer_size)
        if flag==0:
            start_time = time.time()
        if(len(data)>1650):raise ValueError("eror")
        if flames>150:
            n=n+1
            flames=1
            winsound.Beep(440, 800)
            time.sleep(3)
            print(f"{n} file start")
            winsound.Beep(860, 800)
            start_time=time.time()
            continue
        
        with open(outfile+str(n)+'.txt', mode='a') as f:
            outdata=mp.parse(data)
            f.write(outdata)
            f.write(f"\n")
            f.close()
            flames=flames+1
        end_time = time.time()
        flag=1
        last_time = time.time()

        
    except OSError as e:
        # エラーが発生した場合は表示
        print(f"エラー: {e}")
    except Exception:
        print('error_',len(data))
        continue
