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
    QSizePolicy,
    QFrame,
    QDate,
    QTableWidget,
    QCalendarWidget,
    QMessageBox
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
        langout.triggered.connect(self.show_langout)
        
        # Mengatur layout untuk widget utama
        self.setLayout(self.layoutMHS)

    def Dashboard(self):
        container = QWidget()
        layoutDs = QVBoxLayout()
        
        # judul
        self.judul = QLabel("DASHBOARD")
        self.judul.setObjectName("lbJudul")        
        layoutDs.addWidget(self.judul)

        # membuat garis
        garis = QFrame()
        garis.setObjectName("line")
        garis.setFrameShape(QFrame.HLine)
        garis.setFrameShadow(QFrame.Sunken)
        layoutDs.addWidget(garis)

        layoutTanggal = QHBoxLayout()

        # Mengambil tanggal hari ini
        tangglHariIni = QDate.currentDate()
        # format tanggal
        format = tangglHariIni.toString("dddd dd - MMMM - yyyy")

        self.tanggal = QLabel(format)
        self.tanggal.setObjectName("lbTanggal")
        layoutTanggal.addWidget(self.tanggal)


        # Membuat tombol
        self.btnViewJadwal = QPushButton("  Jadwal")
        self.btnViewJadwal.setObjectName("btnViewJadwal")
        self.btnViewJadwal.setFixedSize(90, 30)

        # memberi icon di push button
        gambarMahasiswa_path = os.path.join(basedir, "gambarMahasiswa", "eyes.png")
        self.btnViewJadwal.setIcon(QIcon(gambarMahasiswa_path))
        self.btnViewJadwal.pressed.connect(self.DashboardJadwal)
        layoutTanggal.addWidget(self.btnViewJadwal)
        layoutDs.addLayout(layoutTanggal)

        # serch
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Here ...")
        self.search.setObjectName("search")
        self.search.textChanged.connect(self.apply_filter)
        layoutDs.addWidget(self.search)

        # table
        self.daftarTugas = QTableWidget()
        self.daftarTugas.setObjectName("daftarTugas")
        self.daftarTugas.horizontalHeader().setStretchLastSection(True)
        self.daftarTugas.setColumnCount(8)

        self.daftarTugas.setHorizontalHeaderLabels(["No Tugas","Hari", "Judul Tugas", "Tanggal Pemberian", "Deadline","Waktu","Mata Kuliah","Action"])
        layoutDs.addWidget(self.daftarTugas)
        
        # 
        layoutDs.addStretch()
        container.setLayout(layoutDs)
        self.setCentralWidget(container)
        self.tugas()
        # self.pesanPengingat()
        self.pengingat()
    
    def DashboardJadwal(self):
        container = QWidget()
        layoutDs = QVBoxLayout()
        
        self.judul = QLabel("Jadwal Overview")
        self.judul.setObjectName("lbJudul")        
        layoutDs.addWidget(self.judul)

        # membuat garis
        garis = QFrame()
        garis.setObjectName("line")
        garis.setFrameShape(QFrame.HLine)
        garis.setFrameShadow(QFrame.Sunken)
        layoutDs.addWidget(garis)

        # celender
        self.celender = QCalendarWidget()
        self.celender.setObjectName("tanggal")
        self.celender.setGridVisible(True)
        self.current_date = self.celender.selectedDate()  # Ambil tanggal default dari QCalendarWidget
        layoutDs.addWidget(self.celender)

        self.daftarJadwal = QTableWidget()
        self.daftarJadwal.setObjectName("daftarJadwal")
        self.daftarJadwal.horizontalHeader().setStretchLastSection(True)
        self.daftarJadwal.setColumnCount(6)
        self.daftarJadwal.setHorizontalHeaderLabels(["Hari","Jam/Waktu", "Nama Ruangan", "Mata Kuliah", "Nama Dosen","SKS"])
        layoutDs.addWidget(self.daftarJadwal)

        layoutDs.addStretch()
        container.setLayout(layoutDs)
        self.setCentralWidget(container)
        self.jadwal()

    def show_langout(self):
        masseg = QMessageBox.question(self, "Konfirmasi", 
                "Apakah anda yakin ingin keluar dari aplikasi?", QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No)
            
        if masseg == QMessageBox.Yes:
                    self.close()
                    print("aplikasi di close")

def apply_stylesheet(app, path):
    if os.path.exists(path):
        with open(path, "r") as file:
            qss = file.read()
            app.setStyleSheet(qss)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet_path = os.path.join(basedir, "./style.qss")
    apply_stylesheet(app, stylesheet_path)

    window = HalamanMahasiswa()
    window.show()
    sys.exit(app.exec())