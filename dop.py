import numpy as np
import copy
from datetime import datetime

#Коллинеарность 
'''Определение нахождения трех точек на одной прямой может быть реализовано за счет определения площади треугольника
с вершинами на интересующих точках. Если площадь близка к нулю то точки коллинеарны'''
def collinear(point1,point2,point3):
    return ((point2[0]-point1[0])*(point3[1]-point1[1])-(point3[0]-point1[0])*(point2[1]-point1[0]))
#Расстояние между точками
def dist_to(point1,point2):
    R1=((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2)**0.5
    return R1

#вычисление HDOP,VDOP,PDOP для точки на полигоне при текущем размещении станций
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
    try:
        Q=np.linalg.inv(ATA)
    except:
        DOP=[10000,10000]
        return DOP
    #print(Q)
    
    HDOP=((Q[0][0]+Q[1][1])**0.5) if (Q[0][0]+Q[1][1])>0 else 10000
    PDOP=((Q[0][0]+Q[1][1]+Q[2][2])**0.5) if (Q[0][0]+Q[1][1]+Q[2][2])>0 else 10000
    
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
def dop_of_polygone(stas,geom_,begx,begy,endx,endy):
    """geometry_=geom_.transpose()
    begx=min(np.array(geometry_)[0][:])
    begy=min(np.array(geometry_)[1][:])
    endx=max(np.array(geometry_)[0][:])
    endy=max(np.array(geometry_)[1][:])
    print ("min x = ",begx,"min y = ",begy)
    print ("max x = ",endx,"max y = ",endy)
    """
    i=0
    j=0
    zone_step=1#float(input("Введите точность"))
    dop_map=np.zeros((int((endx-begx)/zone_step),int((endy-begy)/zone_step)))
    for xi in np.arange(begx,endx,zone_step):
        j=0
        for yi in np.arange(begy,endy,zone_step):
            if in_poligon(geometry,[xi,yi]):
                dop_map[i][j]=dop_of_point(stas,[xi,yi,28])[0]
            j+=1
        i+=1
    vvv=np.array(dop_map).mean()
    return vvv



num_st=int(input("Введите количество станций"))
zonе_height=float(input("Длинна зоны"))
zone_widtch=float(input("ширина зоны"))

now = datetime.now()
print("Время начала:  ", now)
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
'''[zone_widtch*1.5,zonе_height/2],'''
geometry = np.array ([[0,0],[0,zonе_height],[zone_widtch,zonе_height],[zone_widtch,0]])
"""определение нахождения точки внутри очерченой вершинами области"""
op1=[10,12]
print(in_poligon(geometry,op1))     #проверка функции вхождения токи в полигон


#функция перебора всех возможных расстановок станций на местности для 4 станций
geometry_=geometry.transpose()
begx=min(np.array(geometry_)[0][:])
begy=min(np.array(geometry_)[1][:])
endx=max(np.array(geometry_)[0][:])
endy=max(np.array(geometry_)[1][:])
print(dop_of_polygone(stations,geometry,begx,begy,endx,endy))       #проверка вычисления среднего
#шаг по зоне
zone_stepx=endx/10#float(input("Введите точность"))
zone_stepy=endy/10
#минимальное расстояние между станциями
min_distx=zone_stepx*2 - 0.00000001
min_disty=zone_stepy*2 - 0.00000001
counter=0 #счетчик количества итераций
min_dop=100000 #здесь будет храниться минимальный DOP
min_coll=2
station_min_dop=list([[20.0,0.0,30.0],[0.0,20.0,30.0],[20.0,20.0,30.0],[0.0,0.0,30.0]])
#####################################
######## ЦИКЛ ПО СЕТОЧКЕ ############
#####################################
#цикл для первой станции
for xi1 in np.arange(begx,endx+0.00000001,zone_stepx):
    stations[0][0]=xi1
    for yi1 in np.arange(begy,endy+0.00000001,zone_stepy):
        if(not in_poligon(geometry,[xi1,yi1])): continue
        stations[0][1]=yi1
        #цикл для второй станции
        for xi2 in np.arange(begx,endx+0.00000001,zone_stepx):
            stations[1][0]=xi2
            for yi2 in np.arange(begy,endy+0.00000001,zone_stepy):
                stations[1][1]=yi2
                #если расстояние между станциями 1 и 2 меньше минимума то пропускаем итерацию
                if((np.abs(stations[0][0]-stations[1][0])**2+np.abs(stations[0][1]-stations[1][1])**2)<=(min_disty**2+min_distx**2)): continue
                if(not in_poligon(geometry,[xi2,yi2])): continue
                #цикл для третей станции
                for xi3 in np.arange(begx,endx+0.00000001,zone_stepx):
                    stations[2][0]=xi3
                    for yi3 in np.arange(begy,endy+0.00000001,zone_stepy):
                        stations[2][1]=yi3
                        if((np.abs(stations[1][0]-stations[2][0])**2+np.abs(stations[1][1]-stations[2][1])**2)<=(min_disty**2+min_distx**2)): continue
                        if((np.abs(stations[0][0]-stations[2][0])**2+np.abs(stations[0][1]-stations[2][1])**2)<=(min_disty**2+min_distx**2)): continue
                        if(not in_poligon(geometry,[xi3,yi3])): continue
                        #цикл для четвертой станции
                        for xi4 in np.arange(begx,endx+0.00000001,zone_stepx):
                            stations[3][0]=xi4
                            j4=0
                            for yi4 in np.arange(begy,+0.00000001,zone_stepy):
                                stations[3][1]=yi4
                                if((np.abs(stations[0][0]-stations[3][0])**2+np.abs(stations[0][1]-stations[3][1])**2)<=(min_disty**2+min_distx**2)): continue
                                if((np.abs(stations[1][0]-stations[3][0])**2+np.abs(stations[1][1]-stations[3][1])**2)<=(min_disty**2+min_distx**2)): continue
                                if((np.abs(stations[2][0]-stations[3][0])**2+np.abs(stations[2][1]-stations[3][1])**2)<=(min_disty**2+min_distx**2)): continue
                                if (collinear(stations[0],stations[1],stations[2])<min_coll): continue
                                if (collinear(stations[0],stations[1],stations[3])<min_coll): continue
                                if (collinear(stations[0],stations[3],stations[2])<min_coll): continue
                                if (collinear(stations[3],stations[1],stations[2])<min_coll): continue
                                if(not in_poligon(geometry,[xi4,yi4])): continue
                                counter+=1
                                m_dop=dop_of_polygone(stations,geometry,begx,begy,endx,endy)
                                #print(counter) 
                                if m_dop<min_dop:
                                    #print(counter) 
                                    min_dop=m_dop
                                    station_min_dop.clear
                                    station_min_dop=copy.deepcopy(stations)

print(counter)
print("Минимальный DOP:  ",min_dop)
print("Координаты станций \n",np.array(station_min_dop))

now = datetime.now()
print("Время окончания:  ", now)
