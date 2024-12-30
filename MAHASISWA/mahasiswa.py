import sys
import os
import re
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
    QMessageBox,
    QTableWidget,
    QFrame,
    QCalendarWidget,
    QTableWidgetItem,
    QPlainTextEdit

)
from PySide6.QtCore import QSize, Qt,QDate
from PySide6.QtGui import QAction, QIcon,QPixmap

# import modlu
from DATABASE.databse import buat_koneksi
basedir = os.path.dirname(__file__)

class HalamanMahasiswa(QMainWindow):
    def __init__(self,username):
        super().__init__()
        self.username = username  # Simpan username
        self.setWindowTitle(f"Selamat Datang, {self.username}")
        self.setFixedSize(600,500)
        self.styleqss()

        # Layout dan Widget
        self.layoutMHS = QVBoxLayout()
        self.judul = QLabel("SELAMAT DATANG MAHASISWA")
        self.judul.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        self.judul.setAlignment(Qt.AlignCenter)
        self.layoutMHS.addWidget(self.judul)
        
        # Menambahkan widget ke layout
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar)

        dataMHS = QAction("Dashboard", self)
        dataMHS.setCheckable(True)
        self.toolbar.addAction(dataMHS)
        dataMHS.triggered.connect(self.Dashboard)

        jadwal = QAction("Jadwal", self)
        jadwal.setCheckable(True)
        self.toolbar.addAction(jadwal)
        jadwal.triggered.connect(self.DashboardJadwal)

        spasi = QWidget()
        spasi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spasi)

        # Tambahkan action Data User di sebelah kanan
        datauser = QAction(
            QIcon(os.path.join(basedir, "./gambarMahasiswa/userhh.png")),
            "User",self
        )
        datauser.triggered.connect(self.halamanDataUser)
        self.toolbar.addAction(datauser)

        setting = QAction(QIcon(os.path.join(basedir,"../DOSEN/image.png")),"Setting",self)
        setting.triggered.connect(self.halamanSetting)
        self.toolbar.addAction(setting)

        # toolbar langout
        langout = QAction(
            QIcon(os.path.join(basedir, "./gambarMahasiswa/langout.png")),
            "Langout",self
        )
        self.toolbar.addAction(langout)
        langout.triggered.connect(self.show_langout)
        
        # Mengatur layout untuk widget utama
        self.setLayout(self.layoutMHS)

    def styleqss(self):
        qss_file = os.path.join(basedir, "./mahasiswa.qss")
        if os.path.exists(qss_file):
            with open(qss_file, "r") as file:
                qss = file.read()
                QApplication.instance().setStyleSheet(qss)
    
    def halamanDataUser(self):
        self.showDataUser = DataUser(self.username)
        self.showDataUser.show()

    def halamanSetting(self):
         self.showSetting = HalamanSetting()
         self.showSetting.show()

    def show_langout(self):
        masseg = QMessageBox.question(self, "Konfirmasi", 
                "Apakah anda yakin ingin keluar dari aplikasi?", QMessageBox.Yes | QMessageBox.No)
        if masseg == QMessageBox.Yes:
                    self.close()
                    print("aplikasi di close")

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
        self.btnViewJadwal.setIconSize(QSize(20,20))
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
        self.daftarTugas.setColumnCount(8)
        self.daftarTugas.setHorizontalHeaderLabels(["No Tugas","Id mk", "Hari", "Deskripsi Tugas", "Tanggal Pemberian","Tanggal Pengumpulan","Waktu","Action"])
        self.daftarTugas.horizontalHeader().setStretchLastSection(True)
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

    def jadwal(self):
        # menghubungkan ke databases
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT 
                    Jadwal.Hari,
                    Jadwal.Jam,
                    Ruang.Nama_Ruang,
                    MataKuliah.Nama_MK,
                    Dosen.Nama_Dosen,
                    MataKuliah.SKS
                FROM 
                    Jadwal
                INNER JOIN 
                    MataKuliah ON Jadwal.ID_MK = MataKuliah.ID_MK
                INNER JOIN 
                    Dosen ON Jadwal.ID_Dosen = Dosen.ID_Dosen
                INNER JOIN 
                    Ruang ON Jadwal.ID_Ruang = Ruang.ID_Ruang;
            """
        curse.execute(query)
        # ambil data semua pada table jadwal
        ambildata = curse.fetchall()

        # mengambil data untuk diisi kedalam table jadwal
        self.daftarJadwal.setRowCount(len(ambildata))
        for barisnumber, barisData in enumerate(ambildata):   
                for col,data in enumerate(barisData):
                    self.daftarJadwal.setItem(barisnumber, col, QTableWidgetItem(str(data)))
        # merapikan table
        self.daftarJadwal.resizeColumnsToContents()
    
    def tugas(self):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT 
                    tugas.ID_Tugas,
                    tugas.ID_mk,
                    Jadwal.Hari,
                    tugas.Deskripsi_Tugas,
                    tugas.Tanggal_Pemberian,
                    tugas.Tanggal_Pengumpulan,
                    (abs(day(tanggal_pemberian) - (day(tanggal_pengumpulan)))),
                    MataKuliah.Nama_MK
                FROM 
                    Tugas
                INNER JOIN 
                    Jadwal ON Tugas.ID_Jadwal = Jadwal.ID_Jadwal
                INNER JOIN 
                    MataKuliah ON Jadwal.ID_MK = MataKuliah.ID_MK
            """
        
        curse.execute(query)
        # ambil data semua pada table jadwal
        ambildata = curse.fetchall()

        # mengambil data untuk diisi kedalam table jadwal
        self.daftarTugas.setRowCount(len(ambildata))
        for barisnumber, barisData in enumerate(ambildata):
                for col,data in enumerate(barisData):
                    self.daftarTugas.setItem(barisnumber, col, QTableWidgetItem(str(data)))
                self.button = QPushButton("Kumpulkan")
                self.button.clicked.connect(self.kumpulkan)
                self.button.setProperty("row",barisnumber)
                self.daftarTugas.setCellWidget(barisnumber, 7, self.button)
        self.daftarTugas.resizeColumnsToContents() 

    def kumpulkan(self):
        self.ShowHalamanKumpulkanTugas = HalamanKumpulkanTugas(self.username)
        self.ShowHalamanKumpulkanTugas.show()

    def apply_filter(self):
        filter_text = self.search.text().lower()  # Ambil teks pencarian dan ubah menjadi huruf kecil
        for row in range(self.daftarTugas.rowCount()):  # Loop setiap baris di tabel
            found = False  # Variabel untuk mengecek apakah teks ditemukan
            for col in range(self.daftarTugas.columnCount()):  # Loop setiap kolom di baris
                item = self.daftarTugas.item(row, col)  # Ambil item di posisi (row, col)
                if item and filter_text in item.text().lower():  # Cek apakah teks pencarian ada di item
                    found = True  # Jika ada, set found = True
                    break  # Tidak perlu cek kolom lainnya
            self.daftarTugas.setRowHidden(row, not found)  # Sembunyikan baris jika teks tidak ditemukan

    def pengingat(self):
        connection,curse = buat_koneksi()
        curse = connection.cursor()

        # Query untuk mengambil data deadline
        query = "SELECT * FROM tugas"
        curse.execute(query)
        ambildata = curse.fetchall()

        # ini mengambil tanggal hari ini
        hariIni = QDate.currentDate()

        for  data in ambildata:
            # ambildata di kolom 1
            namajudul = data[1]
            # ambil data dikolom 2 dengan format tanggal
            tanggalDeadline = data[4].strftime("%Y-%m-%d %H:%M:%S")
            
            # Konversi ke QDate
            formatDeadline = QDate.fromString(tanggalDeadline, "yyyy-MM-dd HH:mm:ss")  
            # hitung sisa hari hingga deadline
            sisaHari = hariIni.daysTo(formatDeadline)  # Hitung sisa hari hingga deadline

            # memeriksa sisahari jika sisahari lebihkecil dari 3
            if sisaHari <= 3:
                pesan = f"Tugas '{namajudul}' akan jatuh tempo dalam {sisaHari} hari, yaitu pada {formatDeadline.toString('dd MMMM yyyy HH:mm:ss')}."
                QMessageBox.information(self, "Pengingat Deadline", pesan)

                # jika sisaHari mendekati deadline
                if sisaHari > 0:  
                    pesan = f"Tugas '{namajudul}' akan jatuh tempo dalam {sisaHari} hari, yaitu pada {formatDeadline.toString('dd MMMM yyyy HH:mm:ss')}."
                    QMessageBox.information(self, "Pengingat Deadline", pesan)
                
                # Deadline hari ini
                elif sisaHari == 0:  
                    pesan = f"Tugas '{namajudul}' harus diselesaikan hari ini ({formatDeadline.toString('dd MMMM yyyy HH:mm:ss')})!"
                    QMessageBox.warning(self, "Deadline Hari Ini", pesan)

                # Deadline sudah lewat
                else:  
                    pesan = f"Tugas '{namajudul}' sudah melewati deadline pada {formatDeadline.toString('dd MMMM yyyy HH:mm:ss')}!"
                    QMessageBox.warning(self, "Deadline Terlewat", pesan)
                    self.button.setStyleSheet("background-color: white")


