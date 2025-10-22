import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vashu@Tyagi",
    database="employee_management_system"
)

cursor = conn.cursor()
cursor.close() 