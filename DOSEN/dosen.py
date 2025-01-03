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
    QTabWidget
)
from PySide6.QtCore import QSize, Qt,QDate,QDateTime
from PySide6.QtGui import QAction, QIcon,QPixmap
# from databases.database_main import database
from DATABASE.databse import buat_koneksi
basedir = os.path.dirname(__file__)

class HalamanDosen(QMainWindow):
    def __init__(self,username):
        super().__init__()
        # self.setWindowTitle("Mahasiswa")
        self.username = username  # Simpan username
        self.setWindowTitle(f"Selamat Datang, {self.username}")
        self.setFixedSize(600,400)

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
            QIcon(os.path.join(basedir, "./image.png")),
            "Setting",self
        )
        self.toolbar.addAction(setting)
        setting.triggered.connect(self.show_setting)
        

        exit = QAction(
            QIcon(os.path.join(basedir, "./logout.png")),
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
        self.layout = QVBoxLayout()
        judul = QLabel("Dashboard")
        
        frameLine = QFrame()
        frameLine.setFrameShape(QFrame.HLine)
        frameLine.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(judul)
        self.layout.addWidget(frameLine)

        tanggal = QDate.currentDate()
        fromat = tanggal.toString("dddd dd - MMMM - yyyy")
        lbTanggal = QLabel(fromat)
        self.layout.addWidget(lbTanggal)

        btnAdd = QPushButton("  Add")
        btnAdd.setObjectName("add")
        btnAdd.setFixedSize(90,30)
        gambarBtnadd = os.path.join(basedir,"","add.png")
        btnAdd.setIcon(QIcon(gambarBtnadd))
        btnAdd.setIconSize(QSize(20,20))
        btnAdd.clicked.connect(self.show_AddTugas)
        self.layout.addWidget(btnAdd)


        self.tableTugas = QTableWidget()
        self.tableTugas.setColumnCount(7)
        self.tableTugas.setHorizontalHeaderLabels(["Id Tugas","kode matakuliah","Nama Kuliah","Deskripsi Tugas","Tanggal Pemberian","Tanggal Deadline","Action"])
        self.tableTugas.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.tableTugas)

        self.layout.addStretch()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.updateDataTableTugas(self.username)
    
    # ini fungsi untuk memnggil class halaman tambah tugas
    def show_AddTugas(self):
        self.showAddTugas = HalamanAddtugas(self)
        self.showAddTugas.show()

    def updateDataTableTugas(self,username):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
           SELECT 
                tugas.ID_Tugas,
                tugas.ID_MK,
                matakuliah.Nama_MK,
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
                    self.btnView = QPushButton(" View")
                    self.btnView.clicked.connect(self.halamanView)
                    self.btnView.setProperty("row",barisnumber)
                    self.tableTugas.setCellWidget(barisnumber, 6, self.btnView)
            self.tableTugas.resizeColumnsToContents()
        else:
            QMessageBox.information(self, "Info", "Tidak ada data yang ditemukan di tabel tugas.")

    
    # ini fungsi untuk menampilkan halaman view
    # def halamanView(self):
    #     # # mendapatkan baris dari button yang diclik
    #     # row = self.sender().property("row") 
    #     # # menamdapatkan id tugas dari table
    #     # task_id = self.tableTugas.item(row, 0).text()  
    #     # self.showView = HalamanView()
    #     # # lewati id tugas untuk melihat (view) halaman
    #     # self.showView.mengaturDataTugas(task_id)
    #     # self.showView.show()
    #     self.showHalamanView = HalamanView()
    #     self.showHalamanView.show()


    # menampilkan halaman setting
    def show_setting(self):
        self.showSetting = HalamanSetting(self.username)
        self.showSetting.show()

    # ini fungsi untuk logout
    def logout(self):
        massage = QMessageBox.question(self,"Pertanyaa","Apakah anda ingin keluar dari aplikasi ? ", QMessageBox.Yes | QMessageBox.No)
        if massage == QMessageBox.Yes:
                    self.close()
                    print("aplikasi di close")

    def halamanView(self):
         self.showView = HalamanView()
         self.showView.show()


