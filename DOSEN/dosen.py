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
    QDialog,
    QFrame,
    QTableWidget,
    QFileDialog,
    QComboBox,
    QDateTimeEdit,
    QSpinBox,
    QTableWidgetItem,
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

        # Tambahkan action Data User di sebelah kanan
        datauser = QAction(
            QIcon(os.path.join(basedir, "./userhh.png")),
            "User",self
        )
        datauser.triggered.connect(self.show_datauser)

        self.toolbar.addAction(datauser)
        setting = QAction(
            QIcon(os.path.join(basedir, "./image.png")),
            "Setting",self
        )
        self.toolbar.addAction(setting)
        setting.triggered.connect(self.show_setting)
        

        exit = QAction(
            QIcon(os.path.join(basedir, "./langout.png")),
            "Langout",self
        )
        self.toolbar.addAction(exit)
        exit.triggered.connect(self.langout)

        # Mengatur layout untuk widget utama
        self.setLayout(self.layoutMHS)

    # sedangkan ini memanggil file style.qss
    def styleqss(self):
        qss_file = os.path.join(basedir, "./dosen.qss")
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
        self.tableTugas.setColumnCount(6)
        self.tableTugas.setHorizontalHeaderLabels(["Id Tugas","kode matakuliah","Deskripsi Tugas","Tanggal Pemberian","Tanggal Deadline","Action"])
        self.tableTugas.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.tableTugas)

        self.layout.addStretch()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.updateDataTableTugas()
    
    def show_AddTugas(self):
        self.showAddTugas = HalamanAddtugas(self)
        self.showAddTugas.show()

    def show_datauser(self):
        self.showAddTugas = DataUser(self.username)
        self.showAddTugas.show()

    def updateDataTableTugas(self):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = (
            "SELECT tugas.id_tugas, tugas.id_mk, tugas.deskripsi_tugas, "
            "tugas.tanggal_pemberian, tugas.tanggal_pengumpulan FROM tugas"
        )
        curse.execute(query)
        ambildata = curse.fetchall()
        if ambildata:
            self.tableTugas.setRowCount(len(ambildata))
            for barisnumber, barisData in enumerate(ambildata):
                for col, data in enumerate(barisData):
                    self.tableTugas.setItem(barisnumber, col, QTableWidgetItem(str(data)))
                    self.btnView = QPushButton(" View")
                    self.btnView.clicked.connect(self.halamanView)
                    self.btnView.setProperty("row",barisnumber)
                    self.tableTugas.setCellWidget(barisnumber, 5, self.btnView)
            self.tableTugas.resizeColumnsToContents()
        else:
            QMessageBox.information(self, "Info", "Tidak ada data yang ditemukan di tabel tugas.")

    

    def halamanView(self):
        row = self.sender().property("row")  # Get row number from the clicked button
        task_id = self.tableTugas.item(row, 0).text()  # Get the task ID from the table
        self.showView = HalamanView()
        self.showView.set_task_data(task_id)  # Pass task ID to the view page
        self.showView.show()



    def show_setting(self):
        self.showSetting = HalamanSetting(self.username)

        self.showSetting.show()


    def langout(self):
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
                SELECT datadosen.nip,datadosen.nama
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
                nip,nama = ambildata
                self.lb2Nim.setText(f'Nim            : {nip}')
                self.lb2Nama.setText(f'Nama         : {nama}')
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
class HalamanSetting(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set layout
        self.layout = QVBoxLayout()

        # Label untuk Halaman Pengaturan
        self.label_title = QLabel("Pengaturan Akun")
        self.layout.addWidget(self.label_title)

        # Input untuk mengganti password
        self.label_password = QLabel("Ganti Password:")
        self.layout.addWidget(self.label_password)
        
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)  # Untuk menyembunyikan input password
        self.layout.addWidget(self.input_password)
        
        # Tombol untuk menyimpan perubahan password
        self.btn_save_password = QPushButton("Simpan Password")
        self.btn_save_password.clicked.connect(self.ganti_password)
        self.layout.addWidget(self.btn_save_password)

        # Tombol untuk logout
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.clicked.connect(self.logout)
        self.layout.addWidget(self.btn_logout)

        # Set layout ke widget
        self.setLayout(self.layout)
        
    def ganti_password(self):
        # Ambil password baru dari input
        new_password = self.input_password.text()
        
        # Validasi password (misalnya panjang minimal 6 karakter)
        if len(new_password) < 6:
            QMessageBox.warning(self, "Peringatan", "Password harus minimal 6 karakter.")
        else:
            # Simpan password baru (ini hanya contoh, proses sesungguhnya tergantung pada aplikasi Anda)
            # Di sini Anda bisa menyimpan password ke database atau file
            QMessageBox.information(self, "Sukses", "Password berhasil diganti.")
            self.input_password.clear()  # Kosongkan input setelah berhasil

    def logout(self):
        # Proses logout (misalnya kembali ke halaman login atau keluar dari aplikasi)
        QMessageBox.information(self, "Logout", "Anda telah logout.")
        # Di sini bisa menambahkan kode untuk kembali ke halaman login atau keluar dari aplikasi.
        self.close()  # Tutup halaman pengaturan

    
    # halaman view nama mahasiswa kumpulkan tugas
