import numpy as np
def dist_to(point1,point2):
    R1=((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2)**0.5
    return R1
    
def dop_of_point(sts,point):
    num_sta=len(sts)
    matrix=np.array(sts).reshape(num_sta,3)
    print (matrix)
    for i in range(0,len(matrix)):
        R=dist_to(matrix[i][:],point)
        for j in range(0,len(matrix[0])):
            matrix[i][j]=(matrix[i][j]-point[j])/R
    print(matrix)
    matrix1=matrix.transpose()
    ATA=np.matmul(matrix1,matrix)
    Q=np.linalg.inv(ATA)
    print(Q)
    HDOP=(Q[0][0]+Q[1][1])**0.5
    PDOP=(Q[0][0]+Q[1][1]+Q[2][2])**0.5
    print("HDOP = ",HDOP)
    print("PDOP = ",PDOP)
    DOP=[HDOP,PDOP]
    return DOP


num_st=int(input("Введите количество станций"))
zonе_height=input("Высота зоны")
zone_widtch=input("ширина зоны")
#ввод координат станций
 
stations =list([[20.0,0.0,30.0],[0.0,20.0,30.0],[20.0,20.0,30.0],[0.0,0.0,30.0]])
'''
stations = []
for i in range(0,num_st):
    st=[0, 0, 0]
    st[0]=float(input("X"))
    st[1]=float(input("Y"))
    st[2]=float(input("Z"))
    stations.append(st)'''
print(stations)   

#задание точки измерения
op=[10,10,27]
dop_of_point(stations,op)