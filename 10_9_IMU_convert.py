import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time
import math
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
def rotate(acc, q,angle):
    # new_v = [2 * (q[1] * q[3] + q[0] * q[2]), 2 * (q[2] * q[3] - q[0] * q[1]),
    #          q[0] ** 2 - q[1] ** 2 - q[2] ** 2 + q[3] ** 2]
    ax = (acc[0] - math.sin(angle[0]*math.pi/180) * 1000)
    ay = (acc[1] - math.sin(angle[1]*math.pi/180)* 1000)
    az = (acc[2] - math.sin(angle[2]*math.pi/180) * 1000)
    x = quaternprod(q, [0, ax, ay, az])
    y = quaternprod(x , quaternconj(q))
    z = np.array([y[1], y[2], y [3]])
    return z
# def rotation(gyro_m,q,dt):
#     c=np.array([[0,-gyro_m[0],-gyro_m[1],-gyro_m[2]],[gyro_m[0],0,gyro_m[2],-gyro_m[1]],[gyro_m[1],-gyro_m[2],0,gyro_m[0]],[gyro_m[2],gyro_m[1],-gyro_m[0],0]])
#     aq = dt * 0.5 * np.dot(c, q) + q
#     norm = aq[0] ** 2 + aq[1] ** 2 + aq[2] ** 2 + aq[3] ** 2
#     new_q = aq / norm
#     return (new_q)
def rotation(gyro,q,dt):
    q0=q[0]-gyro[0]*dt*0.5*q[1]-gyro[1]*dt*0.5*q[2]-gyro[2]*dt*0.5*q[3]
    q1=0.5*gyro[0]*dt*q[0]+q[1]+gyro[2]*dt*0.5*q[2]-gyro[1]*dt*0.5*q[3]
    q2=gyro[1]*dt*0.5*q[0]-gyro[2]*dt*0.5*q[1]+q[2]+gyro[0]*dt*0.5*q[3]
    q3=gyro[2]*dt*0.5*q[0]+gyro[1]*dt*0.5*q[1]-gyro[0]*dt*0.5*q[2]+q[3]
    norm=q0**2+q1**2+q2**2+q3**2
    new_q=[q0/norm,q1/norm,q2/norm,q3/norm]
    return new_q

