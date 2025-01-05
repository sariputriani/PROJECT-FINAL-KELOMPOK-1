import sys
import os
from PySide6.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

# from MAHASISWA.mahasiswa import HalamanM  Mahasiswa
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon

# import dosen dan mahasiswa
from MAHASISWA.mahasiswa import HalamanMahasiswa
from DOSEN.dosen import HalamanDosen
from DATABASE.databse import buat_koneksi
basedir = os.path.dirname(__file__)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.connectDB()
        self.setShortcutEnabled(True)

        # start
        self.setWindowTitle("Login")
        self.setFixedSize(340,500)
        self.setStyleSheet("background-color:white")
        # end

        # pembuatan halaman login
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20,5,5,5)
        layout.setSpacing(10)

        # gambar
        iconLogin = QLabel()
        iconLogin.setPixmap(QIcon("./gambar/gambarlogin.jpg").pixmap(QSize(260, 260)))
        iconLogin.setAlignment(Qt.AlignCenter)
        layout.addWidget(iconLogin)
        
        # start username
        # layout h username
        layoutHUser = QHBoxLayout()
        lbUser = QLabel()
        lbUser.setPixmap(QIcon("./gambar/userhh.png").pixmap(QSize(25, 25)))
        lbUser.setStyleSheet("margin: 30,20,0")
        layoutHUser.addWidget(lbUser)

        self.username = QLineEdit()
        # self.username.setObjectName("username")
        self.username.setStyleSheet("""
            font-family : "Cabliri";
            font-size : 14px;
            margin : 30,20,5;
            border: 2px solid #125370;
            border-radius: 5px;
            padding: 5px; 
""")
        self.username.setFixedSize(270,85)
        self.username.setPlaceholderText("username")
        layoutHUser.addWidget(self.username)
        layout.addLayout(layoutHUser)

        # start password
        # layout h password
        layoutHPassword = QHBoxLayout()
        lbPw = QLabel()
        lbPw.setPixmap(QIcon("./gambar/iconpw.png").pixmap(QSize(25, 25)))
        lbPw.setStyleSheet("margin:0,20,0")
        layoutHPassword.addWidget(lbPw)

        self.password = QLineEdit()
        # self.password.setObjectName("password")
        self.password.setStyleSheet("""
        font-family : "Cabliri";
        font-size : 14px;
            margin : 0,20,0;
            border: 2px solid #125370;
            border-radius: 5px;
            padding: 5px;

""")
        self.password.setFixedSize(270,55)
        self.password.setPlaceholderText("password")
        layoutHPassword.addWidget(self.password)
        layout.addLayout(layoutHPassword)

        # button
        self.btnLogin = QPushButton("L O G I N")
        self.btnLogin.setObjectName("btnlogin")
        self.btnLogin.setFixedSize(309,45)
        self.btnLogin.setStyleSheet("""
        QPushButton{
        background-color: #6AE0E8;
        border-radius:10px;
        margin-top:10px;                            
            }
        QPushButton::pressed{
            background-color: white;
            }
        
""")    
        self.btnLogin.clicked.connect(self.periksaUser)
        layout.addWidget(self.btnLogin)
        layout.addStretch()
        layoutHUser.addStretch()
        layoutHPassword.addStretch()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    # ini periksa user
    def periksaUser(self):
        username = self.username.text()
        password = self.password.text()

        # menghubungkan ke databases
        connection,curse = buat_koneksi()
        curse = connection.cursor()

        # mahasiswa
        queryMahasiswa = 'select * from loginmahasiswa where username = %s AND password = %s'
        curse.execute(queryMahasiswa, (username,password)) 
             
        resultMahasiswa = curse.fetchall()
        if resultMahasiswa:
            print("Mahasiswa ditemukan")
            self.showMHS = HalamanMahasiswa(username)
            self.showMHS.show()
            self.close()
            return
        
        # dosen
        queryDosen = 'select * from logindosen where username = %s AND password = %s'
        curse.execute(queryDosen,(username,password))
        resultDosen = curse.fetchall()
        if resultDosen: 
            print("Dosen ditemukan")
            self.showDSN = HalamanDosen(username)
            self.showDSN.show()
            self.close()
        else:
            print("Username tidak ditemukan")
            QMessageBox.warning(self, "Login Gagal", "password salah!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())