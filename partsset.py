import numpy as np


upper_pts=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
lower_pts=[0,19,20,21,22,23,24,25,26]
left_arm_pts=[7,11,12,13,14]
right_arm_pts=[7,15,16,17,18]
left_leg_pts=[0,19,20,21,22]
right_leg_pts=[0,23,24,25,26]



#qdata=[ファイルのフレーム数][27関節][クォータニオン]を受け取り、指定のパーツに分解する
#parts_list=[添え字番号のリスト]
def pts_cut(qdata,parts_list):
    parts_list.sort()
    print(len(parts_list))
    cut_data=np.empty((len(qdata),len(parts_list),len(qdata[0,0])))
    for f in range(len(qdata)):
        for i,pt in zip(range(len(parts_list)),parts_list):
            cut_data[f][i]=qdata[f][pt]
    return cut_data

def upper_body(qdata):
    return pts_cut(qdata,upper_pts)

def lower_body(qdata):
    return pts_cut(qdata,lower_pts)

def left_arm(qdata):
    return pts_cut(qdata,left_arm_pts)

def right_arm(qdata):
    return pts_cut(qdata,right_arm_pts)
 
def left_leg(qdata):
    return pts_cut(qdata,left_leg_pts)

def right_arm(qdata):
    return pts_cut(qdata,right_leg_pts)