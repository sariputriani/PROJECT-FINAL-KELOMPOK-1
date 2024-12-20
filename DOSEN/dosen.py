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
    QVBoxLayout
)
from PySide6.QtCore import QSize, Qt
basedir = os.path.dirname(__file__)

class HalamanMahasiswa(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mahasiswa")
        self.setFixedSize(600,400)

        # Layout dan Widget
        self.layoutDS = QVBoxLayout()
        self.judul = QLabel("SELAMAT DATANG DOSEN")
        self.judul.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        self.judul.setAlignment(Qt.AlignCenter)
        
        # Menambahkan widget ke layout
        self.layoutDS.addWidget(self.judul)
        
        # Mengatur layout untuk widget utama
        self.setLayout(self.layoutDS)


app = QApplication(sys.argv)
Window = HalamanMahasiswa()
Window.show()
app.exec()