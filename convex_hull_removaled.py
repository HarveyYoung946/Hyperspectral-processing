from pysptools import spectro as sp
import numpy as np
import pandas as pd
import os
base_path = r"C:\Users\Administrator\Desktop\普朗数据整理\勘查线00\钻孔0017"
path = os.path.join(base_path,"temp04.csv")

csv_data = pd.read_csv(path,header=None)
data = np.array(csv_data)
data_size = data.shape
print(['共',data_size[1],'条数据'])
wavelength = np.linspace(1, 2151, 2151)
refl_removed = np.zeros([data_size[0],data_size[1]])

for i in range(0,data_size[1]):
    CR = sp.convex_hull_removal(data[:,i], wavelength)  # CR为元组，第一维是去包络线后的值，第二维是波长，第三维是去包络线值
    refl_removed[:,i] = CR[0]
    if i % 100 == 0:
        print(['运行至', i, '条数据'])
paths = os.path.join(base_path,"temp05.csv")
np.savetxt(paths, refl_removed, delimiter=',')

print('done')