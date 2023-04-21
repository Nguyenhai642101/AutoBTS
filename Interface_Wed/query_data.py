import sqlite3
conn=sqlite3.connect('data.db')
curs=conn.cursor()

print ("\nLast raw Data logged on database:\n")
for row in curs.execute("SELECT * FROM tables ORDER BY timestamp DESC LIMIT 1"):
    # timestamp la  cot dau tien trong table, luc tao table nen them cot tgian thuc vao cho de truy van
    print (str(row[0])+" ==> Goc nghieng = "+str(row[1])+"	trang thai = "+str(row[2]))