class HalamanAddtugas(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Halaman Tambah Tugas")
        self.setFixedSize(300,350)
        container = QWidget()
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
        self.ldidTugas.setPlaceholderText("Judul Tugas")
        self.layoutidTugas.addWidget(self.ldidTugas)
        layout.addLayout(self.layoutidTugas)

        # ID_MK
        layoutIdMk = QHBoxLayout()
        self.lbMkTugas = QLabel("Id Mata Kuliah")
        self.lbMkTugas.setObjectName("idMk")
        layoutIdMk.addWidget(self.lbMkTugas)
        self.spMk = QComboBox()
        self.spMk.addItems(['NM','PPV'])
        layoutIdMk.addWidget(self.spMk)
        layout.addLayout(layoutIdMk)

        # JDL TUGAS
        layoutjdlTugas = QHBoxLayout()
        self.lbjdlTugas = QLabel("No Tugas")
        self.lbjdlTugas.setObjectName("jdltugas")
        layoutjdlTugas.addWidget(self.lbjdlTugas)
        self.ldjdlTugas = QLineEdit()
        self.ldjdlTugas.setObjectName("jdlldtugas")
        self.ldjdlTugas.setPlaceholderText("Judul Tugas")
        layoutjdlTugas.addWidget(self.ldjdlTugas)
        layout.addLayout(layoutjdlTugas)
        # layout.addLayout(layoutIdMk)

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
        layoutTglMl.addWidget(self.tglmulai)
        layout.addLayout(layoutTglMl)

        # TANGGAL DEADLINE
        layoutTglEnd = QHBoxLayout()
        self.lbtglend = QLabel("Tanggal Pegumpulan")
        layoutTglEnd.addWidget(self.lbtglend)
        self.tglEnd = QDateTimeEdit()
        layoutTglEnd.addWidget(self.tglEnd)
        layout.addLayout(layoutTglEnd)

        # btn add
        btnTambah = QPushButton("Tambah")
        layout.addWidget(btnTambah)
        btnTambah.clicked.connect(self.tambah)

        # layoutDSTugas.addStretch()
        layout.addStretch()

        self.setLayout(layout)
        # container.setLayout(layout)

    def tambah (self):
        idtgs = self.ldidTugas.text()
        idmk = self.spMk.currentText()
        idDsMk = self.ldDSTugas.text()
        idtglml = self.tglmulai.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        idtglend = self.tglEnd.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        if not idtgs or not idmk or not idDsMk or not idtglml or not idtglend:
            QMessageBox.warning(self, "Peringatan", "Lengkapi semua data sebelum menambahkan tugas.")
            return

        else:    
            conection, curse = buat_koneksi()
            curse = conection.cursor()
            query = ("INSERT INTO tugas (id_tugas, id_mk, deskripsi_tugas, tanggal_pemberian, tanggal_pengumpulan) "
                    "VALUES (%s, %s, %s, %s, %s)")
            ambil = (idtgs, idmk, idDsMk, idtglml, idtglend)
            curse.execute(query, ambil)
            conection.commit()
            QMessageBox.information(self,"Peringatan","Tugas berhasil DItambahkan")
        
            self.parent.updateDataTableTugas()
            self.ldidTugas.clear()
            self.ldDSTugas.clear()
            self.tglmulai.setDateTime(QDateTime.currentDateTime())
            self.tglEnd.setDateTime(QDateTime.currentDateTime())
    
    
# class DataUser(QWidget):
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

        # menambahkan semester
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
                SELECT datadosen.nip,datadosen.nama_dosen
                FROM datadosen 
                JOIN logindosen 
                ON datadosen.nip = logindosen.username 
                WHERE logindosen.username = %s;
            """
        
        curse.execute(query,(username,))

        # menampilkan usrname di consle
        print(username)

        ambildata = curse.fetchone()
        if ambildata:
                nip,nama_dosen = ambildata
                self.lb2Nim.setText(f'Nim            : {nip}')
                self.lb2Nama.setText(f'Nama         : {nama_dosen}')
                # self.lb2Jurusan.setText(f'Jurusan     : {jurusan}')
                # self.lb2Prodi.setText(f'Prodi          : {prodi}')
                # self.lb2Semester.setText(f'Semester  : {semester}')
        else:
                self.lb2Nim.setText(f"Data Tidak ditemukan")
                self.lb2Nama.setText("Data Tidak ditemukan")
                self.lb2Jurusan.setText("Data Tidak ditemukan")
                self.lb2Prodi.setText("Data Tidak ditemukan")
                self.lb2Semester.setText("Data Tidak ditemukan")


# halaman setting
# class HalamanSetting(QWidget):
#     def __init__(self):
#         super().__init__()
        
#         # Set layout
#         self.layout = QVBoxLayout()

#         # Label untuk Halaman Pengaturan
#         self.label_title = QLabel("Pengaturan Akun")
#         self.layout.addWidget(self.label_title)

#         # Input untuk mengganti password
#         self.label_password = QLabel("Ganti Password:")
#         self.layout.addWidget(self.label_password)
        
#         self.input_password = QLineEdit()
#         self.input_password.setEchoMode(QLineEdit.Password)  # Untuk menyembunyikan input password
#         self.layout.addWidget(self.input_password)
        
#         # Tombol untuk menyimpan perubahan password
#         self.btn_save_password = QPushButton("Simpan Password")
#         self.btn_save_password.clicked.connect(self.ganti_password)
#         self.layout.addWidget(self.btn_save_password)

#         # Tombol untuk logout
#         self.btn_logout = QPushButton("Logout")
#         self.btn_logout.clicked.connect(self.logout)
#         self.layout.addWidget(self.btn_logout)

#         # Set layout ke widget
#         self.setLayout(self.layout)
        
#     def ganti_password(self):
#         # Ambil password baru dari input
#         new_password = self.input_password.text()
        
#         # Validasi password (misalnya panjang minimal 6 karakter)
#         if len(new_password) < 6:
#             QMessageBox.warning(self, "Peringatan", "Password harus minimal 6 karakter.")
#         else:
#             # Simpan password baru (ini hanya contoh, proses sesungguhnya tergantung pada aplikasi Anda)
#             # Di sini Anda bisa menyimpan password ke database atau file
#             QMessageBox.information(self, "Sukses", "Password berhasil diganti.")
#             self.input_password.clear()  # Kosongkan input setelah berhasil

#     def logout(self):
#         # Proses logout (misalnya kembali ke halaman login atau keluar dari aplikasi)
#         QMessageBox.information(self, "Logout", "Anda telah logout.")
#         # Di sini bisa menambahkan kode untuk kembali ke halaman login atau keluar dari aplikasi.
#         self.close()  # Tutup halaman pengaturany

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
        fotouser = QPixmap(os.path.join(basedir,"./13.png"))
        foto.setPixmap(fotouser)
        foto.setAlignment(Qt.AlignCenter)
        layout.addWidget(foto)

        # layout nama
        layoutHNama = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbNama = QLabel("Nama")
        self.lbNama.setStyleSheet("margin-right: 15px")
        self.ldNama = QLineEdit()
        self.ldNama.setEnabled(False)
        layoutHNama.addWidget(self.lbNama)
        layoutHNama.addWidget(self.ldNama)

        # layout nip
        layoutHNip = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbNip = QLabel("Nip")
        self.lbNip.setStyleSheet("margin-right : 25px")
        self.ldNip = QLineEdit()
        self.ldNip.setEnabled(False)
        layoutHNip.addWidget(self.lbNip)
        layoutHNip.addWidget(self.ldNip)

        # layout nim
        layoutHUsername = QHBoxLayout()
        # ini content label dan line edit nama
        self.lbUsername = QLabel("Username")
        self.lbUsername.setStyleSheet("margin-right : 5px")
        self.ldUsername = QLineEdit()
        self.ldUsername.setEnabled(False)
        layoutHUsername.addWidget(self.lbUsername)
        layoutHUsername.addWidget(self.ldUsername)

        # ini membuat widget yang menampung layout vertikal
        widget = QWidget()
        layout.addLayout(layoutHNama)
        layout.addLayout(layoutHNip)
        layout.addLayout(layoutHUsername)


        # merapikan layout
        layoutHNama.setContentsMargins(4,4,4,4)
        layoutHNama.setSpacing(5)
        layoutHNip.setContentsMargins(4,4,4,4)
        layoutHNip.setSpacing(5)
        layoutHUsername.setContentsMargins(4,4,4,4)
        layoutHUsername.setSpacing(5)
        widget.setLayout(layout)
        self.ambilDataUser(username)
        return widget
    
    def ambilDataUser(self,username):
        connction,curse = buat_koneksi()
        curse = connction.cursor()
        query = """
                SELECT dosen.nama_dosen,dosen.nip_dosen, logindosen.username
            FROM dosen
            JOIN logindosen ON dosen.nip_dosen = logindosen.username
            WHERE logindosen.username = %s;       
                """
        curse.execute(query,(username,))
        ambildata = curse.fetchall()
        if ambildata:
            nama,nip,username = ambildata[0]
            self.ldNama.setText(nama)
            self.ldNip.setText(nip)
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
        self.ldUsernamePw.setEnabled(False)
        layoutHUsernamePw.addWidget(self.lbUsernamePw)
        layoutHUsernamePw.addWidget(self.ldUsernamePw)

        connection,curse = buat_koneksi()
        curse = connection.cursor()

        query = """
            select logindosen.username from logindosen where logindosen.username = %s;
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
        # self.edit.clicked.connect(self.simpan)

        # menambah layout didalam layout utama
        layout.addLayout(layoutHUsernamePw)
        layout.addLayout(layoutHPw)
        layout.addLayout(layoutHKonfirPw)
        layout.addWidget(self.edit) 

        container = QWidget()
        container.setLayout(layout)
        # self.simpan(username)
        return container

    
# halaman view nama mahasiswa kumpulkan tugas
class HalamanView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detail Tugas")
        # mengatur ukuran window
        self.setFixedSize(500, 400) 
        
        # MEMBUAT LAYOUT UNTUK HALAMAN 
        self.layout = QVBoxLayout()

        self.tableView = QTableWidget()
        self.tableView.setColumnCount(7)
        self.tableView.setHorizontalHeaderLabels(["Id Pengumpulan","Nama Kuliah","Nim Mahasiswa","Nama Mahasiswa","Deskripsi Tugas","Tanggal Pengumpulan","Action"])
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.tableView)
        
        # # MEMBUAT TABLE WIGET UNTUK MENUNJUKKAN DETAIL TUGAS 
        # self.tableWidget = QTableWidget()
        # self.layout.addWidget(self.tableWidget)

        # MENAMBAHKN BUTTON UNTUK MENUTUP VIEW
        btnClose = QPushButton("Tutup")
        btnClose.clicked.connect(self.close_view)
        self.layout.addWidget(btnClose)

        # UNTUK MELIHAT LAYOUT ATAU MEMANGGIL LAYOUT
        self.setLayout(self.layout)

    def mengaturDataTugas(self, tugas_id,username):
        """Set task details based on the task ID."""
        # koneksi kedalam databases
        connection, cursor = buat_koneksi()
        try:
            query = """
                SELECT 
                tugas.ID_Tugas,
                tugas.ID_MK,
                matakuliah.Nama_MK,
                tugas.Deskripsi_Tugas,
                tugas.Tanggal_Pemberian,
                tugas.Tanggal_Pengumpulan
            FROM tugas
            JOIN matakuliah ON tugas.ID_MK = matakuliah.ID_MK
            JOIN logindosen ON matakuliah.NIP_Dosen = logindosen.Username
            WHERE logindosen.Username = %s;
            """
            
            cursor.execute(query, (tugas_id,username))
            task_data = cursor.fetchall()

            if task_data:
                # membokar/megulik/mengkoreksi data tugas dengan benar (8 values)
                nama_mahasiswa, nim, tugas_id, matakuliah, deskripsi, tgl_pemberian, tgl_deadline, nama_pengumpul = task_data

                # mengatur format tanggal untuk tampilan ke 
                tgl_pemberian = QDate.fromString(tgl_pemberian, "yyyy-MM-dd").toString("dd MMM yyyy")
                tgl_deadline = QDate.fromString(tgl_deadline, "yyyy-MM-dd").toString("dd MMM yyyy")

                # menyiapkan table 
                self.tableWidget.setRowCount(8)  # satu baris per detail tugas + mahasiswa yang mengumpulkan 
                self.tableWidget.setColumnCount(2)  #dua colom : label dan data
                
                # menyiapkan header
                self.tableWidget.setHorizontalHeaderLabels(["Detail", "Informasi"])

                # menambah detail tugas ke dalam table
                details = [
                    ("Nama Mahasiswa", nama_mahasiswa),
                    ("NIM", nim),
                    ("ID Tugas", str(tugas_id)),
                    ("Mata Kuliah", matakuliah),
                    ("Deskripsi Tugas", deskripsi),
                    ("Tanggal Pemberian", tgl_pemberian),
                    ("Tanggal Deadline", tgl_deadline),
                    ("Pengumpul", nama_pengumpul if nama_pengumpul else "Belum Dikirim"),
                ]
                
                # mengisi table
                for row, (label, value) in enumerate(details):
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(label))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(value))

                # mengatur lebar kolom untuk tampilan baca yang lebih baik
                self.tableWidget.setColumnWidth(0, 150)  #menyesuaikan lebar kolom untuk label
                self.tableWidget.setColumnWidth(1, 300)  # menyesuailkan lebar colom untuk data 

            else:
                QMessageBox.warning(self, "Tidak Ditemukan", "Tugas tidak ditemukan.")
                self.tableWidget.clear() #membersihkan table jika tidak menemukan tugas
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def close_view(self):
        """Close the view page."""
        self.close()