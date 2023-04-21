import sqlite3
conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS tables")
cur.execute("CREATE TABLE data2(timestamp DATETIME, x interger, y interger, z interger, v interger, t string,"
            " capgio interger, gocnghieng interger, acc1 interger, acc2 interger, acc3 interger,"
            "gyro1 interger, gyro2 interger, gyro3 interger, F1 interger, F2 interger, F3 interger,"
            "F4 interger, F5 interger, F6 interger, F7 interger, F8 interger, F9 interger, status string)")
conn.close()
