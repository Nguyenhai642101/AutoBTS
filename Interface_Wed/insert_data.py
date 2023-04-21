import time
from flask import *
import sqlite3
from download_data_from_firebase import *


def logData(x, y, z, v, t, capgio, gocnghieng, acc1, acc2, acc3, gyro1, gyro2, gyro3, F1, F2, F3,
            F4, F5, F6, F7, F8, F9, status):
    conn = sqlite3.connect("data.db")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO data VALUES(datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
            " ?, ?, ?, ?, ?, ?, ?, ?)",
            (x, y, z, v, t, capgio, gocnghieng, acc1, acc2, acc3, gyro1, gyro2, gyro3, F1, F2, F3,
             F4, F5, F6, F7, F8, F9, status))
        conn.commit()
    except:
        print("Error")
    conn.close()


def insert_data_sql():
    # i = 0
    # print(i)
    x, y, z, v, huonggio = downloadData()
    acc1, acc2, acc3, gyro1, gyro2, gyro3 = downloadDataElse()
    F = calculator()
    status1, statusNum = calculatorWarn()
    capgio = calculatorv()
    gocnghieng = calculatorDegree()
    logData(x, y, z, v, huonggio, capgio, gocnghieng, acc1, acc2, acc3, gyro1, gyro2, gyro3, F[0], F[1], F[2], F[3], F[4], F[5], F[6], F[7], F[8], status1)
    # i = i + 1
