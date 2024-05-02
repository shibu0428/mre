# 準備あれこれ
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn
seaborn.set()
from torch.utils.data import Dataset

# PyTorch 関係のほげ
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import ToTensor
from torchvision.datasets import FashionMNIST
import torchsummary

#自作関数軍
import sys
sys.path.append('..')
from lib import readfile as rf
from lib import partsset as ps
import dataload as dl

#ファイルパス、種類クラスの親まで,/入り
fp="../dataset/0430/"
# クラス番号とクラス名
#label_map.keys()
#"suburi"=label_map.get(1)
labels_map = {
    0: "walk",
    1: "suburi",
    2: "udehuri",
}

#cudaの準備
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(device)
print(torch.cuda.is_available())

#データ読み込み
#ファイル添え字の設定
Lnum_s=0
Lnum_e=10
Lnum=Lnum_e-Lnum_s
#frameの設定
fra_s=0
fra_e=20
fra_sep=1
fnum=int((fra_e-fra_s)/fra_sep)
np_data = dl.dataloading(fp,labels_map,Lnum_s,Lnum_e,fra_s,fra_e,fra_sep)

#labelの添え字確認
np_data_label=np.zeros((Lnum*fnum*len(labels_map)))
for i in range(len(labels_map)):
    np_data_label[(i)*Lnum*fnum:(i+1)*Lnum*fnum] = i

t_data = torch.from_numpy(np_data)
print(t_data.shape)
t_data_label = torch.from_numpy(np_data_label)
print(t_data_label.shape)

#ファイル添え字の設定
Tnum_s=10
Tnum_e=15
Tnum=Tnum_e-Tnum_s

np_Tdata = dl.dataloading(fp,labels_map,Tnum_s,Tnum_e,fra_s,fra_e,fra_sep)

#labelの添え字確認
np_Tdata_label=np.zeros((Tnum*fnum*len(labels_map)))
for i in range(len(labels_map)):
    np_Tdata_label[(i)*Tnum*fnum:(i+1)*Tnum*fnum] = i

t_Tdata = torch.from_numpy(np_Tdata)
print(t_Tdata.shape)
t_Tdata_label = torch.from_numpy(np_Tdata_label)
print(t_Tdata_label.shape)
# data読み込み




class dataset_class(Dataset):
    def __init__(self,data,labels, transform=None):
        self.data = data
        self.labels = labels

    def __getitem__(self, index):
        return self.data[index],self.labels[index]

    def __len__(self):
        return len(self.labels)


# データ読み込みの仕組み
dsL = dataset_class(t_data,t_data_label)
dsT = dataset_class(t_Tdata,t_Tdata_label)
dlL = DataLoader(dsL, batch_size=10, shuffle=True)
dlT = DataLoader(dsT, batch_size=10, shuffle=False)
print(f'学習データ数: {len(dsL)}  テストデータ数: {len(dsT)}')






# 1epoch の学習を行う関数
#
def train(model, lossFunc, optimizer, dl):
    loss_sum = 0.0
    ncorrect = 0
    n = 0
    for i, (X, lab) in enumerate(dl):
        lab=lab.long()
        X, lab = X.to(device), lab.to(device)
        X = X.float()  # 入力データをFloat型に変換
        Y = model(X)           # 一つのバッチ X を入力して出力 Y を計算
        loss = lossFunc(Y, lab) # 正解ラベル lab に対する loss を計算
        optimizer.zero_grad()   # 勾配をリセット
        loss.backward()         # 誤差逆伝播でパラメータ更新量を計算
        optimizer.step()         # パラメータを更新
        n += len(X)
        loss_sum += loss.item()  # 損失関数の値
        ncorrect += (Y.argmax(dim=1) == lab).sum().item()  # 正解数

    return loss_sum/n, ncorrect/n

# 損失関数や識別率の値を求める関数
#
@torch.no_grad()
def evaluate(model, lossFunc, dl):
    loss_sum = 0.0
    ncorrect = 0
    n = 0
    for i, (X, lab) in enumerate(dl):
        lab=lab.long()
        X, lab = X.to(device), lab.to(device)
        X = X.float()  # 入力データをFloat型に変換
        Y = model(X)           # 一つのバッチ X を入力して出力 Y を計算
        loss = lossFunc(Y, lab)  # 正解ラベル lab に対する loss を計算
        n += len(X)
        loss_sum += loss.item() # 損失関数の値
        ncorrect += (Y.argmax(dim=1) == lab).sum().item()  # 正解数

    return loss_sum/n, ncorrect/n

