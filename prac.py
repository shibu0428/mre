import numpy as np
import lib.readfile as rf
import partsset as ps
import lib.sound.sound as mp3

fp='dataset/sample/sample_int.txt'
qdata,xdata=rf.file_sep(fp)
#print(qdata)
cut_qdata=ps.pts_cut(qdata,[0,1,2,3,24])
#print(cut_qdata)
mp3.start_mp3()

