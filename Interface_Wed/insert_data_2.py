import time
from flask import *
import sqlite3
from downloadCOT2 import *


def logData(x, y, z, v, t, capgio, gocnghieng, acc1, acc2, acc3, gyro1, gyro2, gyro3, F1, F2, F3,
            F4, F5, F6, F7, F8, F9, status):
    conn = sqlite3.connect("data.db")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO data2 VALUES(datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
            " ?, ?, ?, ?, ?, ?, ?, ?)",
            (x, y, z, v, t, capgio, gocnghieng, acc1, acc2, acc3, gyro1, gyro2, gyro3, F1, F2, F3,
             F4, F5, F6, F7, F8, F9, status))
        conn.commit()
    except:
        print("Error")
    conn.close()


def insert_data_2():
    # i = 0
    # print(i)
    x, y, z, v, huonggio = downloadData2()
    acc1, acc2, acc3, gyro1, gyro2, gyro3 = downloadDataElse2()
    F = calculator2()
    status1, statusNum = calculatorWarn2()
    capgio = calculatorv2()
    gocnghieng = calculatorDegree2()
    logData(x, y, z, v, huonggio, capgio, gocnghieng, acc1, acc2, acc3, gyro1, gyro2, gyro3, F[0], F[1], F[2], F[3], F[4], F[5], F[6], F[7], F[8], status1)
    # i = i + 1
