import mysql.connector

def buat_koneksi():
    connection = mysql.connector.connect(
        host = "localhost",
        port = "3307",
        user = "root",
        password = "",
        database = "tugas_jadwal"
    )
    cursor = connection.cursor()
    return connection, cursor