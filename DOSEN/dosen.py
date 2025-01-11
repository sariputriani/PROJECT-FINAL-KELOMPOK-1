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
    QMessageBox,
    QFrame,
    QTableWidget,
    QComboBox,
    QDateTimeEdit,
    QTableWidgetItem,
    QTabWidget,
    QPlainTextEdit
)
from PySide6.QtCore import QSize, Qt,QDate,QDateTime
from PySide6.QtGui import QAction, QIcon,QPixmap
from functools import partial
# from databases.database_main import database
from DATABASE.databse import buat_koneksi
basedir = os.path.dirname(__file__)

class HalamanDosen(QMainWindow):
    def __init__(self,username,password):
        super().__init__()
        # self.setWindowTitle("Mahasiswa")
        self.username = username  # Simpan username
        self.password = password
        self.setWindowTitle(f"Selamat Datang, {self.username}")
        # self.setFixedSize(700,600)
        self.setGeometry(450,50,700,600)


        # ini fungsi memanggil metode styleqss
        self.styleqss()

        # Layout dan Widget
        self.layoutMHS = QVBoxLayout()
        
        # Menambahkan widget ke layout
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar)

        Dashboard = QAction("Dashboard", self)
        Dashboard.setCheckable(True)
        self.toolbar.addAction(Dashboard)
        Dashboard.triggered.connect(self.Dashboard)

        spasi = QWidget()
        spasi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spasi)

        setting = QAction(
            QIcon(os.path.join(basedir, "./gambardosen/image.png")),
            "Setting",self
        )
        self.toolbar.addAction(setting)
        setting.triggered.connect(self.show_setting)
        

        exit = QAction(
            QIcon(os.path.join(basedir, "./gambardosen/langout.png")),
            "logout",self
        )
        self.toolbar.addAction(exit)
        exit.triggered.connect(self.logout)

        # Mengatur layout untuk widget utama
        self.setLayout(self.layoutMHS)

    # sedangkan ini memanggil file style.qss
    def styleqss(self):
        qss_file = os.path.join(basedir, "./style.qss")
        if os.path.exists(qss_file):    
            with open(qss_file, "r") as file:
                qss = file.read()
                QApplication.instance().setStyleSheet(qss)

    def Dashboard(self):
        # connection,curse = buat_koneksi()
        container = QWidget()
        layout = QVBoxLayout()
        judul = QLabel("Dashboard Tugas")
        judul.setObjectName("lbjudul")
        
        frameLine = QFrame()
        frameLine.setObjectName("garis")
        frameLine.setFrameShape(QFrame.HLine)
        frameLine.setFrameShadow(QFrame.Sunken)
        layout.addWidget(judul)
        layout.addWidget(frameLine)

        tanggal = QDate.currentDate()
        fromat = tanggal.toString("dddd dd - MMMM - yyyy")
        lbTanggal = QLabel(fromat)
        layout.addWidget(lbTanggal)

        # membuat layout btn add
        layoutHAddTugas = QHBoxLayout()
        spasi = QWidget()
        spasi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layoutHAddTugas.addWidget(spasi)

        btnAdd = QPushButton("  Add")
        btnAdd.setObjectName("add")
        btnAdd.setFixedSize(80,50)
        gambarBtnadd = os.path.join(basedir,"","add.png")
        btnAdd.setIcon(QIcon(gambarBtnadd))
        btnAdd.setIconSize(QSize(20,20))
        btnAdd.clicked.connect(self.show_AddTugas)
        layoutHAddTugas.addWidget(btnAdd)
        layout.addLayout(layoutHAddTugas)

        # ini membuat table tugas
        self.tableTugas = QTableWidget()
        # self.tableTugas.setFixedSize()
        # self.tableTugas.setFixedSize(800,400)
        self.tableTugas.setFixedSize(750,400)
        self.tableTugas.setColumnCount(8)
        self.tableTugas.setHorizontalHeaderLabels(["Id Tugas","kode matakuliah","Nama Kuliah","Judul Tugas","Deskripsi Tugas","Tanggal Pemberian","Tanggal Deadline","Action"])
        self.tableTugas.horizontalHeader().setStretchLastSection(False)
        layout.addWidget(self.tableTugas)

        # ini mengset layout kedalam container
        layout.addStretch()
        container.setLayout(layout)
        self.setCentralWidget(container)
        # memanggil method data tugas berdasarkan username
        self.updateDataTableTugas(self.username)
    
    # ini fungsi untuk memnggil class halaman tambah tugas
    def show_AddTugas(self):
        self.showAddTugas = HalamanAddtugas(self.username,self)
        self.showAddTugas.show()

    def updateDataTableTugas(self,username):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
           SELECT 
                tugas.ID_Tugas,
                tugas.ID_MK,
                matakuliah.Nama_MK,
                tugas.judul_tugas,
                tugas.Deskripsi_Tugas,
                tugas.Tanggal_Pemberian,
                tugas.Tanggal_Pengumpulan
            FROM tugas
            JOIN matakuliah ON tugas.ID_MK = matakuliah.ID_MK
            JOIN logindosen ON matakuliah.NIP_Dosen = logindosen.Username
            WHERE logindosen.Username = %s;