data ='linear.txt'
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
while 1:
    kp=0.9
    ki=0.02
    # time.sleep(dt)
    newdata = readdata(data, lc)
    lc += 1
    if lc<=200:
        e_x=e_x+float(newdata[0])
        e_y=e_y+float(newdata[1])
        e_z=e_z+float(newdata[2])-1000
        e_gx=e_gx+float(newdata[6])
        e_gy=e_gy+float(newdata[7])
        e_gz=e_gz+float(newdata[8])
    if lc>900:
        break
    print(lc)
    if lc > 200:

        gyro_m = [float(newdata[6])-e_gx/200, float(newdata[7])-e_gy/200, float(newdata[8])-e_gz/200]
        if -0.05<gyro_m[0]<0.05:
            gyro_m[0]=0
        if -0.05 < gyro_m[1] < 0.05:
                gyro_m[1] = 0
        if -0.05 < gyro_m[2] < 0.05:
            gyro_m[2] = 0

        # gyro_m=[0,0,0]
        acc=np.array([float(newdata[0])-e_x/200, float(newdata[1])-e_y/200, float(newdata[2])-e_z/200])
        # acc = np.array([float(newdata[0]) , float(newdata[1]) , float(newdata[2]) ])
        angle=[float(newdata[3]),float(newdata[4]),float(newdata[5])]
        # if -30<acc[0]<30:
        #     acc[0]=0
        # if -30 < acc[1] < 30:
        #      acc[1] = 0
        # if -30 < acc[2] < 30:
        #     acc[2] = 0
        # print(acc)
        new_q = rotation(gyro_m, new_q, dt)

        # print(acc_new)
        v=[2*(new_q[1]*new_q[3]-new_q[0]*new_q[2]),2*(new_q[2]*new_q[3]+new_q[0]*new_q[1]),new_q[0]**2-new_q[1]**2-new_q[2]**2+new_q[3]**2]
        norm=math.sqrt(acc[0]**2+acc[1]**2+acc[2]**2)
        alpha=[acc[0]/norm,acc[1]/norm,acc[2]/norm]
        e=[alpha[1]*v[2]-alpha[2]*v[1],alpha[2]*v[0]-alpha[0]*v[2],alpha[0]*v[1]-alpha[1]*v[0]]
        ex_int=ex_int+e[0]*ki
        ey_int=ey_int+e[1]*ki
        ez_int=ez_int+e[2]*ki
        alpha_x=gyro_m[0]+ex_int+e[0]*kp
        alpha_y=gyro_m[1]+ey_int+e[1]*kp
        alpha_z=gyro_m[2]+ez_int+e[2]*kp
        q=[0,0,0,0]
        q[0]=new_q[0]+0.5*dt*(-new_q[1]*alpha_x-new_q[2]*alpha_y-new_q[3]*alpha_z)
        q[1]=new_q[1]+0.5*dt*(new_q[0]*alpha_x+new_q[2]*alpha_z-new_q[3]*alpha_y)
        q[2]=new_q[2]+0.5*dt*(new_q[0]*alpha_y-new_q[1]*alpha_z+new_q[3]*alpha_x)
        q[3]=new_q[3]+0.5*dt*(new_q[0]*alpha_z+new_q[1]*alpha_y-new_q[2]*alpha_x)
        norm_q=q[0]**2+q[1]**2+q[2]**2+q[3]**2
        q[0]=q[0]/norm_q
        q[1]=q[1]/norm_q
        q[2]=q[2]/norm_q
        q[3]=q[3]/norm_q
        new_q=q
        angle_x=math.atan2(2*(q[2]*q[3]+q[0]*q[1]),1-2*(q[1]**2+q[2]**2))*57.3
        angle_y=math.asin(-2*(q[1]*q[3]-q[0]*q[2]))*57.3
        angle_z=math.atan2(2*(q[1]*q[2]+q[0]*q[3]),1-2*(q[2]**2+q[3]**2))*57.3
        print(angle_x,angle_y,angle_z)
        # print(q)
        acc_new = rotate(acc, q,angle)
        if 30 < acc_new[0] < 30:
            acc_new[0] = 0
        if 30 < acc_new[1] < 30:
            acc_new[1] = 0
        if 30 < acc_new[2] < 30:
            acc_new[2] = 0
        # print(acc_new)
        x=(acc_new[0])*mg
        y = (acc_new[1] ) *mg
        z = (acc_new[2])*mg
        lin_acc=[x,y,z]
        vx=v[0]+(x+a[0])*dt*0.5
        vy = v[1] + (y + a[1]) * dt * 0.5
        vz = v[2] + (z + a[2]) * dt * 0.5

        dx= d[0]+(vx+v[0])*dt*0.5
        dy = d[1] + (vy + v[1]) * dt * 0.5
        dz = d[2] + (vz + v[2]) * dt * 0.5
        # dx=d[0]+v[0]*dt+0.5*x*dt*dt*mg
        # dy=d[1]+v[1]*dt+0.5*y*dt*dt*mg
        # dz=d[2]+v[2]*dt+0.5*z*dt*dt*mg
        # vx=v[0]+x*dt*mg
        # vy=v[1]+y*dt*mg
        # vz=v[2]+z*dt*mg
        dxl.append(dx)
        dyl.append(dy)
        dzl.append(dz)
        a=[x,y,z]
        v=[vx,vy,vz]
        d=[dx,dy,dz]
    # if lc>200:
    #     plt.scatter(dxl, dyl)
    #     plt.ion()
    #     plt.pause(1)
    #     plt.close()

plt.scatter(dxl,dyl)
plt.show()
# fig=plt.figure()
# ax=fig.add_subplot(111,projection='3d')
# ax.scatter(dxl,dyl,dzl)
# plt.legend(loc='upper left')
# ax.set_xlabel('displacement in x')
# ax.set_ylabel('displacement in y ')
# ax.set_zlabel('displacement in z')
# plt.show()