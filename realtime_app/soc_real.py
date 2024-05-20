import socket
import time
import struct
import numpy as np

#torch関連の読み込み
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import ToTensor
import torchsummary

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


#学習した時のclass定義と揃える
class MLP4(nn.Module):

    # コンストラクタ． D: 入力次元数， H1, H2: 隠れ層ニューロン数， K: クラス数
    def __init__(self, D, H1, H2,K):
        super(MLP4, self).__init__()
        # 4次元テンソルで与えられる入力を2次元にする変換
        self.flatten = nn.Flatten()
        # 入力 => 隠れ層1
        self.fc1 = nn.Sequential(
            nn.Linear(D, H1), nn.Sigmoid()
        )
        # 隠れ層1から隠れ層2へ
        self.fc2 = nn.Sequential(
            nn.Linear(H1,H2), nn.Sigmoid()
        )

        # 隠れ層 => 出力層
        self.fc2 = nn.Linear(H2, K) # 出力層には活性化関数を指定しない


        # モデルの出力を計算するメソッド
    def forward(self, X):
        X = self.flatten(X)
        X = self.fc1(X)
        X = self.fc2(X)

        return X

model = MLP4()
#モデルを読み込む
model.load_state_dict(torch.load("model.pth"))

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
            t_in_data = torch.from_numpy(in_data)

            #model実行後にin_dataのframeを前にずらす
            in_data = in_data[[1,2,3,4,4],:,:,:]



                    
            
    except OSError as e:
        # エラーが発生した場合は表示
        print(f"エラー: {e}")
        continue
