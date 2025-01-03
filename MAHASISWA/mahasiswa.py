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
    QPlainTextEdit,
    QTabWidget
)
from PySide6.QtCore import QSize, Qt,QDate,QDateTime
from PySide6.QtGui import QAction, QIcon,QPixmap
from functools import partial

# import modlu
from DATABASE.databse import buat_koneksi
basedir = os.path.dirname(__file__)

class HalamanMahasiswa(QMainWindow):
    def __init__(self,username,id_tugas=None):
        super().__init__()
        self.username = username  # Simpan username
        self.id_tugas = id_tugas
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
        
        setting = QAction(QIcon(os.path.join(basedir,"./gambarMahasiswa/image.png")),"Setting",self)
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
        qss_file = os.path.join(basedir, "./style.qss")
        if os.path.exists(qss_file):
            with open(qss_file, "r") as file:
                qss = file.read()
                QApplication.instance().setStyleSheet(qss)
    
    # def halamanDataUser(self):
    #     self.showDataUser = DataUser(self.username)
    #     self.showDataUser.show()

    def halamanSetting(self):
         self.showSetting = HalamanSetting(self.username)
         self.showSetting.show()

    def show_langout(self):
        from main import LoginWindow
        masseg = QMessageBox.question(self, "Konfirmasi", "Apakah anda yakin ingin keluar dari akun ini?", QMessageBox.Yes | QMessageBox.No)
        if masseg == QMessageBox.Yes:
                    self.close()
                    print("aplikasi di close")
                    self.showLogin = LoginWindow()
                    self.showLogin.show()

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
        self.daftarTugas.setColumnCount(7)
        self.daftarTugas.setHorizontalHeaderLabels(["No Tugas","Id mk","Deskripsi Tugas", "Tanggal Pemberian","Tanggal Pengumpulan","Waktu","Action"])
        self.daftarTugas.horizontalHeader().setStretchLastSection(False)
        layoutDs.addWidget(self.daftarTugas)
        
        # 
        layoutDs.addStretch()
        container.setLayout(layoutDs)
        self.setCentralWidget(container)
        self.tugas()
        # self.pesanPengingat()
        self.pengingat()
        self.tugas()
    
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

        # memembuat table jadwal
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

    # menampilkan data jadwal 
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


    # method menampilkan data tugas
    def tugas(self):
        connection, curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT tugas.id_tugas, tugas.id_mk, tugas.deskripsi_tugas, tugas.tanggal_pemberian, tugas.tanggal_pengumpulan, 
                ABS(DATEDIFF(tugas.tanggal_pengumpulan, tugas.tanggal_pemberian)) AS selisih_hari
                FROM tugas
                JOIN matakuliah ON matakuliah.id_mk = tugas.id_mk;
            """
        
        curse.execute(query)
        ambildata = curse.fetchall()
        hariIni = QDate.currentDate()  # Tanggal hari ini

        self.daftarTugas.setRowCount(len(ambildata))
        for barisnumber, barisData in enumerate(ambildata):
            for col, data in enumerate(barisData):
                self.daftarTugas.setItem(barisnumber, col, QTableWidgetItem(str(data)))
            
            id_tugas = barisData[0]
            tanggal_deadline = QDate.fromString(barisData[4].strftime("%Y-%m-%d"), "yyyy-MM-dd")

            # Cek apakah user sudah mengumpulkan tugas
            query_check = """
            SELECT COUNT(*) 
            FROM pengumpulantugas 
            WHERE id_tugas = %s AND nim = (
                SELECT dataMahasiswa.nim 
                FROM dataMahasiswa 
                JOIN loginMahasiswa ON loginMahasiswa.username = dataMahasiswa.nim 
                WHERE loginMahasiswa.username = %s
            )
            """
            curse.execute(query_check, (id_tugas, self.username))
            sudah_dikumpulkan = curse.fetchone()[0] > 0

            # Kondisi untuk menonaktifkan tombol
            tombol_nonaktif = tanggal_deadline < hariIni
            
            # buttin action
            self.buttonKmpl = QPushButton()
            
            # jika user sudah mengumpulkan tugas maka button tersebut berubah mnejadi view
            # dan bis amelihat isi tugas kita tapi tidak bisa di rubah
            if sudah_dikumpulkan:
                self.buttonKmpl.setText("VIEW")
                self.buttonKmpl.setStyleSheet("""           
                background-color: green;
                color : white;
                font-weight: bold;
                """)
                self.buttonKmpl.clicked.connect(partial(self.kumpulkan, id_tugas=id_tugas))

            # sedangkan ini jika hanya jika tanggal deadline lebih kecil dari hari ini atau user
            # tidak mengumpulkn tugas maka btn nya akan di nonaktifkan dan warnanya berubah dan tulisnya juga berubah 
            elif tanggal_deadline < hariIni or  sudah_dikumpulkan:
                self.buttonKmpl.setText("Tidak Mengumpulkan")
                self.buttonKmpl.setStyleSheet("""           
                background-color: RED;
                color : white;
                font-weight: bold;
                """)
            
            # ini mengecek jika user belum mengumpulkan tugas maka btn bertuliskan kumpulkan dan mengarah ke dalam 
            # method kumpulkn
            else:
                self.buttonKmpl.setText("Kumpulkan")
                self.buttonKmpl.setObjectName("Kumpulkan")
                self.buttonKmpl.clicked.connect(partial(self.kumpulkan, id_tugas=id_tugas))

             # Disable tombol jika kondisi terpenuhi
            self.buttonKmpl.setEnabled(not tombol_nonaktif) 
            self.buttonKmpl.setProperty("row", barisnumber)
            self.daftarTugas.setCellWidget(barisnumber, 6, self.buttonKmpl)
        self.daftarTugas.resizeColumnsToContents()

    # ini method pemanggilan class halamanKumpulkantugas
    def kumpulkan(self,id_tugas):
        self.ShowHalamanKumpulkanTugas = HalamanKumpulkanTugas(id_tugas,self.username,self.tugas)
        self.ShowHalamanKumpulkanTugas.show()
    
    # ini method pemanggilan class halaman penampilan tuags
    def view(self,id_tugas):
        self.ShowHalamanViewTugas = HalamanViewTugas(id_tugas,self.username)
        self.ShowHalamanViewTugas.show()

    # ini method untuk filter
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

    # ini method pesan deadline
    def pengingat(self):
        connection,curse = buat_koneksi()
        curse = connection.cursor()

        # Query untuk mengambil data deadline
        query = "SELECT * FROM tugas"
        curse.execute(query)
        ambildata = curse.fetchall()
        
        # ini mengambil tanggal hari ini
        hariIni = QDateTime.currentDateTime()

        for  data in ambildata:
            # ambildata di kolom 1
            namajudul = data[2]
            # ambil data dikolom 2 dengan format tanggal
            tanggalDeadline = data[4].strftime("%Y-%m-%d %H:%M:%S")
            
            # Konversi ke QDate
            formatDeadline = QDateTime.fromString(tanggalDeadline, "yyyy-MM-dd HH:mm:ss")  
            # hitung sisa hari hingga deadline
            sisaHari = hariIni.daysTo(formatDeadline)  # Hitung sisa hari hingga deadline

            # sudah_kumpulkan = 
            # Cek apakah user sudah mengumpulkan tugas
            query_check = """
            SELECT COUNT(*) 
            FROM pengumpulantugas 
            WHERE id_tugas = %s AND nim = (
                SELECT dataMahasiswa.nim 
                FROM dataMahasiswa 
                JOIN loginMahasiswa ON loginMahasiswa.username = dataMahasiswa.nim 
                WHERE loginMahasiswa.username = %s
            )
            """
            curse.execute(query_check, (data[0], self.username))
            sudah_dikumpulkan = curse.fetchone()[0] > 0

            # menghilangkan pengingat jika batasnya sudah melewati deadline
            if sisaHari < 0 or sudah_dikumpulkan:
                continue

            # deadline hari ini
            elif sisaHari == 0 :
                pesan = f"Tugas '{namajudul}' harus diselesaikan hari ini ({formatDeadline.toString('dd MMMM yyyy HH:mm:ss')})!"
                QMessageBox.warning(self, "Deadline Hari Ini", pesan)    
            
            # tenggal hari <= 3 hari
            elif sisaHari <= 3:  
                pesan = f"Tugas '{namajudul}' akan jatuh tempo dalam {sisaHari} hari, yaitu pada {formatDeadline.toString('dd MMMM yyyy HH:mm:ss')}."
                QMessageBox.information(self, "Pengingat Deadline", pesan)


# ini halamanuser
# class DataUser(QWidget):
#     def __init__(self,username):
#         super().__init__()
#         self.setWindowTitle("Data User")
#         self.setFixedSize(350,350)
#         self.setStyleSheet("""
#             background-color:rgb(235, 241, 243);
#             font-family:Poppins;
#             font-weight:bold;
#             font-size:15px;
#                            """)

