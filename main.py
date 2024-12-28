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
# from MAHASISWA.mahasiswa import HalamanMahasiswa
from PySide6.QtSql import QSqlDatabase,QSqlTableModel

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from MAHASISWA.mahasiswa import HalamanMahasiswa
basedir = os.path.dirname(__file__)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # menentukan databases
        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(os.path.join(basedir,"./manajemen.sql"))
        self.db.open()

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
        self.username.setFixedSize(270,85)
        self.username.setPlaceholderText("username")
        self.username.setStyleSheet("""
        QLineEdit{
            font-family : "Cabliri";
            font-size : 14px;
            margin : 30,20,5;
            border: 2px solid #125370;
            border-radius: 5px;
            padding: 5px;                       
        }                                    
""")
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
        self.password.setFixedSize(270,55)
        self.password.setPlaceholderText("password")
        self.password.setStyleSheet("""                      
        QLineEdit{
            font-family : "Cabliri";
            font-size : 14px;
            margin : 0,20,0;
            border: 2px solid #125370;
            border-radius: 5px;
            padding: 5px;              
        }     
""")
        layoutHPassword.addWidget(self.password)
        layout.addLayout(layoutHPassword)

        # button
        self.btnLogin = QPushButton("L O G I N")
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
   
    def periksaUser(self):
        username = self.username.text()
        password = self.password.text()

        if username == "sari" and password == "sari":
            QMessageBox.information(self, 'Berhasil', 'Berhasil!.')
            self.showMHS = HalamanMahasiswa()
            self.showMHS.show()
            self.close()
        else:
            QMessageBox.warning(self,"Eror","password dan username salah,tolong inputkan ulang")
            self.username.clear()
            self.password.clear()      
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())