"""
        curse.execute(query,(username,))
        ambildata = curse.fetchall()
        if ambildata:
            self.tableTugas.setRowCount(len(ambildata))
            for barisnumber, barisData in enumerate(ambildata):
                for col, data in enumerate(barisData):
                    self.tableTugas.setItem(barisnumber, col, QTableWidgetItem(str(data)))
                # mengambil id_tugas
                id_tugas = barisData[0]
                # membuat  tombolwidget sabgai container buton edit,hapus,view
                tombolWidget = QWidget()
                layoutTombol = QHBoxLayout(tombolWidget)
                # menghapus sapsi mrgin antar content
                layoutTombol.setContentsMargins(0,0,0,0)
                layoutTombol.setSpacing(0)

                # button view
                self.btnView = QPushButton(" View")
                self.btnView.setObjectName("btnViewMahasiswa")
                self.btnView.clicked.connect(partial(self.halamanView, id_tugas))
                
                # button edit
                self.btnEdit = QPushButton(" Edit")
                self.btnEdit.setObjectName("btnEditTugas")
                self.btnEdit.clicked.connect(partial(self.halamanEdit, id_tugas))

                # button hapus 
                self.btnHapus = QPushButton(" Hapus")
                self.btnHapus.setObjectName("btnHapusTugas")
                self.btnHapus.clicked.connect(partial(self.HapusTugas, id_tugas))
                
                # menambah btn edit,hapus dan view didalam layouttombol
                layoutTombol.addWidget(self.btnView)
                layoutTombol.addWidget(self.btnEdit)
                layoutTombol.addWidget(self.btnHapus)
                
                # menetapkan setpoprty
                self.btnView.setProperty("row",barisnumber)
                # meeletakkan tombolwidget kedalam cel atau colom ke 6 setaiap baris
                self.tableTugas.setCellWidget(barisnumber, 7, tombolWidget)
            # merapikan content agar panjang table sesuai dengan data
        self.tableTugas.resizeColumnsToContents()

    # menampilkan halaman setting
    def show_setting(self):
        self.showSetting = HalamanSetting(self.username,self.password)
        self.showSetting.show()

    # ini fungsi untuk logout
    def logout(self):
        from main import LoginWindow
        massage = QMessageBox.question(self,"Pertanyaa","Apakah anda ingin keluar dari aplikasi ? ", QMessageBox.Yes | QMessageBox.No)
        if massage == QMessageBox.Yes:
                    self.close()
                    self.showLogin = LoginWindow()
                    self.showLogin.show()
                    print("aplikasi di close")

    # halaman view daftar mahasiswa yang mengumpulkan
    def halamanView(self,id_tugas):
         self.showView = HalamanView(self.username,id_tugas)
         self.showView.show()
    
    # halaman hapus tugas
    def HapusTugas(self, id_tugas):
        print(f"ID yang diterima untuk dihapus: {id_tugas}")
        connection, curse = buat_koneksi()
        curse = connection.cursor()
        massage = QMessageBox.question(self, "Konfirmasi", 
                                    "Apakah Anda yakin ingin menghapus tugas ini?", 
                                    QMessageBox.Yes | QMessageBox.No)
        if massage == QMessageBox.Yes:
                query = "DELETE FROM tugas WHERE ID_Tugas = %s"
                curse.execute(query, (id_tugas,))
                connection.commit()
                QMessageBox.information(self, "Konfirmasi", "Tugas berhasil dihapus")
                self.updateDataTableTugas(self.username)  # Update table setelah penghapusan

    # halaman eddit tugas
    def halamanEdit (self,id_tugas):
        self.showHalamanEditTugas = HalamanEdittugas(id_tugas,self.username)
        self.showHalamanEditTugas.show()
        
# ini halaman menmabah tugas
class HalamanAddtugas(QWidget):
    def __init__(self,username,parent=None):
        super().__init__()
        # Pastikan username tidak None
        # ini membuat sebuah variabel untuk mengakses method variabel di luar kelas
        self.parentt = parent
        self.username = username
        self.setWindowTitle("Halaman Tambah Tugas")
        self.setFixedSize(300,350)
        # container = QWidget()
        layout = QVBoxLayout()

        # LOGO
        logo = QLabel()
        logoGambar = QPixmap(os.path.join(basedir,"./tugas.png"))
        logo.setPixmap(logoGambar)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # ID_TUGAS
        self.layoutidTugas = QHBoxLayout()
        self.llbidTugas = QLabel("No Tugas")
        self.llbidTugas.setObjectName("idtugas")
        self.layoutidTugas.addWidget(self.llbidTugas)
        self.ldidTugas = QLineEdit()
        self.ldidTugas.setObjectName("self.ldidTugas")
        self.ldidTugas.setPlaceholderText("Nomor Tugas")
        self.layoutidTugas.addWidget(self.ldidTugas)
        layout.addLayout(self.layoutidTugas)

        # ID_MK
        layoutIdMk = QHBoxLayout()
        self.lbMkTugas = QLabel("Id Mata Kuliah")
        self.lbMkTugas.setObjectName("idMk")
        layoutIdMk.addWidget(self.lbMkTugas)
        self.spMk = QComboBox()
        # ini query mengambil id_mk bersarkan username atau berdasarkan matakuliah sesuai dengan dosennya
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
            SELECT datamatakuliah.ID_MK 
    FROM datamatakuliah 
    JOIN matakuliah ON datamatakuliah.ID_MK = matakuliah.ID_MK
    JOIN logindosen ON datamatakuliah.NIP_Dosen = logindosen.Username
    WHERE logindosen.Username = %s;
"""
        curse.execute(query,(username,))
        ambildata = curse.fetchall()

        # Jika data ditemukan, tampilkan di combobox
        if ambildata:
            for row in ambildata:
                id_mk = row[0]
                self.spMk.addItem(id_mk)
        else:
            print("Tidak ada data yang ditemukan untuk username:", username)
        
        # menambah kontent didalam layout id_mk
        layoutIdMk.addWidget(self.spMk)

        # menambhkn layout idmk didalam layout utama
        layout.addLayout(layoutIdMk)

        # JDL TUGAS
        layoutjdlTugas = QHBoxLayout()
        self.lbjdlTugas = QLabel("Judul Tugas")
        self.lbjdlTugas.setObjectName("jdltugas")
        layoutjdlTugas.addWidget(self.lbjdlTugas)
        self.ldjdlTugas = QLineEdit()
        self.ldjdlTugas.setObjectName("jdlldtugas")
        self.ldjdlTugas.setPlaceholderText("Judul Tugas")
        layoutjdlTugas.addWidget(self.ldjdlTugas)
        layout.addLayout(layoutjdlTugas)

        # DESKRIPSI TUGAS
        layoutDSTugas = QHBoxLayout()
        self.lbDSTugas = QLabel("Deskripsi tugas")
        self.lbDSTugas.setObjectName("jdltugas")
        layoutDSTugas.addWidget(self.lbDSTugas)
        self.ldDSTugas = QLineEdit()
        self.ldDSTugas.setObjectName("DSldtugas")
        self.ldDSTugas.setPlaceholderText("Deskripsi Tugas")
        layoutDSTugas.addWidget(self.ldDSTugas)
        layout.addLayout(layoutDSTugas)

        # TANGGAL PEMBERIAN
        layoutTglMl = QHBoxLayout()
        self.lbtglml = QLabel("Tanggal Pemberian")
        layoutTglMl.addWidget(self.lbtglml)
        self.tglmulai = QDateTimeEdit()
        self.tglmulai.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        ambilWaktuSekarang = QDateTime.currentDateTime()
        self.tglmulai.setDateTime(ambilWaktuSekarang)
        layoutTglMl.addWidget(self.tglmulai)
        layout.addLayout(layoutTglMl)

        # TANGGAL DEADLINE
        layoutTglEnd = QHBoxLayout()
        self.lbtglend = QLabel("Tanggal Pegumpulan")
        layoutTglEnd.addWidget(self.lbtglend)
        self.tglEnd = QDateTimeEdit()
        self.tglEnd.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.tglEnd.setDateTime(ambilWaktuSekarang)
        layoutTglEnd.addWidget(self.tglEnd)
        layout.addLayout(layoutTglEnd)

        # btn add
        btnTambah = QPushButton("Tambah")
        btnTambah.setObjectName("btnTambahTugas")
        layout.addWidget(btnTambah)
        btnTambah.clicked.connect(self.tambah)

        # layoutDSTugas.addStretch()
        layout.addStretch()
        self.setLayout(layout)
        
    # membuat method tambah
    def tambah (self):
        # membuat variabel yang menampung isi dari variabel sebelumnya
        idtgs = self.ldidTugas.text()
        idmk = self.spMk.currentText()
        jdl = self.ldjdlTugas.text()
        idDsMk = self.ldDSTugas.text()
        idtglml = self.tglmulai.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        idtglend = self.tglEnd.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        # ini analogi jika salah satu widget yang didalam alaman tersebut tidka terisi maka akan menimbulkan pesan
        if not idtgs or not idmk or not jdl or not idDsMk or not idtglml or not idtglend:
            QMessageBox.warning(self, "Peringatan", "Lengkapi semua data sebelum menambahkan tugas.")
            return
        
        # jika widget widget tersebut telah terisi semua maka akan menambhakan data kedalam database table tugas
        else:    
            
            # ini menghubungkan ke database
            conection, curse = buat_koneksi()
            curse = conection.cursor()
            
            # ini query untuk menambahkan tugas 
            query = ("INSERT INTO tugas (id_tugas, id_mk, judul_tugas,deskripsi_tugas, tanggal_pemberian, tanggal_pengumpulan) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")
            
            # ini mengambil data yang telah diisikan didalam widget tersebut
            ambil = (idtgs, idmk, jdl, idDsMk, idtglml, idtglend)
            
            # setelah itu ambil perintah query dan ambil data 
            curse.execute(query, ambil)
            
            # ini memperbaharui databases
            conection.commit()
            
            # pesan jika tugas telah berhasil ditambahkan 
            QMessageBox.information(self,"Berhasil","Tugas berhasil DItambahkan")

            # ini memnggil update table tugas sehingga tugas yang telah ditambahkan langsung terload didalam
            self.parentt.updateDataTableTugas(self.username)

            # ini menghapus widget widget ketika sudah ditamabhkan
            self.ldidTugas.clear()
            self.ldDSTugas.clear()
            self.tglmulai.setDateTime(QDateTime.currentDateTime())
            self.tglEnd.setDateTime(QDateTime.currentDateTime())
            
            # ini mengcolse halaman tambah tugas
            self.close()