#         container = QWidget()
#         layout = QVBoxLayout()
        
#         lbFoto = QLabel()
#         pixmap = QPixmap(os.path.join(basedir, "./gambarMahasiswa/13.png"))
#         lbFoto.setPixmap(pixmap)
        
#         lbFoto.setAlignment(Qt.AlignCenter)
#         layout.addWidget(lbFoto)

#         # nim
#         self.lb2Nim = QLabel("")
#         self.lb2Nim.setObjectName("nim")
        
#         # nama
#         self.lb2Nama = QLabel("")
#         self.lb2Nama.setObjectName("nama")
        
#         # menambahakan jurusan
#         self.lb2Jurusan = QLabel("")
#         self.lb2Jurusan.setObjectName("jurusan")

#         # menambahkaan prodi
#         self.lb2Prodi = QLabel("")
#         self.lb2Prodi.setObjectName("prodi")

#         # menmbhkan smester
#         self.lb2Semester = QLabel("")
#         self.lb2Semester.setObjectName("semester")

#         # menambhakn widget kedalam layout 
#         layout.addWidget(self.lb2Nim)
#         layout.addWidget(self.lb2Nama)
#         layout.addWidget(self.lb2Jurusan)
#         layout.addWidget(self.lb2Prodi)
#         layout.addWidget(self.lb2Semester)

