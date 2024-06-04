#soc_real.py用のパラメータ設定を行う

#1dataに乗せるフレーム数
#model・学習時と同じ形にしなければならない
nframes=20
parts=27
dof=4
motions={
    0:"walk",
    1:"suburi",
    2:"udehuri",
    3:"iai",
    4:"sit_stop",
    5:"sit_udehuri",
    6:"stand_neutral",
    7:"scwat",
    8:"fencing_stand",
}
#使用するモデルのパス
model_path="../learning/model/0529_model27_20.pth"