##### 学習結果の表示用関数
# 学習曲線の表示
def printdata():
  data = np.array(results)
  fig, ax = plt.subplots(1, 2, facecolor='white', figsize=(12, 4))
  ax[0].plot(data[:, 0], data[:, 1], '.-', label='training data')
  ax[0].plot(data[:, 0], data[:, 2], '.-', label='test data')
  ax[0].axhline(0.0, color='gray')
  ax[0].set_ylim(-0.05, 1.75)
  ax[0].legend()
  ax[0].set_title(f'loss')
  ax[1].plot(data[:, 0], data[:, 3], '.-', label='training data')
  ax[1].plot(data[:, 0], data[:, 4], '.-', label='test data')
  ax[1].axhline(1.0, color='gray')
  ax[1].set_ylim(0.35, 1.01)
  ax[1].legend()
  ax[1].set_title(f'accuracy')
 

  # 学習後の損失と識別率
  loss2, rrate = evaluate(net, loss_func, dlL)
  print(f'# 学習データに対する損失: {loss2:.5f}  識別率: {rrate:.4f}')
  loss2, rrate = evaluate(net, loss_func, dlT)
  print(f'# テストデータに対する損失: {loss2:.5f}  識別率: {rrate:.4f}')
  plt.show()



  # 2層ニューラルネットを定義するクラス
#
class MLP2(nn.Module):

    # コンストラクタ． D: 入力次元数， H: 隠れ層ニューロン数， K: クラス数
    def __init__(self, D, H, K):
        super(MLP2, self).__init__()
        # 4次元テンソルで与えられる入力を2次元にする変換
        self.flatten = nn.Flatten()
        # 入力 => 隠れ層
        self.fc1 = nn.Sequential(
            nn.Linear(D, H), nn.ReLU()
        )
        # 隠れ層 => 出力層
        self.fc2 = nn.Linear(H, K) # 出力層には活性化関数を指定しない

    # モデルの出力を計算するメソッド
    def forward(self, X):
        X = self.flatten(X)
        X = self.fc1(X)
        X = self.fc2(X)
        return X
    
    ##### 学習の実行 #####

class MLP3(nn.Module):

    # コンストラクタ． D: 入力次元数， H1, H2: 隠れ層ニューロン数， K: クラス数
    def __init__(self, D, H1, H2,H3,H4,H5, K):
        super(MLP3, self).__init__()
        # 4次元テンソルで与えられる入力を2次元にする変換
        self.flatten = nn.Flatten()
        # 入力 => 隠れ層1
        self.fc1 = nn.Sequential(
            nn.Linear(D, H1), nn.ReLU()
        )
        ### 続きを自分で書いてね ###
        # 隠れ層1から隠れ層2へ
        self.fc2 = nn.Sequential(
            nn.Linear(H1,H2),nn.ReLU()
        )
        self.fc3 = nn.Sequential(
            nn.Linear(H2,H3),nn.ReLU()
        )
        self.fc4 = nn.Sequential(
            nn.Linear(H3,H4),nn.ReLU()
        )
        self.fc5 = nn.Sequential(
            nn.Linear(H4,H5),nn.ReLU()
        )

        # 隠れ層 => 出力層
        self.fc6 = nn.Linear(H5, K) # 出力層には活性化関数を指定しない


        # モデルの出力を計算するメソッド
    def forward(self, X):
        X = self.flatten(X)
        X = self.fc1(X)
        X = self.fc2(X)
        X = self.fc3(X)
        X = self.fc4(X)
        X = self.fc5(X)
        X = self.fc6(X)

        return X

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
        ### 続きを自分で書いてね ###
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


# ネットワークモデル
net = MLP4(t_data.size(1)*t_data.size(2)*t_data.size(3),64,64, 3).to(device)
#torchsummary.summary(net, (1, 28, 28))
print(net)

# 損失関数（交差エントロピー）
loss_func = nn.CrossEntropyLoss(reduction='sum')

# パラメータ最適化器
optimizer = torch.optim.Adam(net.parameters(), lr=1e-5)

# 学習の繰り返し回数
nepoch = 100

# 学習
results = []
print('# epoch  lossL  lossT  rateL  rateT')
for t in range(1, nepoch+1):
    lossL, rateL = train(net, loss_func, optimizer, dlL)
    lossT, rateT = evaluate(net, loss_func, dlT)
    results.append([t, lossL, lossT, rateL, rateT])
    if(t%10==0):
        print(f'{t}   {lossL:.5f}   {lossT:.5f}   {rateL:.4f}   {rateT:.4f}')
printdata()