# halaman edit data tugas
class HalamanEdittugas(QWidget):
    def __init__(self,id_tugas,username, windows = None):
        super().__init__()
        self.id_tugas = id_tugas
        self.windows = windows
        self.username = username
        
        layout = QVBoxLayout()
        #  ID_TUGAS
        self.layoutidTugas = QHBoxLayout()
        self.llbidTugas = QLabel("No Tugas")
        self.llbidTugas.setObjectName("idtugas")
        self.layoutidTugas.addWidget(self.llbidTugas)
        # ld id_tugas
        self.ldidTugas = QLineEdit()
        self.ldidTugas.setObjectName("self.ldidTugas")
        self.ldidTugas.setPlaceholderText("Judul Tugas")
        self.layoutidTugas.addWidget(self.ldidTugas)
        layout.addLayout(self.layoutidTugas)

        # JDL TUGAS
        layoutjdlTugas = QHBoxLayout()
        # label lbjdltugas
        self.lbjdlTugas = QLabel("Judul Tugas")
        self.lbjdlTugas.setObjectName("jdltugas")
        layoutjdlTugas.addWidget(self.lbjdlTugas)
        # line eidt judul tugas
        self.ldjdlTugas = QLineEdit()
        self.ldjdlTugas.setObjectName("jdlldtugas")
        self.ldjdlTugas.setPlaceholderText("Judul Tugas")
        layoutjdlTugas.addWidget(self.ldjdlTugas)
        layout.addLayout(layoutjdlTugas)

        # DESKRIPSI TUGAS
        layoutDSTugas = QHBoxLayout()
        self.lbDSTugas = QLabel("Deskripsi tugas")
        self.lbDSTugas.setObjectName("jdltugas")
        layoutDSTugas.addWidget(self.lbDSTugas)
        self.ldDSTugas = QLineEdit()
        self.ldDSTugas.setObjectName("DSldtugas")
        self.ldDSTugas.setPlaceholderText("Deskripsi Tugas")
        layoutDSTugas.addWidget(self.ldDSTugas)
        layout.addLayout(layoutDSTugas)

        # TANGGAL PEMBERIAN
        layoutTglMl = QHBoxLayout()
        self.lbtglml = QLabel("Tanggal Pemberian")
        layoutTglMl.addWidget(self.lbtglml)
        self.tglmulai = QDateTimeEdit()
        self.tglmulai.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layoutTglMl.addWidget(self.tglmulai)
        layout.addLayout(layoutTglMl)

        # TANGGAL DEADLINE
        layoutTglEnd = QHBoxLayout()
        self.lbtglend = QLabel("Tanggal Pegumpulan")
        layoutTglEnd.addWidget(self.lbtglend)
        self.tglEnd = QDateTimeEdit()
        self.tglEnd.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layoutTglEnd.addWidget(self.tglEnd)
        layout.addLayout(layoutTglEnd)

        # btn add
        btnTambah = QPushButton("Simpan")
        btnTambah.setObjectName("btnTambahTugas")
        layout.addWidget(btnTambah)
        btnTambah.clicked.connect(partial(self.simpan, id_tugas=self.id_tugas))

        connection , curse = buat_koneksi()
        curse = connection.cursor()

        # query untuk mengambil data lama
        query_old = """
            SELECT 
                tugas.ID_Tugas,
                tugas.judul_tugas,
                tugas.Deskripsi_Tugas,
                tugas.Tanggal_Pemberian,
                tugas.Tanggal_Pengumpulan
            FROM tugas WHERE tugas.id_tugas = %s;

"""
        curse.execute(query_old, (id_tugas,))
        ambildata = curse.fetchall()
        if ambildata:
            id_tugas, judul_tugas, deskripsi_tugas, tanggalMulai, tanggaldeadline = ambildata[0]
            self.ldidTugas.setText(id_tugas)
            self.ldjdlTugas.setText(judul_tugas)
            self.ldDSTugas.setText(deskripsi_tugas)
            # Konversi datetime ke string dan set ke QDateTimeEdit
            self.tglmulai.setDateTime(tanggalMulai)
            self.tglEnd.setDateTime(tanggaldeadline)

        # layoutDSTugas.addStretch()
        layout.addStretch()
        self.setLayout(layout)
    
    def simpan(self, id_tugas):
        # Ambil data yang baru dimasukkan oleh pengguna
        # Ambil ID tugas baru dari QLineEdit
        id_tugas_baru = self.ldidTugas.text()
         # Ambil judul tugas dari QLineEdit
        judul_tugas = self.ldjdlTugas.text()
        # Ambil deskripsi tugas dari QLineEdit 
        deskripsi_tugas = self.ldDSTugas.text()  
        # Format tanggal mulai
        tgl_mulai = self.tglmulai.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        # Format tanggal mulai  
        tgl_akhir = self.tglEnd.dateTime().toString("yyyy-MM-dd HH:mm:ss")  

        # Validasi input pengguna
        if not id_tugas_baru or not judul_tugas or not deskripsi_tugas:
            QMessageBox.warning(self, "Peringatan", "Semua kolom wajib diisi.")
            return
        else:
            # Membuat koneksi ke database
            connection, curse = buat_koneksi()

            # Ambil data lama untuk perbandingan
            query_check = """
                    SELECT 
                        tugas.ID_Tugas,
                        tugas.judul_tugas,
                        tugas.Deskripsi_Tugas,
                        tugas.Tanggal_Pemberian,
                        tugas.Tanggal_Pengumpulan
                    FROM tugas
                    WHERE tugas.ID_Tugas = %s;
                """
            curse.execute(query_check, (id_tugas,))
            datalama = curse.fetchone()

            if datalama:
                old_id_tugas, old_judul, old_deskripsi, old_tgl_mulai, old_tgl_akhir = datalama
                # Periksa apakah ada perubahan data
                if (id_tugas_baru != old_id_tugas or judul_tugas != old_judul or deskripsi_tugas != old_deskripsi or tgl_mulai != old_tgl_mulai or tgl_akhir != old_tgl_akhir):
                        # Lakukan update jika ada perubahan
                        query_update = """
                            UPDATE tugas
                            SET ID_Tugas = %s, judul_tugas = %s, Deskripsi_Tugas = %s,
                                Tanggal_Pemberian = %s, Tanggal_Pengumpulan = %s
                            WHERE ID_Tugas = %s;
                        """
                        curse.execute(query_update, (id_tugas_baru, judul_tugas, deskripsi_tugas, tgl_mulai, tgl_akhir, id_tugas))
                        connection.commit()
                        QMessageBox.information(self, "Informasi", "Data berhasil diperbarui.")
                        self.close()
                        self.windows.updateDataTableTugas(self.username)


