import numpy as np
import pandas as pd
import pylab as plt
import os

base_path = r"C:\Users\Administrator\Desktop\普朗数据整理\勘查线00\钻孔0017"
path = os.path.join(base_path,"temp03.csv")
csv_data = pd.read_csv(path)
data = np.array(csv_data)
data_size = data.shape
"""
* 创建系数矩阵X
* size - 2×size+1 = window_size
* rank - 拟合多项式阶次
* x - 创建的系数矩阵
"""
def create_x(size, rank):
    x = []
    for i in range(2 * size + 1):
        m = i - size
        row = [m**j for j in range(rank)]
        x.append(row)
    x = np.mat(x)
    return x

"""
 * Savitzky-Golay平滑滤波函数
 * data - list格式的1×n纬数据
 * window_size - 拟合的窗口大小
 * rank - 拟合多项式阶次
 * ndata - 修正后的值
"""
def savgol(data, window_size, rank):
    m = (window_size - 1) // 2
    odata = data[:]
    # 处理边缘数据，首尾增加m个首尾项
    for i in range(m):
        odata.insert(0,odata[0])
        odata.insert(len(odata),odata[len(odata)-1])
    # 创建X矩阵
    x = create_x(m, rank)
    # 计算加权系数矩阵B
    b = (x * (x.T * x).I) * x.T
    a0 = b[m]
    a0 = a0.T
    # 计算平滑修正后的值
    ndata = []
    for i in range(len(data)):
        y = [odata[i + j] for j in range(window_size)]
        y1 = np.mat(y) * a0
        y1 = float(y1)
        ndata.append(y1)
    return ndata


filtered_data = np.zeros([data_size[0],data_size[1]])
print(['共',data_size[1],'条数据'])
for i in range(0,data_size[1]):

    SG_filtered = savgol(list(data[:,i]),window_size=15,rank=3)
    SG_filtered = np.array(SG_filtered)
    filtered_data[:,i] = SG_filtered
    if i % 100 ==0:
        print(['运行至',i,'条数据'])
paths = os.path.join(base_path,"temp04.csv")
np.savetxt(paths,filtered_data,delimiter=',')

plt.subplot(121)
plt.plot(data[:,0])

plt.subplot(122)
plt.plot(filtered_data[:,0])
plt.show()
print('done')