class HalamanView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detail Tugas")
        self.setFixedSize(500, 400)  # Adjusted size to accommodate the table
        
        # Create a layout for the page
        self.layout = QVBoxLayout()
        
        # Create a table widget to display the task details
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)

        # Add a button to close the view
        btnClose = QPushButton("Tutup")
        btnClose.clicked.connect(self.close_view)
        self.layout.addWidget(btnClose)

        # Set the layout
        self.setLayout(self.layout)

    def set_task_data(self, tugas_id):
        """Set task details based on the task ID."""
        connection, cursor = buat_koneksi()  # Assuming buat_koneksi returns a valid connection and cursor
        try:
            query = """
                SELECT m.nama, m.nim, t.id_tugas, mk.nama, t.deskripsi_tugas, t.tanggal_pemberian, t.tanggal_deadline, s.nama
                FROM tugas t
                JOIN mata_kuliah mk ON t.id_mk = mk.id_mk
                JOIN mahasiswa m ON t.id_mahasiswa = m.id_mahasiswa
                LEFT JOIN pengumpulan_tugas pt ON pt.id_tugas = t.id_tugas
                LEFT JOIN mahasiswa s ON pt.id_mahasiswa = s.id_mahasiswa
                WHERE t.id_tugas = %s
            """
            cursor.execute(query, (tugas_id,))
            task_data = cursor.fetchone()

            if task_data:
                # Unpack task data correctly (8 values)
                nama_mahasiswa, nim, tugas_id, matakuliah, deskripsi, tgl_pemberian, tgl_deadline, nama_pengumpul = task_data

                # Formatting dates for better display
                tgl_pemberian = QDate.fromString(tgl_pemberian, "yyyy-MM-dd").toString("dd MMM yyyy")
                tgl_deadline = QDate.fromString(tgl_deadline, "yyyy-MM-dd").toString("dd MMM yyyy")

                # Set up the table
                self.tableWidget.setRowCount(8)  # One row per task detail + student who submitted
                self.tableWidget.setColumnCount(2)  # Two columns: label and data
                
                # Set the headers
                self.tableWidget.setHorizontalHeaderLabels(["Detail", "Informasi"])

                # Insert task details into the table
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
                
                # Populate the table with details
                for row, (label, value) in enumerate(details):
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(label))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(value))

                # Adjust column widths for better readability
                self.tableWidget.setColumnWidth(0, 150)  # Adjust column width for labels
                self.tableWidget.setColumnWidth(1, 300)  # Adjust column width for data

            else:
                QMessageBox.warning(self, "Tidak Ditemukan", "Tugas tidak ditemukan.")
                self.tableWidget.clear()  # Clear table if no task found
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def close_view(self):
        """Close the view page."""
        self.close()