# halaman view nama mahasiswa kumpulkan tugas
class HalamanView(QWidget):
    def __init__(self,username,id_tugas):
        super().__init__()
        self.username = username
        self.id_tugas = id_tugas
        self.setWindowTitle("Detail Tugas")
        # mengatur ukuran window
        self.setFixedSize(500, 400) 
        
        # MEMBUAT LAYOUT UNTUK HALAMAN 
        self.layout = QVBoxLayout()

        # ini judul  
        self.judul = QLabel("Daftar Pengumpulan Tugas")
        self.judul.setObjectName("lbjudul")
        
        # ini membuat garis untuk pemisah
        frameLine = QFrame()
        frameLine.setObjectName("garis")
        frameLine.setFrameShape(QFrame.HLine)
        frameLine.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.judul)
        self.layout.addWidget(frameLine)

        # ini membuat table daftar mahasiswa yang menggumpulkan tugas
        self.tableViewMahasiswa = QTableWidget()
        self.tableViewMahasiswa.setColumnCount(7)
        self.tableViewMahasiswa.setHorizontalHeaderLabels(["Id Pengumpulan","Nama Kuliah","Nim Mahasiswa","Nama Mahasiswa","Deskripsi Tugas","Tanggal Pengumpulan","Action"])
        self.tableViewMahasiswa.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.tableViewMahasiswa)

        # UNTUK MELIHAT LAYOUT ATAU MEMANGGIL LAYOUT
        self.setLayout(self.layout)
        self.TableDaftarPengumpulanTugas()
    

    # ini table daftar mahasiswa yang mengumpulkan tugas
    def TableDaftarPengumpulanTugas(self):
    # Buat koneksi dan cursor
        connection, curse = buat_koneksi()
        curse = connection.cursor()

        # Query untuk mengambil data tugas
        query = """
            SELECT 
                pengumpulantugas.id_pengumpulan,
                matakuliah.nama_mk,
                datamahasiswa.nim,
                datamahasiswa.nama,
                tugas.deskripsi_tugas,
                pengumpulantugas.tanggal_pengumpulan
            FROM pengumpulantugas
            JOIN matakuliah ON pengumpulantugas.id_mk = matakuliah.id_mk
            JOIN datamahasiswa ON pengumpulantugas.nim = datamahasiswa.nim
            JOIN tugas ON pengumpulantugas.id_tugas = tugas.id_tugas
            JOIN logindosen ON matakuliah.NIP_Dosen = logindosen.Username
            WHERE logindosen.Username = %s AND tugas.id_tugas = %s;
        """
        
        # Eksekusi query
        curse.execute(query, (self.username,self.id_tugas))
        ambildata = curse.fetchall()  # Mengambil semua baris data, bukan hanya satu baris
        # Cek jika data ditemukan
        if ambildata:
            self.tableViewMahasiswa.setRowCount(len(ambildata))  # Menentukan jumlah baris di QTableWidget
            for barisnumber, barisData in enumerate(ambildata):
                for col, data in enumerate(barisData):
                    self.tableViewMahasiswa.setItem(barisnumber, col, QTableWidgetItem(str(data)))
                
                # Menambahkan tombol 'View' pada kolom 6 (kolom terakhir)
                self.btnView = QPushButton("View")
                # mengambil nim dikolom 2
                nim = barisData[2]

                # ini mengambil id_pengumpulan dikolom 0
                id_pengumpulan = barisData[0]
                
                self.btnView.clicked.connect(partial(self.halamanViewFileTugas, nim, id_pengumpulan))
                # self.btnView.clicked.connect(partial(self.halamanViewFileTugas))  # Pastikan Anda memiliki fungsi halamanView
                
                self.tableViewMahasiswa.setCellWidget(barisnumber, 6, self.btnView)

            # Menyesuaikan lebar kolom agar muat dengan konten
            self.tableViewMahasiswa.resizeColumnsToContents()
    
    def halamanViewFileTugas(self, nim, id_pengumpulan):
        print(f"halamanViewFileTugas called with NIM: {nim}, ID Pengumpulan: {id_pengumpulan}")
        self.showHalamanfileTugasMhs = HalamanFileTugasMhs(nim, id_pengumpulan)
        self.showHalamanfileTugasMhs.show()

