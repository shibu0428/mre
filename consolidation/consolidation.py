#接続、保存、学習、試験を一括(consolidation)で行う

#必要モジュールのimport
import socket
import time
import struct
import numpy as np
import winsound
import os

#torch関連の読み込み
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import ToTensor
import torchsummary

#自作関数読み込み
import sys
sys.path.append('..')
from lib import readfile as rf
from lib import partsset


#必要パラメータ
motions={
    0:"suburi",
    1:"iai",
    2:"udehuri",
}
N=10    #1モーションのデータの数
max_frames=20   #1データあたりのフレーム数
n_data=10       #1モーションのデータ数
parts=27
dof=4




#加工用の仮置きでフォルダ作成
#timestampを手書きで

folder_path='processing/0612/'
if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
else:
    print("既にフォルダが埋まってます。\n別のフォルダ名にするか、既存フォルダを削除してください。\n")
    print(folder_path)
    exit()
for motion in motions:
    print("フォルダ名 "+folder_path)
    print(motions[motion])
    os.mkdir(folder_path+motions[motion])


host = ''
port = 52353


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port))

# 受信用のバッファーサイズを設定
buffer_size = 4096



#data=[Nframe][27parts][4dof]
in_data=np.empty((max_frames,parts,dof))
#motion_dataset=[data数][Nframe][27parts][4dof]
motion_dataset=np.empty((len(motions)*N,max_frames,parts,dof))

#学習のclass定義
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
        self.fc3 = nn.Linear(H2, K) # 出力層には活性化関数を指定しない


        # モデルの出力を計算するメソッド
    def forward(self, X):
        X = self.flatten(X)
        X = self.fc1(X)
        X = self.fc2(X)
        X = self.fc3(X)
        return X

model = MLP4(max_frames*parts*dof,4096,4096, len(motions))
print(f"UDP 受信開始。ホスト: {host}, ポート: {port}")
n=0
fr=0
motion_id=0
print("3,2,1")
time.sleep(3)
print("start")
while True:
    if motion_id == len(motions):
        break
    try:
        # データを受信
        
        data, addr = udp_socket.recvfrom(buffer_size)
        #1575byteデータより大きいなら別データのためスキップ
        if(len(data)>1600):continue
        bnid_list = data.split(b'bnid')[1:]
        with open(+str(n)+'.txt', mode='a') as f:
            for id_parts,part in enumerate(bnid_list):
                tran_btdt_data = part.split(b'tran')[1:]
                dofdata = tran_btdt_data[0].split(b'btdt')[0]
                for id_dof,i in enumerate(range(0, par.dof*4, 4)):
                    in_data[flag,id_parts,id_dof] = struct.unpack('<f', dofdata[i:i+4])[0]
                    float_value = struct.unpack('<f', dofdata[i:i+4])
                    f.write(f"{float_value[0]} ")
            f.write(f"\n")
            f.close()


        fr=fr+1
        if fr>150:
            fr=0
            n=n+1
            if n>16:
                print("お疲れさまでした")
                udp_socket.close()
                exit()
            print(n,"番ファイルスタート")

    except OSError as e:
        # エラーが発生した場合は表示
        print(f"エラー: {e}")
        continue
