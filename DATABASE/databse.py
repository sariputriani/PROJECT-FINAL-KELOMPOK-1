import mysql.connector

def buat_koneksi():
    con = mysql.connector.connect(
        username = "root",
        password = "",
        database = "tugas_jadwal",
    )
    curse = con.cursor()
    return con,curse