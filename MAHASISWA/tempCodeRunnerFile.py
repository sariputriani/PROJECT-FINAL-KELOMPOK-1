import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QToolBar,
    QSizePolicy
)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
basedir = os.path.dirname(__file__)

class HalamanMahasiswa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mahasiswa")
        self.setFixedSize(600,400)

        # Layout dan Widget
        self.layoutMHS = QVBoxLayout()
        # self.judul = QLabel("SELAMAT DATANG MAHASISWA")
        # self.judul.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        # self.judul.setAlignment(Qt.AlignCenter)
        
        # Menambahkan widget ke layout
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar)

        dataMHS = QAction("Dashboard", self)
        dataMHS.setCheckable(True)
        self.toolbar.addAction(dataMHS)

        spasi = QWidget()
        spasi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spasi)

        # Tambahkan action Data User di sebelah kanan
        datauser = QAction(
            QIcon(os.path.join(basedir, "user-female.png")),
            "User",self
        )
        # datauser.triggered.connect(self.show_datauser)
        self.toolbar.addAction(datauser)
        langout = QAction(
            QIcon(os.path.join(basedir, "application-dock.png")),
            "Langout",self
        )
        
        # Mengatur layout untuk widget utama
        self.setLayout(self.layoutMHS)


def apply_stylesheet(app, path):
    with open(path, "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)
# Muat stylesheet
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet_path = "./style.qss"
    apply_stylesheet(app, stylesheet_path)

    window = HalamanMahasiswa()
    window.show()
    sys.exit(app.exec())