#         # setlayout (layout) kedalam container
#         container.setLayout(layout)
#         layout.addStretch()
#         self.setLayout(layout)
#         self.ambil_dataUser(username)
    
#     def ambil_dataUser(self,username):
#         connection,curse = buat_koneksi()
#         curse = connection.cursor()
#         query = """
#                 SELECT datamahasiswa.nim , datamahasiswa.nama, datamahasiswa.jurusan, datamahasiswa.prodi , datamahasiswa.semester
#                 FROM datamahasiswa 
#                 JOIN loginmahasiswa 
#                 ON datamahasiswa.nim = loginmahasiswa.username 
#                 WHERE loginmahasiswa.username = %s;
#             """
#         curse.execute(query,(username,))

#         # menampilkan usrname di consle
#         print(username)

#         ambildata = curse.fetchone()
#         if ambildata:
#                 nim,nama,jurusan,prodi,semester = ambildata
#                 self.lb2Nim.setText(f'Nim            : {nim}')
#                 self.lb2Nama.setText(f'Nama         : {nama}')
#                 self.lb2Jurusan.setText(f'Jurusan     : {jurusan}')
#                 self.lb2Prodi.setText(f'Prodi          : {prodi}')
#                 self.lb2Semester.setText(f'Semester  : {semester}')
#         else:
#                 self.lb2Nim.setText(f"Data Tidak ditemukan")
#                 self.lb2Nama.setText("Data Tidak ditemukan")
#                 self.lb2Jurusan.setText("Data Tidak ditemukan")
#                 self.lb2Prodi.setText("Data Tidak ditemukan")
#                 self.lb2Semester.setText("Data Tidak ditemukan")