class DataUser(QWidget):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle("Data User")
        self.setFixedSize(350,350)
        self.setStyleSheet("""
            background-color:rgb(235, 241, 243);
            font-family:Poppins;
            font-weight:bold;
            font-size:15px;
                           """)

        container = QWidget()
        layout = QVBoxLayout()
        
        lbFoto = QLabel()
        pixmap = QPixmap(os.path.join(basedir, "./gambarMahasiswa/13.png"))
        lbFoto.setPixmap(pixmap)
        
        lbFoto.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbFoto)

        # nim
        self.lb2Nim = QLabel("")
        self.lb2Nim.setObjectName("nim")
        
        # nama
        self.lb2Nama = QLabel("")
        self.lb2Nama.setObjectName("nama")
        
        # menambahakan jurusan
        self.lb2Jurusan = QLabel("")
        self.lb2Jurusan.setObjectName("jurusan")

        # menambahkaan prodi
        self.lb2Prodi = QLabel("")
        self.lb2Prodi.setObjectName("prodi")

        # menmbhkan smester
        self.lb2Semester = QLabel("")
        self.lb2Semester.setObjectName("semester")

        # menambhakn widget kedalam layout 
        layout.addWidget(self.lb2Nim)
        layout.addWidget(self.lb2Nama)
        layout.addWidget(self.lb2Jurusan)
        layout.addWidget(self.lb2Prodi)
        layout.addWidget(self.lb2Semester)

        # setlayout (layout) kedalam container
        container.setLayout(layout)

        layout.addStretch()
        self.setLayout(layout)
        self.ambil_dataUser(username)
    
    def ambil_dataUser(self,username):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT datamahasiswa.nim , datamahasiswa.nama, datamahasiswa.jurusan, datamahasiswa.prodi , datamahasiswa.semester
                FROM datamahasiswa 
                JOIN loginmahasiswa 
                ON datamahasiswa.nim = loginmahasiswa.username 
                WHERE loginmahasiswa.username = %s;
            """
        
        curse.execute(query,(username,))

        # menampilkan usrname di consle
        print(username)

        ambildata = curse.fetchone()
        if ambildata:
                nim,nama,jurusan,prodi,semester = ambildata
                self.lb2Nim.setText(f'Nim            : {nim}')
                self.lb2Nama.setText(f'Nama         : {nama}')
                self.lb2Jurusan.setText(f'Jurusan     : {jurusan}')
                self.lb2Prodi.setText(f'Prodi          : {prodi}')
                self.lb2Semester.setText(f'Semester  : {semester}')
        else:
                self.lb2Nim.setText(f"Data Tidak ditemukan")
                self.lb2Nama.setText("Data Tidak ditemukan")
                self.lb2Jurusan.setText("Data Tidak ditemukan")
                self.lb2Prodi.setText("Data Tidak ditemukan")
                self.lb2Semester.setText("Data Tidak ditemukan")


class HalamanSetting(QWidget):
    def __init__(self):
        super().__init__()


class HalamanKumpulkanTugas(QWidget):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle("Kumpulkan Tugas")
        self.setFixedSize(450,450)

        layout = QVBoxLayout()

        # membuat kontent
        self.id_tugas = QLabel("h")
        self.mataKuliah = QLabel("")
        self.judulTugas = QLabel("h")
        self.tanggalPemberian = QLabel("h")
        self.tanggalDeadline = QLabel("h")
        self.FileTugas = QPlainTextEdit()
        
        # menambahkan ke layout
        layout.addWidget(self.id_tugas)
        layout.addWidget(self.mataKuliah)
        layout.addWidget(self.judulTugas)
        layout.addWidget(self.tanggalPemberian)
        layout.addWidget(self.tanggalDeadline)
        layout.addWidget(self.FileTugas)

        # mengsetlayout
        self.setLayout(layout)
        self.ambilDataTugas(username)
    
    def ambilDataTugas(self,username):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT tugas.id_tugas, tugas.id_mk, tugas.deskripsi_tugas, tugas.tanggal_pemberian, tugas.tanggal_pengumpulan
                FROM tugas
                JOIN matakuliah ON matakuliah.id_mk = tugas.id_mk
                JOIN loginmahasiswa ON loginmahasiswa.username = %s
                WHERE loginmahasiswa.username = %s;
            """
        
        curse.execute(query,(username,username))

        # menampilkan usrname di consle
        print(username)

        ambildata = curse.fetchone()
        if ambildata:
                id_tugas,id_mk,deskripsi_tugas,tanggal_pemberian,tanggal_pengumpulan = ambildata
                self.id_tugas.setText(f'id Tugas            : {id_tugas}')
                self.mataKuliah.setText(f'MataKuliah         : {id_mk}')
                self.judulTugas.setText(f'judul tugas     : {deskripsi_tugas}')
                self.tanggalPemberian.setText(f'tanggal pemberian          : {tanggal_pemberian}')
                self.tanggalDeadline.setText(f'deadline  : {tanggal_pengumpulan}')
                # self.lb2Semester.setText(f'Semester  : {tanggal_pen}')

        