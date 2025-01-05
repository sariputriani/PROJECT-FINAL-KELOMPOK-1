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
    QTabWidget,
    QSpinBox
)
from PySide6.QtCore import QSize, Qt,QDate,QDateTime
from PySide6.QtGui import QAction, QIcon,QPixmap
from functools import partial

# import modlu
from DATABASE.databse import buat_koneksi
basedir = os.path.dirname(__file__)

class HalamanMahasiswa(QMainWindow):
    def __init__(self,username,id_tugas=None,id_kegiatan=None):
        super().__init__()
        self.username = username  # Simpan username
        self.id_tugas = id_tugas
        self.id_kegiatan = id_kegiatan
        self.setWindowTitle(f"Selamat Datang, {self.username}")
        # self.setFixedSize(650,650)
        self.setGeometry(450,50,700,600)
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

        jadwalKuliah = QAction("Jadwal Kuliah", self)
        jadwalKuliah.setCheckable(True)
        self.toolbar.addAction(jadwalKuliah)
        jadwalKuliah.triggered.connect(self.DashboardJadwal)

        jadwalKegiatan = QAction("Jadwal Kegiatan", self)
        jadwalKegiatan.setCheckable(True)
        self.toolbar.addAction(jadwalKegiatan)
        jadwalKegiatan.triggered.connect(self.DashboardJadwalKegiatan)

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

        self.layoutTanggal = QHBoxLayout()
        self.layoutTanggal.setObjectName("layoutTanggal")


        # Mengambil tanggal hari ini
        tangglHariIni = QDate.currentDate()
        # format tanggal
        format = tangglHariIni.toString("dddd dd - MMMM - yyyy")

        self.tanggal = QLabel(format)
        self.tanggal.setObjectName("lbTanggal")
        self.layoutTanggal.addWidget(self.tanggal)


        # Membuat tombol
        self.btnViewTanggal = QPushButton("  Tanggal")
        self.btnViewTanggal.setObjectName("btnViewTanggal")
        self.btnViewTanggal.setFixedSize(90, 30)

        # memberi icon di push button
        gambarMahasiswa_path = os.path.join(basedir, "gambarMahasiswa", "eyes.png")
        self.btnViewTanggal.setIcon(QIcon(gambarMahasiswa_path))
        self.btnViewTanggal.setIconSize(QSize(20,20))
        self.btnViewTanggal.pressed.connect(self.DashboardJadwal)
        self.layoutTanggal.addWidget(self.btnViewTanggal)
        layoutDs.addLayout(self.layoutTanggal)


        # serch
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Here ...")
        self.search.setObjectName("search")
        self.search.textChanged.connect(self.apply_filter)
        layoutDs.addWidget(self.search)

        # table tugas
        self.daftarTugas = QTableWidget()
        self.daftarTugas.setObjectName("daftarTugas")
        self.daftarTugas.setFixedSize(700,350)
        self.daftarTugas.setColumnCount(7)
        self.daftarTugas.setHorizontalHeaderLabels(["No Tugas","Id mk","Deskripsi Tugas", "Tanggal Pemberian","Tanggal Pengumpulan","Waktu","Action"])
        self.daftarTugas.horizontalHeader().setStretchLastSection(False)
        layoutDs.addWidget(self.daftarTugas)
        
        # 
        layoutDs.addStretch()
        container.setLayout(layoutDs)
        self.setCentralWidget(container)
        self.tugas()
        self.pengingat()
    
    def DashboardJadwal(self):
        container = QWidget()
        layoutDs = QVBoxLayout()
        
        self.judul = QLabel("Jadwal Kuliah")
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

        # ini garis pemisah jadwalkagitan
        self.lineJadwal = QFrame()
        self.lineJadwal.setObjectName("line")
        self.lineJadwal.setFrameShape(QFrame.HLine)
        self.lineJadwal.setFrameShadow(QFrame.Sunken)
        layoutDs.addWidget(self.lineJadwal)

        # memembuat table jadwal
        self.daftarJadwal = QTableWidget()
        self.daftarJadwal.setObjectName("daftarJadwal")
        self.daftarJadwal.setFixedSize(700,250)
        self.daftarJadwal.horizontalHeader().setStretchLastSection(True)
        self.daftarJadwal.setColumnCount(6)
        self.daftarJadwal.setHorizontalHeaderLabels(["Hari","Jam/Waktu", "Nama Ruangan", "Mata Kuliah", "Nama Dosen","SKS"])
        layoutDs.addWidget(self.daftarJadwal)


        # ini magtura layout ke container atau membukur layout utama dengan container
        layoutDs.addStretch()
        container.setLayout(layoutDs)
        self.setCentralWidget(container)
        # ini memanggil method jadwal
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
                    Dosen ON Jadwal.Nip_Dosen = Dosen.Nip_Dosen
                INNER JOIN 
                    Ruang ON Jadwal.nama_Ruang = Ruang.nama_Ruang;
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
        
    def DashboardJadwalKegiatan(self):
        container = QWidget()
        layoutDs = QVBoxLayout()
        # ini judul jadwal kegiatan
        self.judul = QLabel("Jadwal Kegiatan")
        self.judul.setObjectName("lbJudul")        
        layoutDs.addWidget(self.judul)
        # ini garis pemisal jadwal kegiatan
        self.lineJadwalKegiatan = QFrame()
        self.lineJadwalKegiatan.setObjectName("line")
        self.lineJadwalKegiatan.setFrameShape(QFrame.HLine)
        self.lineJadwalKegiatan.setFrameShadow(QFrame.Sunken)
        layoutDs.addWidget(self.lineJadwalKegiatan)

        # ini layout untuk Horizontal btn tambah jadwal kegiatan
        layoutHKegiatan = QHBoxLayout()
        spasi = QWidget()
        spasi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layoutHKegiatan.addWidget(spasi)
        self.btnTambahKegiatan = QPushButton("add Kegiatan")
        self.btnTambahKegiatan.setObjectName("btnJadwalKegiatan")
        self.btnTambahKegiatan.setGeometry(200, 150, 100, 40)
        self.btnTambahKegiatan.clicked.connect(self.addKegiatan)
        layoutHKegiatan.addWidget(self.btnTambahKegiatan) 
        layoutDs.addLayout(layoutHKegiatan)

        # membuat jadwal kegiatan
        self.daftarJadwalKegiatan = QTableWidget()
        self.daftarJadwalKegiatan.setObjectName("daftarKegiatan")
        self.daftarJadwalKegiatan.setFixedSize(700,400)
        self.daftarJadwalKegiatan.horizontalHeader().setStretchLastSection(True)
        self.daftarJadwalKegiatan.setColumnCount(6)
        self.daftarJadwalKegiatan.setHorizontalHeaderLabels(["Hari","Nama Kegiatan","Tanggal Kegiatan","Jam Mulai","Jam Selesa","Action"])
        layoutDs.addWidget(self.daftarJadwalKegiatan)

        layoutDs.addStretch()
        # self.setLayout(layoutDs)
        container.setLayout(layoutDs)
        self.setCentralWidget(container)
        self.jadwalKegiatan()

    # ini method menampilkan data table jadwal kegiatan di databses ke QtabeWIged
    def jadwalKegiatan(self):
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        # ini query menampilkan isi jadwalkegiatan
        query = """
            select jadwalkegiatan.id_kegiatan,jadwalkegiatan.Hari,jadwalkegiatan.nama_kegiatan,jadwalkegiatan.tanggal_kegiatan,jadwalkegiatan.jam_mulai,jadwalkegiatan.jam_selesai from jadwalkegiatan
"""
        curse.execute(query)
        ambildata = curse.fetchall()
        self.daftarJadwalKegiatan.setRowCount(len(ambildata))
        for barisnumber,barisData in enumerate(ambildata):
            for col,data in enumerate(barisData):
                self.daftarJadwalKegiatan.setItem(barisnumber,col,QTableWidgetItem(str(data)))

            id_kegiatan = barisData[0]
            # membuat widget yang menampung button hapus dan konfir
            action = QWidget()
            layoutAction = QHBoxLayout(action)
            layoutAction.setContentsMargins(0,0,0,0)
            # mebuatn content button hapus
            self.btnHapus = QPushButton("Hapus")
            self.btnHapus.setObjectName("btnhapus")
            self.btnHapus.setProperty("row",barisnumber)
            self.btnHapus.clicked.connect(partial(self.Hapus, id_kegiatan=id_kegiatan))
            # membuat content konfir
            query_check = """
            SELECT COUNT(*) FROM daftarkegiatanselesai where id_kegiatan = %s;
"""
            curse.execute(query_check,(id_kegiatan,))
            # ini mengek apakah id_kegiatan tersebut sudah dikumpulkan didalam daftarkegiatanselesai
            sudah_selesai = curse.fetchone()[0] > 0 #ini mengecek jika lebih dari 1 maka sudah seesai
            # ini membuat button konfir
            self.btnkonfir = QPushButton()
            self.btnkonfir.setObjectName("buttonkonfir")
            # ini membuat satu variabel yang dimana = sudah_selesai 
            tombolNonAktif = sudah_selesai
            # ini jika syarat slesai terpenuhi mka btnkonfir akan diset selesai
            if sudah_selesai:
                self.btnkonfir.setText("SELESAI")
                self.btnkonfir.setStyleSheet("Background-color:green")
            # jika button slesai belum terpenuhi maka diset konfirmasi
            else:
                self.btnkonfir.setText("Konfirmasi")
                self.btnkonfir.clicked.connect(partial(self.konfir, id_kegiatan=id_kegiatan))
            
            # ini menjadikan tombol dinonaktifkan jika syarat terpenuhi
            self.btnkonfir.setEnabled(not tombolNonAktif)
            self.btnHapus.setEnabled(not tombolNonAktif)
            
            # menepatlan button konrif kedalam setproperty di setia barisnumber
            self.btnkonfir.setProperty("row",barisnumber)
            # menmabhkn content onte tersebut kedalam layout
            layoutAction.addWidget(self.btnHapus)
            layoutAction.addWidget(self.btnkonfir)
            
            # meletakkan content tersebut atau action tersebut kedalam colom cel ke 5 setiap barisnumber (row)
            self.daftarJadwalKegiatan.setCellWidget(barisnumber, 5, action)
        # merapikan colom sesuai panjang data
        self.daftarJadwalKegiatan.resizeColumnsToContents

    # membuat method add kegiatan untuk memaanggil class halamantambahkegiatan
    def addKegiatan(self):
        self.showTambahKegiatan = HalamanTambahKegiatan(self)
        self.showTambahKegiatan.show()
        # self.hide()

    def Hapus(self,id_kegiatan):
        print(f"ID yang diterima: {id_kegiatan}")
        print("Hapus")
        connction,curse = buat_koneksi()
        curse = connction.cursor()
        massage = QMessageBox.question(self,"question","Apakah anda yakin ingin menghapus jadwal kegiatan ini? ", QMessageBox.Yes | QMessageBox.No)
        if massage == QMessageBox.Yes:
            query = """
                DELETE FROM jadwalkegiatan WHERE id_kegiatan = %s;

    """     
            curse.execute(query,(id_kegiatan,))
            connction.commit()
            QMessageBox.information(self,"Konfirmasi","Jadwal kegiatan berhasil dihapus")
            self.jadwalKegiatan()
   
    def konfir(self,id_kegiatan):
        print("konfir")
        connection,curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                    INSERT INTO daftarKegiatanSelesai (id_kegiatan, nama_kegiatan, hari, tanggal_kegiatan)
                    SELECT id_kegiatan, nama_kegiatan, hari, tanggal_kegiatan
                    FROM jadwalKegiatan
                    WHERE id_kegiatan = %s;
    """ 
        curse.execute(query,(id_kegiatan,))
        massage = QMessageBox.question(self,"question","Apakah ini tugas ini telah selesai ? " , QMessageBox.Yes | QMessageBox.No)
        if massage == QMessageBox.Yes:
            connection.commit()
            self.jadwalKegiatan()

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
                self.buttonKmpl.clicked.connect(partial(self.view, id_tugas=id_tugas))

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
        self.ShowHalamanKumpulkanTugas = HalamanKumpulkanTugas(id_tugas,self.username,self)
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
            elif sisaHari > 3:  
                pesan = f"Tugas '{namajudul}' akan jatuh tempo dalam {sisaHari} hari, yaitu pada {formatDeadline.toString('dd MMMM yyyy HH:mm:ss')}."
                QMessageBox.information(self, "Pengingat Deadline", pesan)

# ini halaman kumpulkan tugas
class HalamanKumpulkanTugas(QWidget):
    def __init__(self,id_tugas,username,parent_window):
        super().__init__()
        self.username = username
        self.parent_window = parent_window 
        # self.tugas = id_tugas
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
        # self.FileTugas.setEnabled(False)
        self.lbFile = QLabel("File Tugas")
        self.btnKirim = QPushButton("Kirim")
        self.btnKirim.clicked.connect(self.kirim)
        
        # menambahkan ke layout
        layout.addWidget(self.id_tugas)
        layout.addWidget(self.mataKuliah)
        layout.addWidget(self.judulTugas)
        layout.addWidget(self.tanggalPemberian)
        layout.addWidget(self.tanggalDeadline)
        layout.addWidget(self.tanggal)
        layout.addWidget(self.lbFile)
        layout.addWidget(self.FileTugas)
        layout.addWidget(self.btnKirim)

        # mengsetlayout
        self.setLayout(layout)
        self.ambilDataTugas(id_tugas)

    def ambilDataTugas(self, id_tugas):
        connection, curse = buat_koneksi()
        curse = connection.cursor()
        query = """
                SELECT tugas.id_tugas, tugas.id_mk, tugas.deskripsi_tugas, tugas.tanggal_pemberian, tugas.tanggal_pengumpulan
                FROM tugas
                JOIN matakuliah ON matakuliah.id_mk = tugas.id_mk
                WHERE tugas.id_tugas = %s;
            """
        curse.execute(query, (id_tugas,))
        ambildata = curse.fetchone()

        if ambildata:
            id_tugas, id_mk, deskripsi_tugas, tanggal_pemberian, tanggal_pengumpulan = ambildata
            self.idTugas = id_tugas
            self.idmk = id_mk
            self.deskripsi = deskripsi_tugas
            self.id_tugas.setText(f'ID Tugas\t\t\t: {id_tugas}')
            self.mataKuliah.setText(f'ID Mata Kuliah\t\t: {id_mk}')
            self.judulTugas.setText(f'Judul Tugas\t\t: {deskripsi_tugas}')
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
            Jdltugas = self.deskripsi
            massage = QMessageBox.question(self,"",f"Apakah anda yakin ? ", QMessageBox.Yes | QMessageBox.No)
            if massage == QMessageBox.Yes : 
                connection.commit()
                print("berhasil")
                QMessageBox.information(self,"Berhasil",f"Pengumpulan tugas yang berjudul {Jdltugas} berhasil")
                self.close()
                self.parent_window.tugas()


#halaman setting 
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
        tabs.addTab(self.changePw(self.username), "Change Password")

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
        self.ldNama.setEnabled(False)
        layoutHNama.addWidget(self.lbNama)
        layoutHNama.addWidget(self.ldNama)

        # Layout Nim
        layoutHNim = QHBoxLayout()
        self.lbNim = QLabel("Nim")
        self.lbNim.setStyleSheet("margin-right : 25px")
        self.ldNim = QLineEdit()
        self.ldNim.setEnabled(False)
        layoutHNim.addWidget(self.lbNim)
        layoutHNim.addWidget(self.ldNim)

        # Layout Jurusan
        layoutHJurusan = QHBoxLayout()
        self.lbJurusan = QLabel("Jurusan")
        self.lbJurusan.setStyleSheet("margin-right : 8px")
        self.ldJurusan = QLineEdit()
        self.ldJurusan.setEnabled(False)
        layoutHJurusan.addWidget(self.lbJurusan)
        layoutHJurusan.addWidget(self.ldJurusan)

        # Layout Prodi
        layoutHProdi = QHBoxLayout()
        self.lbProdi = QLabel("Prodi")
        self.lbProdi.setStyleSheet("margin-right : 20px")
        self.ldProdi = QLineEdit()
        self.ldProdi.setEnabled(False)
        layoutHProdi.addWidget(self.lbProdi)
        layoutHProdi.addWidget(self.ldProdi)

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

    def changePw(self,username):
        layout = QVBoxLayout()

        # Layout Username
        layoutHUsernamePw = QHBoxLayout()
        self.lbUsernamePw = QLabel("Username")
        self.lbUsernamePw.setStyleSheet("margin-right : 58px")
        self.ldUsernamePw = QLineEdit()
        self.ldUsernamePw.setEnabled(False)
        layoutHUsernamePw.addWidget(self.lbUsernamePw)
        layoutHUsernamePw.addWidget(self.ldUsernamePw)

        # mengambil username untuk halaman change password
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

# # untuk melihat tugas yang sudah diinputkan
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
        self.FileTugas.setReadOnly(True)
        # self.FileTugas.setEnabled(False)
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

# halaman menambahkan kegiatan
class HalamanTambahKegiatan(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(400,450)
        # self.setStyleSheet("background-color:rgb(235, 241, 243);")

        # layout utama
        layout = QVBoxLayout()

        logo = QLabel()
        fotoLogo = (QPixmap(os.path.join(basedir,"./gambarMahasiswa/rb_2148552956_copy-removebg-preview.png")))
        logo.setPixmap(fotoLogo)
        logo.setAlignment(Qt.AlignCenter)
        # logo.setSi
        layout.addWidget(logo)

        # ini content widget
        # layout hari
        layoutHhari = QHBoxLayout()
        layoutHhari.setObjectName("layoutHharikegiatan")
        # layoutHhari.setContentsMargins(5,50,0,5)
        layoutHhari.setSpacing(10)
        # content layout hari
        self.Hari = QLabel("Hari")
        self.Hari.setObjectName("LabelHari")
        self.ldHari = QLineEdit()
        layoutHhari.addWidget(self.Hari)
        layoutHhari.addWidget(self.ldHari)
        layout.addLayout(layoutHhari)

        # layout nama kegiatab
        layoutHkegitan = QHBoxLayout()
        # content kegiatan
        self.kegiatan = QLabel("Nama Kegiatan")
        self.kegiatan.setObjectName("LabelKegiatan")
        self.ldkegiatan =QLineEdit()
        layoutHkegitan.addWidget(self.kegiatan)
        layoutHkegitan.addWidget(self.ldkegiatan)
        layout.addLayout(layoutHkegitan)

        # layout tanggal
        layoutHTanggal = QHBoxLayout()
        # contente layout tanggal
        self.Tanggal = QLabel("Tanggal")
        self.Tanggal.setObjectName("LabelTanggal")
        self.spin_tahun = QSpinBox()
        self.spin_tahun.setRange(1900, 2100)  # Rentang tahun
        self.spin_tahun.setPrefix("Tahun: ")
        self.spin_tahun.setStyleSheet("padding: 3px 10px;")

        # SpinBox untuk input bulan
        self.spin_bulan = QSpinBox()
        self.spin_bulan.setRange(1, 12)  # Rentang bulan
        self.spin_bulan.setPrefix("Bulan: ")
        self.spin_bulan.setStyleSheet("padding: 3px 10px;")

        # SpinBox untuk input tanggal
        self.spin_tanggal = QSpinBox()
        self.spin_tanggal.setRange(1, 31)  # Rentang tanggal
        self.spin_tanggal.setPrefix("Tanggal: ")
        self.spin_tanggal.setStyleSheet("padding: 3px 10px;")
        layoutHTanggal.addWidget(self.Tanggal)
        layoutHTanggal.addWidget(self.spin_tahun)
        layoutHTanggal.addWidget(self.spin_bulan)
        layoutHTanggal.addWidget(self.spin_tanggal)
        layout.addLayout(layoutHTanggal)

        # layout jam mulai
        layoutjam = QHBoxLayout()
        # contente layout jam
        self.lbjam = QLabel("Jam Mulai")
        self.lbjam.setObjectName("LabelJam")
        layoutjam.addWidget(self.lbjam)
        # jam mulai
        self.spin_JmMulai = QSpinBox()
        self.spin_JmMulai.setRange(0, 23)  # Rentang tanggal
        self.spin_JmMulai.setPrefix("Jam: ")
        self.spin_tanggal.setStyleSheet("padding: 3px 10px;")
        
        # menit mulai
        self.spin_MenitMulai = QSpinBox()
        self.spin_MenitMulai.setRange(0, 59)  # Rentang tanggal
        self.spin_MenitMulai.setPrefix("Menit: ")
        self.spin_MenitMulai.setStyleSheet("padding: 3px 10px;")
        # detik mulai
        self.spin_detikMulai = QSpinBox()
        self.spin_detikMulai.setRange(0, 59)  # Rentang tanggal
        self.spin_detikMulai.setPrefix("Detik: ")
        self.spin_detikMulai.setStyleSheet("padding: 3px 10px;")
        #menmabah content layout jam mulai
        layoutjam.addWidget(self.spin_JmMulai)
        layoutjam.addWidget(self.spin_MenitMulai)
        layoutjam.addWidget(self.spin_detikMulai)
        layout.addLayout(layoutjam)

        # layout jam selesai
        layoutjamSelesai = QHBoxLayout()
        self.lbjamSelesai = QLabel("Jam Selesai")
        self.lbjamSelesai.setObjectName("LabelJamSelesai")
        layoutjamSelesai.addWidget(self.lbjamSelesai)
        # jam selesai
        self.spin_Jmselesai = QSpinBox()
        self.spin_Jmselesai.setRange(0, 23)  # Rentang tanggal
        self.spin_Jmselesai.setPrefix("Jam: ")
        self.spin_Jmselesai.setStyleSheet("padding: 3px 10px;")
        
        # menit selesai
        self.spin_Menitselesai = QSpinBox()
        self.spin_Menitselesai.setRange(0, 59)  # Rentang tanggal
        self.spin_Menitselesai.setPrefix("Menit: ")
        self.spin_Menitselesai.setStyleSheet("padding: 3px 10px;")
        # detik selesai
        self.spin_detikSelesai = QSpinBox()
        self.spin_detikSelesai.setRange(0, 59)  # Rentang tanggal
        self.spin_detikSelesai.setPrefix("Detik: ")
        self.spin_detikSelesai.setStyleSheet("padding: 3px 10px;")
        #menmabah content layout jam 
        layoutjamSelesai.addWidget(self.spin_Jmselesai)
        layoutjamSelesai.addWidget(self.spin_Menitselesai)
        layoutjamSelesai.addWidget(self.spin_detikSelesai)
        layout.addLayout(layoutjamSelesai)

        # btn tambah
        self.btntambah = QPushButton("Tambah")
        self.btntambah.setObjectName("btntambahKegiatan")
        self.btntambah.clicked.connect(self.tambah)
        layout.addWidget(self.btntambah)

        # mengatur layout utama
        layout.addStretch()
        self.setLayout(layout)
    
    def tambah (self):
        hari = self.ldHari.text()
        nama_kegiatan = self.ldkegiatan.text()
        tanggal = f"{self.spin_tahun.value():01d}-{self.spin_bulan.value():02d}-{self.spin_tanggal.value()}"
        jam_mulai = f"{self.spin_JmMulai.value()}:{self.spin_MenitMulai.value()}:{self.spin_detikMulai.value()}"
        jam_selesai = f"{self.spin_Jmselesai.value()}:{self.spin_Menitselesai.value()}:{self.spin_detikSelesai.value()}"

        connection,curse = buat_koneksi()
        curse = connection.cursor()
        if not hari or not nama_kegiatan or not tanggal or not jam_mulai or not jam_selesai:
            QMessageBox.warning(self, "Peringatan", "Silahkan lengkapi file tugas.")
            return
        else:
            query = """
                INSERT INTO jadwalkegiatan (hari, nama_kegiatan, Tanggal_kegiatan, jam_mulai, jam_selesai) 
    VALUES (%s, %s, %s, %s, %s);
    """ 
            curse.execute(query,(hari,nama_kegiatan,tanggal,jam_mulai,jam_selesai))
            massage = QMessageBox.question(self,"",f"Apakah anda yakin ? ", QMessageBox.Yes | QMessageBox.No)
            if massage == QMessageBox.Yes : 
                connection.commit()
                print("berhasil")
                QMessageBox.information(self,"Berhasil",f"Penmabahan Jadwal Kegiatan Berhasil")
                self.close()
                self.parent.jadwalKegiatan()