# ini class menampilkan data data yang didalam setting
class HalamanSetting(QWidget):
    def __init__(self,username):
        super().__init__()
        self.userame = username
        self.setWindowTitle("Halaman Pengaturan")
        self.setFixedSize(300,350)
        layout = QVBoxLayout()

        # membuat tab
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)

        # menmabhkan tab didalam tabs(QTabWidget)
        tabs.addTab(self.user(username), "Profile")
        tabs.addTab(self.changePw(username), "Change Password")   
        # tabs.addTab(self.logout(), "Logout")   

        # menmapilkan tabs
        # self.setCentralWidget(tabs)
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.user(username)
        self.changePw(username)

    def user(self,username):
        # layout awal
        layout = QVBoxLayout()
        
        # memberikan margin
        layout.setContentsMargins(4,4,4,4)
        
        # ini memberikan spacing antar content
        layout.setSpacing(5)

        #ini  content
        foto = QLabel()
        fotouser = QPixmap(os.path.join(basedir,"./gambarMahasiswa/13.png"))
        foto.setPixmap(fotouser)
        foto.setAlignment(Qt.AlignCenter)
        layout.addWidget(foto)

        # layout nama
        layoutHNama = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbNama = QLabel("Nama")
        self.lbNama.setStyleSheet("margin-right: 15px")
        self.ldNama = QLineEdit()
        layoutHNama.addWidget(self.lbNama)
        layoutHNama.addWidget(self.ldNama)

        # layout nim
        layoutHNim = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbNim = QLabel("Nim")
        self.lbNim.setStyleSheet("margin-right : 25px")
        self.ldNim = QLineEdit()
        layoutHNim.addWidget(self.lbNim)
        layoutHNim.addWidget(self.ldNim)

        # layout jurusan
        layoutHJurusan = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbJurusan = QLabel("Jurusan")
        self.lbJurusan.setStyleSheet("margin-right : 8px")
        self.ldJurusan = QLineEdit()
        layoutHJurusan.addWidget(self.lbJurusan)
        layoutHJurusan.addWidget(self.ldJurusan)

        # layout prodi
        layoutHProdi = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbProdi = QLabel("Prodi")
        self.lbProdi.setStyleSheet("margin-right : 20px")
        self.ldProdi = QLineEdit()
        layoutHProdi.addWidget(self.lbProdi)
        layoutHProdi.addWidget(self.ldProdi)

        # layout nim
        layoutHUsername = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbUsername = QLabel("Username")
        self.lbUsername.setStyleSheet("margin-right : 5px")
        self.ldUsername = QLineEdit()
        layoutHUsername.addWidget(self.lbUsername)
        layoutHUsername.addWidget(self.ldUsername)

        # ini membuat widget yang menampung layout vertikal
        widget = QWidget()
        layout.addLayout(layoutHNama)
        layout.addLayout(layoutHNim)
        layout.addLayout(layoutHJurusan)
        layout.addLayout(layoutHProdi)
        layout.addLayout(layoutHUsername)


        # merapikan layout
        layoutHNama.setContentsMargins(4,4,4,4)
        layoutHNama.setSpacing(5)
        layoutHNim.setContentsMargins(4,4,4,4)
        layoutHNim.setSpacing(5)
        layoutHJurusan.setContentsMargins(4,4,4,4)
        layoutHJurusan.setSpacing(5)
        layoutHProdi.setContentsMargins(4,4,4,4)
        layoutHProdi.setSpacing(5)
        layoutHUsername.setContentsMargins(4,4,4,4)
        layoutHUsername.setSpacing(5)
        widget.setLayout(layout)
        self.ambilDataUser(username)
        return widget
    
    def ambilDataUser(self,username):
        connction,curse = buat_koneksi()
        curse = connction.cursor()

        query = """
                SELECT datamahasiswa.nama, datamahasiswa.nim, datamahasiswa.jurusan,
                   datamahasiswa.prodi, loginmahasiswa.username
            FROM datamahasiswa
            JOIN loginmahasiswa ON datamahasiswa.nim = loginmahasiswa.username
            WHERE loginmahasiswa.username = %s;       
                """
        curse.execute(query,(username,))
        ambildata = curse.fetchall()
        if ambildata:
            nama,nim,jurusan,prodi,username = ambildata[0]
            self.ldNama.setText(nama)
            self.ldNim.setText(nim)
            self.ldJurusan.setText(jurusan)
            self.ldProdi.setText(prodi)
            self.ldUsername.setText(username)

    def changePw(self,username):
        # layout pertama
        layout = QVBoxLayout()

        # layout username
        layoutHUsernamePw = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbUsernamePw = QLabel("Username")
        self.lbUsernamePw.setStyleSheet("margin-right : 58px")
        self.ldUsernamePw = QLineEdit()
        self.ldUsername.setEnabled(False)
        layoutHUsernamePw.addWidget(self.lbUsernamePw)
        layoutHUsernamePw.addWidget(self.ldUsernamePw)

        connection,curse = buat_koneksi()
        curse = connection.cursor()

        query = """
            select loginmahasiswa.username from loginmahasiswa where loginmahasiswa.username = %s;
"""

        curse.execute(query,(username,))
        ambildata = curse.fetchone()
        if ambildata:
            username = ambildata[0]
            self.ldUsernamePw.setText(username)

        # layout pw baru
        layoutHPw = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbPw = QLabel("New Password")
        self.lbPw.setStyleSheet("margin-right : 35px")
        self.ldPw = QLineEdit()
        layoutHPw.addWidget(self.lbPw)
        layoutHPw.addWidget(self.ldPw)

        # layout konfir pw
        layoutHKonfirPw = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbKonfirPw = QLabel("Konfirmasi Password")
        self.lbKonfirPw.setStyleSheet("margin-right : 5px")
        self.ldKonfirPw = QLineEdit()
        layoutHKonfirPw.addWidget(self.lbKonfirPw)
        layoutHKonfirPw.addWidget(self.ldKonfirPw)

        # button ubah
        self.edit = QPushButton("SIMPAN")
        self.edit.clicked.connect(self.simpan)

        # menambah layout didalam layout utama
        layout.addLayout(layoutHUsernamePw)
        layout.addLayout(layoutHPw)
        layout.addLayout(layoutHKonfirPw)
        layout.addWidget(self.edit) 

        container = QWidget()
        container.setLayout(layout)
        self.simpan(username)
        return container

#     def simpan(self,username):
#         print("simpan")
#         connection,curse = buat_koneksi()
#         curse = connection.cursor()

#         query_check = """
#             select loginmahasiswa.username from loginmahasiswa where loginmahasiswa.username = %s;
# """
#         curse.execute(query_check,(username,))
#         ambildata = curse.fetchone()

#         if ambildata:
#             username = ambildata[0]
#             self.ldUsernamePw.setText(username)

