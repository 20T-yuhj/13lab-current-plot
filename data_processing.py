import matplotlib.pyplot as plt
import numpy as np
file_name = "afterECC-Pt-0.02.txt"
f = open(file_name, 'r').readlines()
Voltage = []
Current = []

initial = 0.45

plt.rcParams["font.family"] = "Times New Roman"   # 使用するフォント
plt.rcParams["font.size"] = 14                 # 文字の大きさ

start_line = f.index('Potential/V, Current/A\n') + 2

for lines in f[start_line:]:
    data_temp = lines.split(',')
    Voltage.append(float(data_temp[0]))
    Current.append(float(data_temp[1]))
# データ処理

position = np.where(np.array(Voltage) == initial)[0]
# print(position) #電圧がinitialの位置をarrayで表示

fig,ax1 = plt.subplots()

color = '#0000ff'
ax1.set_xlabel('Voltage/V')
ax1.set_ylabel('Current/A')
ax1.plot(Voltage[int(position[0]):int(position[2]-1)],Current[int(position[0]):int(position[2]-1)],label = '1st',markersize=1)
ax1.plot(Voltage[int(position[2]):int(position[4]-1)],Current[int(position[2]):int(position[4]-1)],label = '2nd',markersize=1)
ax1.plot(Voltage[int(position[4]):],Current[int(position[4]):],label = '3rd',markersize=1)
plt.legend()
plt.show()