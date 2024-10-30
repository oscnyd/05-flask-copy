import sqlite3

conn = sqlite3.connect("database.db")
print("opened db with sucess")

conn.execute("CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)")
print("table created sucessfully")

conn.close()