import time
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

data ='rectangle_new.txt'
hertz = 104;
dt = 1/hertz;
mg= 0.00981;
def readdata(data,lc):
    with open(data,'r')as f:
        data= f.readlines()
        last_line= data[lc]
        imu = last_line.split()
        pass
    return(imu)
def quaternconj(q):
    qj =[q[0],-q[1],-q[2],-q[3]]
    return qj
def quaternprod(a,b):
    ans = [0,0,0,0]
    ans[0]=a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3]
    ans[1]=a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2]
    ans[2]=a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1]
    ans[3]=a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]
    return ans
def quaternrotate(acc, q,v):
    x = quaternprod(q, [0, acc [0], acc [1], acc [2]])
    y = quaternprod(x , quaternconj(q))
    accx=y[1]-v[0]*1000
    accy=y[2]-v[1]*1000
    accz=y[3]-v[2]*1000
    z = np.array([accx,accy,accz])
    return z
def rotation(gyro_m,q,dt):
    c=np.array([[0,-gyro_m[0],-gyro_m[1],-gyro_m[2]],[gyro_m[0],0,gyro_m[2],-gyro_m[1]],[gyro_m[1],-gyro_m[2],0,gyro_m[0]],[gyro_m[2],gyro_m[1],-gyro_m[0],0]])
    new_q=dt*0.5*np.dot(c,q)+q
    return new_q

k=0.02
acc_m = np.array([0,0,0])
acc_d = np.array([0,0,0])
gyro = np.array([0,0,0])
acc_newcoordinate = np.array([0,0,0])
speed_x=[0]
speed_y=[0]
speed_z=[0]
roll=[0]
pitch=[0]
positionx=0
positiony=0
positionz=0
sumx=0
sumy=0
sumz=0
sum_x=[0]
sum_y=[0]
sum_z=[0]
i=0
ic=[0]
free_fall_count=0
q=[1,0,0,0]
lc=3
groll=[0]
gpitch=[0]
ic=[0]
yaw=[0]
while 1:
# def main():
    time.sleep(dt);
    newdata= readdata(data,lc)
    lc+=1
    x=float(newdata[0])
    y=float(newdata[1])
    z=float(newdata[2])
    acc_m=np.row_stack((acc_m,[x,y,z]))
    acc=np.array([x,y,z])
    acc_d= np.row_stack((acc_d,[float(newdata[3]),float(newdata[4]),float(newdata[5])]))
    gyro_m=[float(newdata[6]),float(newdata[7]),float(newdata[8])]
    gyro= np.row_stack((gyro,[float(newdata[6]),float(newdata[7]),float(newdata[8])]))


    phi=math.atan2(y,math.sqrt(x**2+z**2))
    theta=math.atan2(-x,math.sqrt(y**2+z**2))
    roll_i1=k*(roll[i]+float(newdata[6])*dt)+(1-k)*(phi*180/math.pi)
    roll.append(roll_i1)
    pitch_i1=k*(pitch[i]+float(newdata[7])*dt)+(1-k)*(theta*180/math.pi)
    pitch.append(pitch_i1)
    yaw_i1=yaw[i]+float(newdata[8])*dt
    yaw.append(yaw_i1)

    roll_g=groll[i]+float(newdata[6])*dt
    groll.append(roll_g)
    pitch_g=gpitch[i]+float(newdata[7])*dt
    gpitch.append(pitch_g)
    i+=1
    ic.append(i)
    if lc>1400:
        break

plt.scatter(ic,roll,label='roll after c')
plt.scatter(ic,groll,label='roll from g')
plt.legend(loc='upper left')
plt.show()
plt.close()
plt.scatter(ic,pitch,label='pitch after c')
plt.scatter(ic,gpitch,label='pitch from g')
plt.legend(loc='upper left')
plt.show()
plt.close()
plt.scatter(ic,yaw,label='yaw')
plt.show()
