import numpy as np
import readfile as rf
import partsset as ps

fp='sample_int.txt'
qdata,xdata=rf.file_sep(fp)
#print(qdata)
cut_qdata=ps.pts_cut(qdata,[0,1,2,3,24])
print(cut_qdata)