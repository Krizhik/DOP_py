num_st=int(input("Введите количество станций"))
zonе_height=input("Высота зоны")
zone_widtch=input("ширина зоны")
stations = []
#ввод координат станций
''' dssddsdsdsdsdcsdcsdc'''
for i in range(0,num_st):
    st=[0, 0, 0]
    st[0]=float(input("X"))
    st[1]=float(input("Y"))
    st[2]=float(input("Z"))
    stations.append(st)
print(stations)   