#soc_real.py用のパラメータ設定を行う

#1dataに乗せるフレーム数
#model・学習時と同じ形にしなければならない
nframes=20
parts=27
dof=4
motions={
    0:"suburi",
    1:"iai",
    2:"stand_neutral",
}
#使用するモデルのパス
model_path="../learning/model/0521_model3data_27_20.pth"

