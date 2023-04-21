import math
import time
from math import *

import pyrebase

l = 30
E = 2 * pow(10, 8)  # đơn vị là kPa ₫> đơn vị của lực sau khi tính sẽ là kN.
A = 1.131 * pow(10, -4)  # đã đổi sang m^2

firebaseConfig = {
    'apiKey': "AIzaSyCpC7eefwjoJC0q5ed_pAdl_Hls_RhPML0",
    'authDomain': "busitech-5c6b5.firebaseapp.com",
    'projectId': "busitech-5c6b5",
    'databaseURL': "https://busitech-5c6b5-default-rtdb.asia-southeast1.firebasedatabase.app",
    'storageBucket': "busitech-5c6b5.appspot.com",
    'messagingSenderId': "903998547050",
    'appId': "1:903998547050:web:46b0ae7420ca80cfd15613",
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()


def downloadData():
    # while True:
    toado_x = db.child("COT1").child("Angle").child("X").get()
    toado_y = db.child("COT1").child("Angle").child("Y").get()
    toado_z = db.child("COT1").child("Angle").child("Z").get()
    vanToc = db.child("COT1").child("SPEED").get()
    huongGio = db.child("COT1").child("DIRECTION").get()

    x0 = toado_x.val()
    y0 = toado_y.val()
    z0 = toado_z.val()
    v = vanToc.val()
    t0 = huongGio.val()

    x_rad = abs( ((x0)) / 180 * math.pi)
    y_rad = abs(((y0)) / 180 * math.pi)
    z_rad = abs(((z0)) / 180 * math.pi)

    x1 = l * (sin(z_rad) * sin(x_rad) + cos(z_rad) * cos(y_rad) * cos(x_rad))
    y1 = l * (sin(z_rad) * sin(y_rad) * cos(x_rad) - cos(z_rad) * cos(x_rad))
    z1 = l * cos(y_rad) * cos(x_rad)

    x = ((l - abs(x1)) * 100)
    y = ((l - abs(y1)) * 100)
    z = (l - abs(z1)) * 100
    # print(x,y,z)

    if ((t0 >= 0 and t0 < 2.25) or (t0 >= 33.75 and t0 <= 36.0)):
        t = 'Bắc'  # hướng bắc
    elif (t0 >= 2.25 and t0 < 6.75):
        t = 'Đông Bắc'  # hướng đông bắc
    elif (t0 >= 6.75 and t0 < 11.25):
        t = 'Đông'  # hướng đông
    elif (t0 >= 11.25 and t0 < 15.75):
        t = 'Đông Nam'  # hướng đông nam
    elif (t0 >= 15.75 and t0 < 20.25):
        t = 'Nam'  # hướng nam
    elif (t0 >= 20.25 and t0 < 24.75):
        t = 'Tây Nam'  # hướng tây nam
    elif (t0 >= 24.75 and t0 < 29.25):
        t = 'Tây'  # hướng tây
    else:
        t = 'Tây Bắc'  # hướng tây bắc

    return round(x, 3), round(y, 3), round(z, 3), round(v, 3), t


def downloadDataElse():
    Acc1 = db.child("COT1").child("Acc").child("X").get()
    Acc2 = db.child("COT1").child("Acc").child("Y").get()
    Acc3 = db.child("COT1").child("Acc").child("Z").get()

    Gyro1 = db.child("COT1").child("Gyro").child("X").get()
    Gyro2 = db.child("COT1").child("Gyro").child("Y").get()
    Gyro3 = db.child("COT1").child("Gyro").child("Z").get()

    # Acc1 = Acc1.val() / 32768 * 16
    # Acc2 = Acc2.val() / 32768 * 16
    # Acc3 = Acc3.val() / 32768 * 16
    # Gyro1 = Gyro1.val() / 32768 * 2000
    # Gyro2 = Gyro2.val() / 32768 * 2000
    # Gyro3 = Gyro3.val() / 32768 * 2000

    Acc1 = Acc1.val()
    Acc2 = Acc2.val()
    Acc3 = Acc3.val()
    Gyro1 = Gyro1.val()
    Gyro2 = Gyro2.val()
    Gyro3 = Gyro3.val()

    return round(Acc1, 3), round(Acc2, 3), round(Acc3, 3), round(Gyro1, 3), round(Gyro2, 3), round(Gyro3, 3)


def calculator():
    x, y, z, v, t = downloadData()
    if (v == 0):
        Nz1 = Nz2 = Nz3 = Nz4 = Nz5 = Nz6 = Nz7 = Nz8 = Nz9 = 0
    # cần phải xác định được lực dựa vào tốc độ gió
    v1 = 1.5 * pow(10, -5)
    Re = (v * 0.06) / v1
    if Re == 0:
        Re = 60
    Cd = 0.7 + pow((14 / Re), 0.25)
    q = 0.5 * 1.225 * v * v
    Fc1 = (Cd * q * pi * 0.06 * 30) / 10  # do gió tác dụng phân bố không đều => tìm độ lớn lực theo độ cao
    Fc2 = (Cd * q * pi * 0.06 * 30) / 10
    Fc3 = (Cd * q * pi * 0.06 * 30) / 10

    # Góc giữa dây co và cột BTS
    anpha0 = math.atan(5 / (l - 3))
    anpha01 = math.atan(5 / (l - 9))
    anpha02 = math.atan(5 / (l - 15))

    # góc giữa lực trên mặt cắt ngang so với lực kéo dây co
    beta = math.pi / 2 - anpha0
    beta1 = math.pi / 2 - anpha01
    beta2 = math.pi / 2 - anpha02

    # tính góc của lực do gió tác dụng
    if t == 'Bắc':
        anpha = 0
        anpha1 = math.pi / 3
        anpha2 = math.pi / 3
    if t == 'Đông Bắc':
        anpha = math.pi / 4
        anpha1 = math.pi / 12
        anpha2 = math.pi * 7 / 12
    if t == 'Đông':
        anpha = math.pi / 2
        anpha1 = -math.pi / 6
        anpha2 = math.pi * 5 / 6
    if t == 'Đông Nam':
        anpha = math.pi * 3 / 4
        anpha1 = -math.pi * 5 / 12
        anpha2 = math.pi * 13 / 12
    if t == 'Nam':
        anpha = math.pi
        anpha1 = -math.pi * 2 / 3
        anpha2 = math.pi * 4 / 3
    if t == 'Tây Nam':
        anpha = math.pi * 5 / 4
        anpha1 = -math.pi * 11 / 12
        anpha2 = math.pi * 19 / 12
    if t == 'Tây':
        anpha = math.pi * 3 / 2
        anpha1 = -math.pi * 7 / 6
        anpha2 = math.pi * 11 / 6
    if t == 'Tây Bắc':
        anpha = math.pi * 7 / 4
        anpha1 = -math.pi * 17 / 12
        anpha2 = math.pi * 25 / 12

    # tính lực hướng vào trọng tâm của cột vị trí cao nhất
    F1 = Fc1 * cos(anpha)
    F2 = Fc1 * cos(anpha1)
    F3 = Fc1 * cos(anpha2)
    # print(F1)

    # lực tác dụng lên cột ở vị trí cao thứ 2
    F4 = Fc2 * cos(anpha)
    F5 = Fc2 * cos(anpha1)
    F6 = Fc2 * cos(anpha2)
    # print(F5)

    # lực tác dụng lên cột ở vị trí cao thứ 3
    F7 = Fc3 * cos(anpha)
    F8 = Fc3 * cos(anpha1)
    F9 = Fc3 * cos(anpha2)
    # print(F9)

    # lực kéo đúng tâm với dây co ở đoạn cao nhất
    Nz1 = F1 * cos(beta)
    Nz2 = F2 * cos(beta)
    Nz3 = F3 * cos(beta)

    # lực kéo đúng tâm với dây co ở đoạn cao thứ 2
    Nz4 = F4 * cos(beta1)
    Nz5 = F5 * cos(beta1)
    Nz6 = F6 * cos(beta1)

    # lực kéo đúng tâm với dây co ở đoạn cao thứ 3
    Nz7 = F7 * cos(beta2)
    Nz8 = F8 * cos(beta2)
    Nz9 = F9 * cos(beta2)

    F = []
    # print(Nz1, Nz2, Nz3)
    F = [abs(round(Nz1, 2)), abs(round(Nz2, 2)), abs(round(Nz3, 2)), abs(round(Nz4, 2)), abs(round(Nz5, 2)),
         abs(round(Nz6, 2)), abs(round(Nz7, 2)), abs(round(Nz8, 2)), abs(round(Nz9, 2))]

    return F


def calculatorv():
    x, y, z, v, t = downloadData()
    statuscap = 0
    if (v >= 0.5 and v <= 1.5):
        statuscap = 1
    if (v >= 1.6 and v <= 3.3):
        statuscap = 2
    if (v >= 3.4 and v <= 5.5):
        statuscap = 3
    if (v >= 5.6 and v <= 7.9):
        statuscap = 4
    if (v >= 8 and v <= 10.7):
        statuscap = 5
    if (v >= 10.8 and v <= 13.8):
        statuscap = 6
    if (v >= 13.9 and v <= 17.1):
        statuscap = 7
    if (v >= 17.2 and v <= 20.7):
        statuscap = 8
    if (v >= 20.8 and v <= 24.4):
        statuscap = 9
    if (v >= 24.5 and v <= 28.4):
        statuscap = 10
    if (v >= 28.5 and v <= 32.6):
        statuscap = 11
    if (v >= 32.7):
        statuscap = 12
    return statuscap


def calculatorDegree():
    x, y, z, v, t = downloadData()
    canh = sqrt((x / 100) * (x / 100) + (y / 100) * (y / 100))
    goc0 = asin(canh / l)
    goc = goc0 / pi * 180
    return round(goc, 5)


def calculatorWarn():
    x, y, z, v, t = downloadData()
    F1, F2, F3, F4, F5, F6, F7, F8, F9 = calculator()
    gocnghieng = calculatorDegree()
    status1 = 'Normal'
    statusNum = 0
    if (((F1 >= 80) or (F2 >= 80) or (F3 >= 80) or (F4 >= 80) or (F5 >= 80) or (F6 >= 80) or (F7 >= 80) or (
            F8 >= 80) or (
                 F9 >= 80)) or gocnghieng > 0.65):
        status1 = 'Mức 2'
        statusNum = 2
    elif (((F1 >= 50 and F1 < 80) or (F2 >= 50 and F2 < 80) or (F3 >= 50 and F3 < 80) or (F4 >= 50 and F4 < 80) or (
            F5 >= 50 and F5 < 80) or (F6 >= 50 and F6 < 80) or (F7 >= 50 and F7 < 80) or (F8 >= 50 and F8 < 80) or (
                   F9 >= 50 and F9 < 80)) or ( gocnghieng >= 0,65 and gocnghieng <= 0.3)):
        status1 = 'Mức 1'
        statusNum = 1
    # elif (((F1 >= 40 and F1 < 60) or (F2 >= 40 and F2 < 60) or (F3 >= 40 and F3 < 60) or (F4 >= 40 and F4 < 60) or (
    #         F5 >= 40 and F5 < 60) or (F6 >= 40 and F6 < 60) or (F7 >= 40 and F7 < 60) or (F8 >= 40 and F8 < 60) or (
    #                F9 >= 40 and F9 < 60)) or (
    #               gocnghieng >= 2 and gocnghieng <= 4)):
    #     status1 = 'Mức 1'
    #     statusNum = 1
    else:
        status1 = 'Normal'
        statusNum = 0
    return status1, statusNum



# while True:
#     F = calculator()
#     print(F[0], F[1], F[2], F[3], F[4], F[5], F[6], F[7], F[8])
#     F1, F2, F3, F4, F5, F6, F7, F8, F9 = calculator()
#     status = calculatorWarn()
#     goc = calculatorDegree()
#     print(status)
#     print(F1, F2, F3, F4, F5, F6, F7, F8, F9)
#     print(goc)
#     time.sleep(5)
# print(datetime.datetime.now())
