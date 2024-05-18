import socket
import time
import struct
import binascii
import winsound
import numpy as np

#自作関数読み込み
import param_soc_real as par


dof_parts=7 
host = ''
port = 52353


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port))

# 受信用のバッファーサイズを設定
buffer_size = 8192

print(f"UDP 受信開始。ホスト: {host}, ポート: {port}")

#data=[Nframe][27parts][4dof]
in_data=np.empty((par.nframes,27,4))

#最初のnframeまでは前側のデータが足りないため
#データがそろうまではmodel読み込みをスキップ
flag=0

while True:
    try:
        # データを受信
        
        data, addr = udp_socket.recvfrom(buffer_size)
        #1575byteデータより大きいなら別データのためスキップ
        if(len(data)>1600):continue

        bnid_list = data.split(b'bnid')[1:]
        for id_parts,part in enumerate(bnid_list):
            tran_btdt_data = part.split(b'tran')[1:]
            dofdata = tran_btdt_data[0].split(b'btdt')[0]
            for id_dof,i in enumerate(range(0, 28, 4)):
                in_data[flag,id_parts,id_dof] = struct.unpack('<f', dofdata[i:i+4])
                if flag!=4:
                    flag+=1

        if flag==4:
            print("実装中dao!")
            #ここにモデルに入れて識別するものを構築

            #model実行後にin_dataのframeを前にずらす
            in_data = in_data[[1,2,3,4,4],:,:,:]



                    
            
    except OSError as e:
        # エラーが発生した場合は表示
        print(f"エラー: {e}")
        continue
