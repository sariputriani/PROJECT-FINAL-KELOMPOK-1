import mysql.connector

def buat_koneksi():
    connection = mysql.connector.connect(
        user = "root",
        password = "",
        database = "Kelompok1"
    )
    cursor = connection.cursor()
    return connection, cursor