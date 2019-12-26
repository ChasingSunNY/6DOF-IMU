import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl

def readdata(data,lc):
    with open(data,'r')as f:
        data= f.readlines()
        last_line= data[lc]
        imu = last_line.split()
        pass
    return(imu)
data ='static.txt'
hertz = 104
dt = 1/hertz
mg= 0.00981
lc=3
new_q=[1,0,0,0]
a=[0,0,0]
v=[0,0,0]
d=[0,0,0]
dxl=[]
dyl=[]
dzl=[]
e_x=0
e_z=0
e_y=0
e_gx=0
e_gy=0
e_gz=0
ex_int = 0
ey_int = 0
ez_int = 0
mg=0.00981
il=[]
xl=[]
yl=[]
zl=[]
xo=[]
yo=[]
zo=[]
gxo=[]
gyo=[]
gzo=[]
gx=[]
gy=[]
gz=[]
i=0
while 1:

    newdata = readdata(data, lc)


    lc += 1
    if lc <= 200:
        e_x = e_x + float(newdata[0])
        e_y = e_y + float(newdata[1])
        e_z = e_z + float(newdata[2]) - 1000
        e_gx = e_gx + float(newdata[6])
        e_gy = e_gy + float(newdata[7])
        e_gz = e_gz + float(newdata[8])
    if lc > 900:
        break
    print(lc)
    if lc > 200:
        print(e_gx,e_gy,e_gz)
        gyro_m = [float(newdata[6]) - e_gx / 200, float(newdata[7]) - e_gy / 200, float(newdata[8]) - e_gz / 200]
        # gyro_m=[0,0,0]
        acc = np.array([float(newdata[0]) - e_x / 200, float(newdata[1]) - e_y / 200, float(newdata[2]) - e_z / 200])
        # acc = np.array([float(newdata[0]) , float(newdata[1]) , float(newdata[2]) ])
        angle = [float(newdata[3]), float(newdata[4]), float(newdata[5])]
        x=(acc[0]-math.sin(float(newdata[3])*math.pi/180))*mg
        y=(acc[1]-math.sin(float(newdata[4])*math.pi/180))*mg
        z= (acc[2]-math.sin(float(newdata[3])*math.pi/180))*mg
        # if -0.05<gyro_m[0]<0.05:
        #     gyro_m[0]=0
        # if -0.05 < gyro_m[1] < 0.05:
        #         gyro_m[1] = 0
        # if -0.05 < gyro_m[2] < 0.05:
        #     gyro_m[2] = 0
        # x=float(newdata[0]) - e_x / 200

        # y = float(newdata[1]) - e_y / 200
        # z = float(newdata[2]) - e_z / 200
        xl.append(x)
        yl.append(y)
        zl.append(z)
        gx.append(gyro_m[0])
        gy.append(gyro_m[1])
        gz.append(gyro_m[2])
        xo.append(newdata[0])
        yo.append(newdata[1])
        zo.append(newdata[2])
        gxo.append(newdata[6])
        gyo.append(newdata[7])
        gzo.append(newdata[8])
        i+=1
        il.append(i)
        print(gyro_m)
        print(newdata[6],newdata[7],newdata[8])
print(e_gx/200)
print(e_gy/200)
print(e_gy/200)

plt.scatter(il,xo,label='acc in x from device')
plt.scatter(il,xl,label='acc in x after calibration')
plt.legend(loc='upper left')
plt.xlabel('count times')
plt.ylabel('acceleration when static')
plt.show()
plt.scatter(il,yo,label='acc in y from device')
plt.scatter(il,yl,label='acc in y after calibration')
plt.legend(loc='upper left')
plt.xlabel('count times')
plt.ylabel('acceleration when static')
plt.show()
plt.scatter(il,zo,label='acc in z from device')
plt.scatter(il,zl,label='acc in z after calibration')
plt.legend(loc='upper left')
plt.xlabel('count times')
plt.ylabel('acceleration when static')
plt.show()
plt.scatter(il,gxo,label='angular velocity in x from device')
plt.scatter(il,gx,label='angualr velocity in x after calibration')
plt.legend(loc='upper left')
plt.xlabel('count times')
plt.ylabel('angular velocity when static')
plt.show()
plt.scatter(il,gyo,label='angular velocity in x from device')
plt.scatter(il,gy,label='angualr velocity in x after calibration')
plt.legend(loc='upper left')
plt.xlabel('count times')
plt.ylabel('angular velocity when static')
plt.show()
plt.scatter(il,gzo,label='angular velocity in x from device')
plt.scatter(il,gz,label='angualr velocity in x after calibration')
plt.legend(loc='upper left')
plt.xlabel('count times')
plt.ylabel('angular velocity when static')
plt.show()