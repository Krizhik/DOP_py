import numpy as np
#Расстояние между точками
def dist_to(point1,point2):
    R1=((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2)**0.5
    return R1

#вычисление HDOP,VDOP,PDOP   
def dop_of_point(sts,point):
    num_sta=len(sts)
    matrix=np.array(sts).reshape(num_sta,3)
    #print (matrix)
    for i in range(0,len(matrix)):
        R=dist_to(matrix[i][:],point)
        for j in range(0,len(matrix[0])):
            matrix[i][j]=(matrix[i][j]-point[j])/R
    #print(matrix)
    matrix1=matrix.transpose()
    ATA=np.matmul(matrix1,matrix)
    Q=np.linalg.inv(ATA)
    #print(Q)
    HDOP=(Q[0][0]+Q[1][1])**0.5
    PDOP=(Q[0][0]+Q[1][1]+Q[2][2])**0.5
#    print("HDOP = ",HDOP)
#    print("PDOP = ",PDOP)
    DOP=[HDOP,PDOP]
    return DOP
'''Алгоритм использован самый простейший — трассировка луча. Последовательно проверяются все грани
 полигона на пересечение с лучом, идущим из точки, куда кликнул пользователь. Четное количество 
 пересечений или нет пересечений вовсе — точка за пределами полигона. Количество 
 пересечений нечетное — точка внутри. '''
def in_poligon(polygon,check_point):
    in_polygon_check = False
    x = check_point[0]
    y = check_point[1]
    for i in range(len(polygon)):
        xp = polygon[i][0]
        yp = polygon[i][1]
        xp_prev = polygon[i-1][0]
        yp_prev = polygon[i-1][1]
#        print("начало",xp,yp,"конец",xp_prev,yp_prev)
        if (((yp <= y and y < yp_prev) or (yp_prev <= y and y < yp)) and (x > (xp_prev - xp) * (y - yp) / (yp_prev - yp) + xp)):
            in_polygon_check = not in_polygon_check
    return in_polygon_check

#Вычисление среднего DOP в полигоне при текущей конфигурации станций
def dop_of_polygone(stas,geom_):
    geometry_=geom_.transpose()
    begx=min(np.array(geometry_)[0][:])
    begy=min(np.array(geometry_)[1][:])
    endx=max(np.array(geometry_)[0][:])
    endy=max(np.array(geometry_)[1][:])
    print ("min x = ",begx,"min y = ",begy)
    print ("max x = ",endx,"max y = ",endy)

    i=0
    j=0
    zone_step=0.1#float(input("Введите точность"))
    dop_map=np.zeros((int((endx-begx)/zone_step),int((endy-begy)/zone_step)))
    for xi in np.arange(begx,endx,zone_step):
        j=0
        for yi in np.arange(begy,endy,zone_step):
            if in_poligon(geometry,[xi,yi]):
                dop_map[i][j]=dop_of_point(stations,[xi,yi,20])[0]
            j+=1
        i+=1
    vvv=np.array(dop_map).mean()
    return vvv



num_st=int(input("Введите количество станций"))
zonе_height=float(input("Высота зоны"))
zone_widtch=float(input("ширина зоны"))
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

#задание точки измерения   1.327539092745131
op=[10,10,27]
dop_of_point(stations,op)
'''
геометрию зоны будем задавать как последовательность точек являющихся вершинами многоугольника
'''
geometry = np.array ([[0,0],[0,zonе_height],[zone_widtch,zonе_height],[zone_widtch,0]])
"""определение нахождения точки внутри очерченой вершинами области"""
op1=[10,12]
print(in_poligon(geometry,op1))     #проверка функции вхождения токи в полигон
print(dop_of_polygone(stations,geometry))       #проверка вычисления среднего

"""geometry_=geometry.transpose()
begx=min(np.array(geometry_)[0][:])
begy=min(np.array(geometry_)[1][:])
endx=max(np.array(geometry_)[0][:])
endy=max(np.array(geometry_)[1][:])
print ("min x = ",begx,"min y = ",begy)
print ("max x = ",endx,"max y = ",endy)

i=0
j=0
zone_step=0.1#float(input("Введите точность"))
dop_map=np.zeros((int((endx-begx)/zone_step),int((endy-begy)/zone_step)))
for xi in np.arange(begx,endx,zone_step):
    j=0
    for yi in np.arange(begy,endy,zone_step):
        if in_poligon(geometry,[xi,yi]):
            dop_map[i][j]=dop_of_point(stations,[xi,yi,20])[0]
        j+=1
    i+=1
vvv=np.array(dop_map).mean()
print(vvv)"""