# halaman file tugas mahasiswa
class HalamanFileTugasMhs(QWidget):
    def __init__(self, nim, id_pengumpulan):
        super().__init__()
        self.setWindowTitle("Detail File Tugas")
        self.setFixedSize(400, 300)
        
        # Layout utama
        layout = QVBoxLayout()
        
        
        # Widget untuk menampilkan data
        self.lbNama = QLabel("Nama Mahasiswa:")
        self.lbNim = QLabel("NIM Mahasiswa:")
        self.lbdeskripsiTugas = QLabel("Deskripsi Tugas:")
        self.fileTugas = QPlainTextEdit()
        self.fileTugas.setReadOnly(True)
        
        # ini menambahkann content content didalam layout
        layout.addWidget(self.lbNama)
        layout.addWidget(self.lbNim)
        layout.addWidget(self.lbdeskripsiTugas)
        layout.addWidget(QLabel("Isi File Tugas:"))
        layout.addWidget(self.fileTugas)
        
        self.setLayout(layout)
        
        # Tampilkan dile tugas  berdasarkan NIM dan ID Pengumpulan
        self.tampilkan_file(nim, id_pengumpulan)

    def tampilkan_file(self, nim, id_pengumpulan):
        connection, curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT 
                    datamahasiswa.nama,
                    pengumpulantugas.nim,
                    tugas.deskripsi_tugas,
                    pengumpulantugas.file_tugas 
                FROM pengumpulantugas
                JOIN datamahasiswa ON pengumpulantugas.nim = datamahasiswa.nim
                join tugas on tugas.id_tugas = pengumpulantugas.id_tugas
                WHERE pengumpulantugas.nim = %s AND pengumpulantugas.id_pengumpulan = %s;
            """
        curse.execute(query, (nim, id_pengumpulan))
        data = curse.fetchone()
        # ini mengambil data didalam dtaabses
        if data:
                nama, nim, deskripsi_tugas,file_tugas = data
                self.lbNama.setText(f"Nama Mahasiswa: {nama}")
                self.lbNim.setText(f"NIM Mahasiswa: {nim}")
                self.lbdeskripsiTugas.setText(f"Deskripsi Tugas: {deskripsi_tugas}")
                self.fileTugas.setPlainText(f"{file_tugas}")

class HalamanSetting(QWidget):
    def __init__(self, username,password):
        super().__init__()
        self.username = username  # Simpan username di atribut instance
        self.password = password
        print(self.password)
        self.setWindowTitle("Halaman Pengaturan")
        self.setFixedSize(300, 350)
        layout = QVBoxLayout()

        # Membuat tab
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)

        # Menambahkan tab di dalam tabs(QTabWidget)
        tabs.addTab(self.user(self.username), "Profile")
        tabs.addTab(self.changePw(self.username,self.password), "Change Password")

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
        fotouser = QPixmap(os.path.join(basedir, "../MAHASISWA/gambarMahasiswa/13.png"))
        foto.setPixmap(fotouser)
        foto.setAlignment(Qt.AlignCenter)
        layout.addWidget(foto)

        # Layout Nama
        layoutHNama = QHBoxLayout()
        self.lbNama = QLabel("Nama")
        self.lbNama.setStyleSheet("margin-right: 15px")
        self.ldNama = QLineEdit()
        self.ldNama.setEnabled(False)
        layoutHNama.addWidget(self.lbNama)
        layoutHNama.addWidget(self.ldNama)

        # Layout Nim
        layoutHNip = QHBoxLayout()
        self.lbNip = QLabel("Nip")
        self.lbNip.setStyleSheet("margin-right : 25px")
        self.ldNip = QLineEdit()
        self.ldNip.setEnabled(False)
        layoutHNip.addWidget(self.lbNip)
        layoutHNip.addWidget(self.ldNip)

        # Layout Username
        layoutHUsername = QHBoxLayout()
        self.lbUsername = QLabel("Username")
        self.lbUsername.setStyleSheet("margin-right : 5px")
        self.ldUsername = QLineEdit()
        self.ldUsername.setEnabled(False)
        layoutHUsername.addWidget(self.lbUsername)
        layoutHUsername.addWidget(self.ldUsername)

        # Menambahkan layout ke dalam layout utama
        layout.addLayout(layoutHNama)
        layout.addLayout(layoutHNip)
        layout.addLayout(layoutHUsername)

        self.ambilDataUser(username)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def ambilDataUser(self, username):
        connection, curse = buat_koneksi()
        curse = connection.cursor()

        query = """
            SELECT dosen.nama_dosen,dosen.nip_dosen, logindosen.username
                        FROM dosen
                        JOIN logindosen ON dosen.nip_dosen = logindosen.username
                        WHERE logindosen.username = %s; 
        """
        curse.execute(query, (username,))
        ambildata = curse.fetchall()
        if ambildata:
            nama,nip,username = ambildata[0]
            self.ldNama.setText(nama)
            self.ldNip.setText(nip)
            self.ldUsername.setText(username)

    def changePw(self,username,password):
        layout = QVBoxLayout()

        # Layout Username
        layoutHUsernamePw = QHBoxLayout()
        self.lbUsernamePw = QLabel("Username")
        self.lbUsernamePw.setStyleSheet("margin-right : 58px")
        self.ldUsernamePw = QLineEdit()
        self.ldUsernamePw.setEnabled(False)
        layoutHUsernamePw.addWidget(self.lbUsernamePw)
        layoutHUsernamePw.addWidget(self.ldUsernamePw)


        # Layout password
        layoutHOldPw = QHBoxLayout()
        self.lbOldPw = QLabel("Old Password")
        self.lbOldPw.setStyleSheet("margin-right : 36px")
        self.ldOldPw = QLineEdit()
        self.ldOldPw.setEchoMode(QLineEdit.Password)
        layoutHOldPw.addWidget(self.lbOldPw)
        layoutHOldPw.addWidget(self.ldOldPw)

        connection, curse = buat_koneksi()
        curse = connection.cursor()

        # Menyesuaikan query untuk mendapatkan username dan password
        query = """
            SELECT username FROM logindosen 
            WHERE username = %s AND password = %s
        """
        curse.execute(query, (username, password))  # Menggunakan dua parameter sesuai query
        ambildata = curse.fetchone()

        if ambildata:
            self.ldUsernamePw.setText(ambildata[0])  # Menampilkan username
            # self.ldOldPw.setText(password)  # Menampilkan password lama

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
        self.edit.clicked.connect(partial(self.simpan, username, password))

        # Menambahkan layout ke dalam layout utama
        layout.addLayout(layoutHUsernamePw)
        layout.addLayout(layoutHOldPw)
        layout.addLayout(layoutHPw)
        layout.addLayout(layoutHKonfirPw)
        layout.addWidget(self.edit)

        container = QWidget()
        container.setLayout(layout)
        return container

    def simpan(self,username,password):
        connection, curse = buat_koneksi()
        curse = connection.cursor()

        query_check = """
            select * from logindosen where logindosen.username = %s and logindosen.password = %s;
"""
        curse.execute(query_check,(username,password))
        ambildata = curse.fetchone()

        if ambildata:
            username = ambildata[0]
            password = ambildata[1]
            self.ldUsernamePw.setText(username)
            # self.ldOldPw.setText(password)

        username = self.ldUsernamePw.text()
        password1 = self.ldOldPw.text()
        pw = self.ldPw.text()
        konfirPw = self.ldKonfirPw.text()

        if not password or not pw or not konfirPw:
            QMessageBox.warning(self, "Warning", "tolong lengkapi data!")
        elif password1 != password:
            QMessageBox.warning(self, "Warning", "Password lama salah!")
        elif pw != konfirPw:
            QMessageBox.warning(self, "Warning", "Password baru dan Konfirmasi password tidak sama!")
            return  # Keluar jika tidak sama
        else:
            query = """
                UPDATE logindosen SET password = %s WHERE username = %s;
            """
            curse.execute(query, (pw, self.username))  # Gunakan self.username untuk update
            connection.commit()
            QMessageBox.information(self, "Berhasil", "Password berhasil diubah!")
            self.ldOldPw.clear()
            self.ldPw.clear()
            self.ldKonfirPw.clear()
         