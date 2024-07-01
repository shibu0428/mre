import glob
import os



def movefiles():
    motions={
    0:"guruguru_stand",
    1:"suburi",
    2:"udehuri",
    3:"iai",
    4:"sit_stop",
    5:"sit_udehuri",
    6:"stand_nautral",
    7:"scwat",
    8:"fencing_stand",
    }
    out_folder="0702"
    in_path = '*.csv'
    folder_path='../dataset/rawcsv/'+out_folder+'/'
    if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
    else:
        print("既にフォルダが埋まってます。\n上書きしてもよろしいですかy/n\n")
        print(folder_path)
        flag=input("y/n\n")
        if flag!="y":
            exit()
    for motion in motions:
        print("フォルダ名 "+folder_path)
        print(motions[motion])
        os.mkdir(folder_path+motions[motion])

    flist = glob.glob(in_path)


if __name__ == "__main__":
    movefiles()