#         pw = self.ldPw.text()
#         konfirPw = self.ldKonfirPw.text()

#         if pw != konfirPw:
#             QMessageBox.warning(self,"Warning","Password baru dan Konfirmasi password tidak sama!")

#         query = """
#             UPDATE loginmahasiswa SET password = %s  where username = %s;
# """
#         curse.execute(query,(username, pw))
#         connection.commit()
# class HalamanSetting(QWidget):
    def __init__(self,username):
        super().__init__()
        self.userame = username
        self.setWindowTitle("Halaman Pengaturan")
        self.setFixedSize(300,350)
        layout = QVBoxLayout()

        # membuat tab
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)

        # menmabhkan tab didalam tabs(QTabWidget)
        tabs.addTab(self.user(username), "Profile")
        tabs.addTab(self.changePw(username), "Change Password")   
        # tabs.addTab(self.logout(), "Logout")   

        # menmapilkan tabs
        # self.setCentralWidget(tabs)
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.user(username)

    def user(self,username):
        # layout awal
        layout = QVBoxLayout()
        
        # memberikan margin
        layout.setContentsMargins(4,4,4,4)
        
        # ini memberikan spacing antar content
        layout.setSpacing(5)

        #ini  content
        foto = QLabel()
        fotouser = QPixmap(os.path.join(basedir,"./gambarMahasiswa/13.png"))
        foto.setPixmap(fotouser)
        foto.setAlignment(Qt.AlignCenter)
        layout.addWidget(foto)

        # layout nama
        layoutHNama = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbNama = QLabel("Nama")
        self.lbNama.setStyleSheet("margin-right: 15px")
        self.ldNama = QLineEdit()
        layoutHNama.addWidget(self.lbNama)
        layoutHNama.addWidget(self.ldNama)

        # layout nim
        layoutHNim = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbNim = QLabel("Nim")
        self.lbNim.setStyleSheet("margin-right : 25px")
        self.ldNim = QLineEdit()
        layoutHNim.addWidget(self.lbNim)
        layoutHNim.addWidget(self.ldNim)

        # layout jurusan
        layoutHJurusan = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbJurusan = QLabel("Jurusan")
        self.lbJurusan.setStyleSheet("margin-right : 8px")
        self.ldJurusan = QLineEdit()
        layoutHJurusan.addWidget(self.lbJurusan)
        layoutHJurusan.addWidget(self.ldJurusan)

        # layout prodi
        layoutHProdi = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbProdi = QLabel("Prodi")
        self.lbProdi.setStyleSheet("margin-right : 20px")
        self.ldProdi = QLineEdit()
        layoutHProdi.addWidget(self.lbProdi)
        layoutHProdi.addWidget(self.ldProdi)

        # layout nim
        layoutHUsername = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbUsername = QLabel("Username")
        self.lbUsername.setStyleSheet("margin-right : 5px")
        self.ldUsername = QLineEdit()
        layoutHUsername.addWidget(self.lbUsername)
        layoutHUsername.addWidget(self.ldUsername)

        # ini membuat widget yang menampung layout vertikal
        widget = QWidget()
        layout.addLayout(layoutHNama)
        layout.addLayout(layoutHNim)
        layout.addLayout(layoutHJurusan)
        layout.addLayout(layoutHProdi)
        layout.addLayout(layoutHUsername)


        # merapikan layout
        layoutHNama.setContentsMargins(4,4,4,4)
        layoutHNama.setSpacing(5)
        layoutHNim.setContentsMargins(4,4,4,4)
        layoutHNim.setSpacing(5)
        layoutHJurusan.setContentsMargins(4,4,4,4)
        layoutHJurusan.setSpacing(5)
        layoutHProdi.setContentsMargins(4,4,4,4)
        layoutHProdi.setSpacing(5)
        layoutHUsername.setContentsMargins(4,4,4,4)
        layoutHUsername.setSpacing(5)
        self.ambilDataUser(username)
        widget.setLayout(layout)
        return widget
    
    def ambilDataUser(self,username):
        connction,curse = buat_koneksi()
        curse = connction.cursor()

        query = """
                SELECT datamahasiswa.nama, datamahasiswa.nim, datamahasiswa.jurusan,
                   datamahasiswa.prodi, loginmahasiswa.username
            FROM datamahasiswa
            JOIN loginmahasiswa ON datamahasiswa.nim = loginmahasiswa.username
            WHERE loginmahasiswa.username = %s;       
                """
        curse.execute(query,(username,))
        ambildata = curse.fetchall()
        if ambildata:
            nama,nim,jurusan,prodi,username = ambildata[0]
            self.ldNama.setText(nama)
            self.ldNim.setText(nim)
            self.ldJurusan.setText(jurusan)
            self.ldProdi.setText(prodi)
            self.ldUsername.setText(username)

    def changePw(self):
        # layout pertama
        layout = QVBoxLayout()

        # layout username
        layoutHUsernamePw = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbUsernamePw = QLabel("Username")
        self.lbUsernamePw.setStyleSheet("margin-right : 58px")
        self.ldUsernamePw = QLineEdit()
        layoutHUsernamePw.addWidget(self.lbUsernamePw)
        layoutHUsernamePw.addWidget(self.ldUsernamePw)

        # layout pw baru
        layoutHPw = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbPw = QLabel("New Password")
        self.lbPw.setStyleSheet("margin-right : 35px")
        self.ldPw = QLineEdit()
        layoutHPw.addWidget(self.lbPw)
        layoutHPw.addWidget(self.ldPw)

        # layout konfir pw
        layoutHKonfirPw = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbKonfirPw = QLabel("Konfirmasi Password")
        self.lbKonfirPw.setStyleSheet("margin-right : 5px")
        self.ldKonfirPw = QLineEdit()
        layoutHKonfirPw.addWidget(self.lbKonfirPw)
        layoutHKonfirPw.addWidget(self.ldKonfirPw)

        # button ubah
        self.edit = QPushButton("SIMPAN")
        self.edit.clicked.connect(self.simpan)

        # menambah layout didalam layout utama
        layout.addLayout(layoutHUsernamePw)
        layout.addLayout(layoutHPw)
        layout.addLayout(layoutHKonfirPw)
        layout.addWidget(self.edit) 

        self.simpan()
        container = QWidget()
        container.setLayout(layout)
        return container

class HalamanSetting(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username  # Simpan username di atribut instance
        self.setWindowTitle("Halaman Pengaturan")
        self.setFixedSize(300, 350)
        layout = QVBoxLayout()

        # Membuat tab
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)

        # Menambahkan tab di dalam tabs(QTabWidget)
        tabs.addTab(self.user(self.username), "Profile")
        tabs.addTab(self.changePw(), "Change Password")

        # Menampilkan tabs
        layout.addWidget(tabs)
        self.setLayout(layout)

    def user(self, username):
        layout = QVBoxLayout()

        # Memberikan margin dan spacing
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(5)

        # Content: Foto
        foto = QLabel()
        fotouser = QPixmap(os.path.join(basedir, "./gambarMahasiswa/13.png"))
        foto.setPixmap(fotouser)
        foto.setAlignment(Qt.AlignCenter)
        layout.addWidget(foto)

        # Layout Nama
        layoutHNama = QHBoxLayout()
        self.lbNama = QLabel("Nama")
        self.lbNama.setStyleSheet("margin-right: 15px")
        self.ldNama = QLineEdit()
        layoutHNama.addWidget(self.lbNama)
        layoutHNama.addWidget(self.ldNama)

        # Layout Nim
        layoutHNim = QHBoxLayout()
        self.lbNim = QLabel("Nim")
        self.lbNim.setStyleSheet("margin-right : 25px")
        self.ldNim = QLineEdit()
        layoutHNim.addWidget(self.lbNim)
        layoutHNim.addWidget(self.ldNim)

        # Layout Jurusan
        layoutHJurusan = QHBoxLayout()
        self.lbJurusan = QLabel("Jurusan")
        self.lbJurusan.setStyleSheet("margin-right : 8px")
        self.ldJurusan = QLineEdit()
        layoutHJurusan.addWidget(self.lbJurusan)
        layoutHJurusan.addWidget(self.ldJurusan)

        # Layout Prodi
        layoutHProdi = QHBoxLayout()
        self.lbProdi = QLabel("Prodi")
        self.lbProdi.setStyleSheet("margin-right : 20px")
        self.ldProdi = QLineEdit()
        layoutHProdi.addWidget(self.lbProdi)
        layoutHProdi.addWidget(self.ldProdi)

        # Layout Username
        layoutHUsername = QHBoxLayout()
        self.lbUsername = QLabel("Username")
        self.lbUsername.setStyleSheet("margin-right : 5px")
        self.ldUsername = QLineEdit()
        layoutHUsername.addWidget(self.lbUsername)
        layoutHUsername.addWidget(self.ldUsername)

        # Menambahkan layout ke dalam layout utama
        layout.addLayout(layoutHNama)
        layout.addLayout(layoutHNim)
        layout.addLayout(layoutHJurusan)
        layout.addLayout(layoutHProdi)
        layout.addLayout(layoutHUsername)

        self.ambilDataUser(username)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def ambilDataUser(self, username):
        connection, curse = buat_koneksi()
        curse = connection.cursor()

        query = """
            SELECT datamahasiswa.nama, datamahasiswa.nim, datamahasiswa.jurusan,
                   datamahasiswa.prodi, loginmahasiswa.username
            FROM datamahasiswa
            JOIN loginmahasiswa ON datamahasiswa.nim = loginmahasiswa.username
            WHERE loginmahasiswa.username = %s;
        """
        curse.execute(query, (username,))
        ambildata = curse.fetchall()
        if ambildata:
            nama, nim, jurusan, prodi, username = ambildata[0]
            self.ldNama.setText(nama)
            self.ldNim.setText(nim)
            self.ldJurusan.setText(jurusan)
            self.ldProdi.setText(prodi)
            self.ldUsername.setText(username)

    def changePw(self):
        layout = QVBoxLayout()

        # Layout Username
        layoutHUsernamePw = QHBoxLayout()
        self.lbUsernamePw = QLabel("Username")
        self.lbUsernamePw.setStyleSheet("margin-right : 58px")
        self.ldUsernamePw = QLineEdit()
        layoutHUsernamePw.addWidget(self.lbUsernamePw)
        layoutHUsernamePw.addWidget(self.ldUsernamePw)

        # Layout Password Baru
        layoutHPw = QHBoxLayout()
        self.lbPw = QLabel("New Password")
        self.lbPw.setStyleSheet("margin-right : 35px")
        self.ldPw = QLineEdit()
        self.ldPw.setEchoMode(QLineEdit.Password)
        layoutHPw.addWidget(self.lbPw)
        layoutHPw.addWidget(self.ldPw)

        # Layout Konfirmasi Password
        layoutHKonfirPw = QHBoxLayout()
        self.lbKonfirPw = QLabel("Konfirmasi Password")
        self.lbKonfirPw.setStyleSheet("margin-right : 5px")
        self.ldKonfirPw = QLineEdit()
        self.ldKonfirPw.setEchoMode(QLineEdit.Password)
        layoutHKonfirPw.addWidget(self.lbKonfirPw)
        layoutHKonfirPw.addWidget(self.ldKonfirPw)

        # Button SIMPAN
        self.edit = QPushButton("SIMPAN")
        self.edit.clicked.connect(self.simpan)

        # Menambahkan layout ke dalam layout utama
        layout.addLayout(layoutHUsernamePw)
        layout.addLayout(layoutHPw)
        layout.addLayout(layoutHKonfirPw)
        layout.addWidget(self.edit)

        container = QWidget()
        container.setLayout(layout)
        return container

    def simpan(self,username):
        connection, curse = buat_koneksi()
        curse = connection.cursor()

        query_check = """
            select loginmahasiswa.username from loginmahasiswa where loginmahasiswa.username = %s;
"""
        curse.execute(query_check,(username,))
        ambildata = curse.fetchone()

        if ambildata:
            username = ambildata[0]
            self.ldUsernamePw.setText(username)

        username = self.ldUsernamePw.text()
        pw = self.ldPw.text()
        konfirPw = self.ldKonfirPw.text()

        if pw != konfirPw:
            QMessageBox.warning(self, "Warning", "Password baru dan Konfirmasi password tidak sama!")
            return  # Keluar jika tidak sama

        query = """
            UPDATE loginmahasiswa SET password = %s WHERE username = %s;
        """
        curse.execute(query, (pw, self.username))  # Gunakan self.username untuk update
        connection.commit()
        QMessageBox.information(self, "Berhasil", "Password berhasil diubah!")

    def ambilDataTugas(self,id_tugas):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT tugas.id_tugas, tugas.id_mk, tugas.deskripsi_tugas, tugas.tanggal_pemberian, tugas.tanggal_pengumpulan
                FROM tugas
                JOIN matakuliah ON matakuliah.id_mk = tugas.id_mk
                WHERE tugas.id_tugas = %s;
            """
        curse.execute(query,(id_tugas,))
        # menampilkan usrname di consle
        print(id_tugas)
        ambildata = curse.fetchone()
        if ambildata:
                id_tugas,id_mk,self.deskripsi_tugas,tanggal_pemberian,tanggal_pengumpulan = ambildata
                self.idTugas = id_tugas
                self.idmk = id_mk
                # self.jdl_tgs = deskripsi_tugas.text()
                self.id_tugas.setText(f'id Tugas\t\t\t: {id_tugas}')
                self.mataKuliah.setText(f'Id Mata Kuliah\t\t: {id_mk}')
                self.judulTugas.setText(f'Judul Tugas\t\t: {self.deskripsi_tugas}')
                self.tanggalPemberian.setText(f'Tanggal Pemberian\t: {tanggal_pemberian}')
                self.tanggalDeadline.setText(f'Deadline\t\t\t: {tanggal_pengumpulan}')

    def kirim (self):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        queryNim = ("select dataMahasiswa.nim from datamahasiswa join loginmahasiswa on loginmahasiswa.username = datamahasiswa.nim where loginmahasiswa.username = %s")
        curse.execute(queryNim,(self.username,))
        nimdata = curse.fetchone()
        nim = nimdata[0]

        queryCheck = """
        SELECT file_tugas 
        FROM pengumpulantugas 
        WHERE id_tugas = %s AND nim = %s
    """
        curse.execute(queryCheck, (self.idTugas, nim))
        ambildata = curse.fetchone()

        if ambildata:
            QMessageBox.warning(self, "Duplikasi", "Tugas ini sudah pernah dikumpulkan.")
            return

        tglPengumpulan = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        fileTgs = self.FileTugas.toPlainText()

        if not fileTgs:
            QMessageBox.warning(self, "Peringatan", "File Tugas kosong,silahkan lengkapi file tugas.")
            return
        else:
            query = """
                    Insert into pengumpulantugas (id_tugas,id_mk,nim,tanggal_pengumpulan,file_tugas)
                    values (%s,%s,%s,%s,%s)
                """
            curse.execute(query,(self.idTugas,self.idmk,nim,tglPengumpulan,fileTgs))
            Jdltugas = self.deskripsi_tugas
            massage = QMessageBox.question(self,"",f"Apakah anda yakin ? ", QMessageBox.Yes | QMessageBox.No)
            if massage == QMessageBox.Yes : 
                connection.commit()
                print("berhasil")
                QMessageBox.information(self,"Berhasil",f"Pengumpulan tugas yang berjudul {Jdltugas} berhasil")
                self.close()
                self.tugas()

# untuk melihat tugas yang sudah diinputkan
class HalamanViewTugas(QWidget):
    def __init__(self,id_tugas,username):
        super().__init__()
        self.username = username
        self.setWindowTitle("View Tugas")
        self.setFixedSize(450,450)
        layout = QVBoxLayout()

        # membuat kontent
        self.id_tugas = QLabel()
        self.mataKuliah = QLabel()
        self.judulTugas = QLabel()
        self.tanggalPemberian = QLabel()
        self.tanggalDeadline = QLabel()
        self.tanggal = QLabel()
        self.FileTugas = QPlainTextEdit()
        self.FileTugas.setEnabled(False)
        self.lbFile = QLabel("File Tugas")
        # self.btnKirim = QPushButton("Kirim")
        # self.btnKirim.clicked.connect(self.kirim)
        
        # menambahkan ke layout
        layout.addWidget(self.id_tugas)
        layout.addWidget(self.mataKuliah)
        layout.addWidget(self.judulTugas)
        layout.addWidget(self.tanggalPemberian)
        layout.addWidget(self.tanggalDeadline)
        layout.addWidget(self.tanggal)
        layout.addWidget(self.lbFile)
        layout.addWidget(self.FileTugas)
        # layout.addWidget(self.btnKirim)

        # mengsetlayout
        self.setLayout(layout)
        self.ambilDataTugas(id_tugas)

    def ambilDataTugas(self,id_tugas):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT tugas.id_tugas, tugas.id_mk, tugas.deskripsi_tugas, tugas.tanggal_pemberian, tugas.tanggal_pengumpulan,pengumpulantugas.tanggal_pengumpulan,pengumpulantugas.file_tugas
                FROM pengumpulantugas
                JOIN matakuliah ON matakuliah.id_mk = pengumpulantugas.id_mk
                JOIN tugas ON tugas.id_tugas = pengumpulantugas.id_tugas
                WHERE pengumpulantugas.id_tugas = %s;
            """
        curse.execute(query,(id_tugas,))
        # menampilkan usrname di consle
        print(id_tugas)
        ambildata = curse.fetchone()
        if ambildata:
                id_tugas,id_mk,deskripsi_tugas,tanggal_pemberian,tanggal_pengumpulan,tanggal,file_tugas = ambildata
                self.idTugas = id_tugas
                self.idmk = id_mk
                self.id_tugas.setText(f'id Tugas\t\t\t: {id_tugas}')
                self.mataKuliah.setText(f'Id Mata Kuliah\t\t: {id_mk}')
                self.judulTugas.setText(f'Judul Tugas\t\t: {deskripsi_tugas}')
                self.tanggalPemberian.setText(f'Tanggal Pemberian\t: {tanggal_pemberian}')
                self.tanggalDeadline.setText(f'Deadline\t\t\t: {tanggal_pengumpulan}')
                self.tanggal.setText(f'Tanggal Pengumpulan\t: {tanggal}')
                self.FileTugas.setPlainText(f'{file_tugas}')