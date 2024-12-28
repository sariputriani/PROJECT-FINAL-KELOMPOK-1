import os
import mysql.connector
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QToolBar, 
    QFileDialog, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox, QFormLayout, 
    QStackedWidget, QSizePolicy, QMessageBox, QAction, QLineEdit, QInputDialog
)
from PySide6.QtCore import QSize, Qt 

class HalamanDosen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Manajemen Mahasiswa")
        self.setFixedSize(800, 600)

        # Menyimpan koneksi database MySQL
        self.db_conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan username MySQL Anda
            password="",  # Ganti dengan password MySQL Anda
            database="aplikasi_mahasiswa"  # Nama database Anda
        )
        self.db_cursor = self.db_conn.cursor()

        # Membuat tabel jika belum ada
        self.create_tables()

        # Layout utama
        self.layoutMHS = QVBoxLayout()

        # Stacked layout untuk memudahkan navigasi antar halaman
        self.stacked_widget = QStackedWidget()
        self.layoutMHS.addWidget(self.stacked_widget)

        # Toolbar
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        # Tambahkan tindakan untuk tiap tombol toolbar
        self._add_toolbar_actions()

        # Mengatur halaman pada stacked widget
        self._setup_pages()

        # Set halaman awal (Dashboard)
        self.stacked_widget.setCurrentWidget(self.dashboard_page)

        # Set Layout utama
        container = QWidget()
        container.setLayout(self.layoutMHS)
        self.setCentralWidget(container)

    def create_tables(self):
        # Membuat tabel tugas, materi, dan kehadiran jika belum ada
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS tugas (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    nama VARCHAR(255),
                                    nim VARCHAR(255),
                                    nilai VARCHAR(255))''')
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS materi (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    nama_file VARCHAR(255),
                                    path TEXT)''')
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS kehadiran (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    nim VARCHAR(255),
                                    nama VARCHAR(255),
                                    status VARCHAR(255))''')
        self.db_conn.commit()

    def _add_toolbar_actions(self):
        dashboard_action = QAction("Dasbor", self)
        self.toolbar.addAction(dashboard_action)
        dashboard_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard_page))

        upload_materi_action = QAction("Unggah Materi", self)
        self.toolbar.addAction(upload_materi_action)
        upload_materi_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.upload_materi_page))

        kelola_tugas_action = QAction("Kelola Tugas", self)
        self.toolbar.addAction(kelola_tugas_action)
        kelola_tugas_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.kelola_tugas_page))

        laporan_kehadiran_action = QAction("Laporan Kehadiran", self)
        self.toolbar.addAction(laporan_kehadiran_action)
        laporan_kehadiran_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.laporan_kehadiran_page))

        logout_action = QAction("Logout", self)
        self.toolbar.addAction(logout_action)
        logout_action.triggered.connect(self.logout)

    def _setup_pages(self):
        self.dashboard_page = QWidget()
        self.upload_materi_page = QWidget()
        self.kelola_tugas_page = QWidget()
        self.laporan_kehadiran_page = QWidget()

        self.setup_dashboard()
        self.setup_upload_materi()
        self.setup_kelola_tugas()
        self.setup_laporan_kehadiran()

        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.upload_materi_page)
        self.stacked_widget.addWidget(self.kelola_tugas_page)
        self.stacked_widget.addWidget(self.laporan_kehadiran_page)

    def setup_dashboard(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ringkasan Tugas, Materi Kuliah, dan Kehadiran"))
        self.dashboard_page.setLayout(layout)

    def setup_upload_materi(self):
        layout = QVBoxLayout()
        upload_button = QPushButton("Unggah Materi")
        upload_button.clicked.connect(self.upload_materi)
        layout.addWidget(upload_button)
        self.upload_materi_page.setLayout(layout)

    def setup_kelola_tugas(self):
        layout = QVBoxLayout()
        kelola_button = QPushButton("Tambah Tugas Baru")
        kelola_button.clicked.connect(self.kelola_tugas)
        layout.addWidget(kelola_button)
        self.kelola_tugas_page.setLayout(layout)

    def setup_laporan_kehadiran(self):
        layout = QVBoxLayout()

        # Button untuk membuka form input kehadiran
        input_button = QPushButton("Input Kehadiran")
        input_button.clicked.connect(self.input_kehadiran)
        layout.addWidget(input_button)

        # Button untuk melihat laporan kehadiran
        lihat_button = QPushButton("Lihat Laporan Kehadiran")
        lihat_button.clicked.connect(self.lihat_laporan_kehadiran)
        layout.addWidget(lihat_button)

        self.laporan_kehadiran_page.setLayout(layout)

    def upload_materi(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("PDF Files (*.pdf);;All Files (*)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                # Simpan materi ke database
                file_name = os.path.basename(file_path)
                self.db_cursor.execute('INSERT INTO materi (nama_file, path) VALUES (%s, %s)', 
                                        (file_name, file_path))
                self.db_conn.commit()
                QMessageBox.information(self, "Sukses", f"Materi berhasil diunggah ke {file_path}")

    def kelola_tugas(self):
        dialog = KelolaTugasDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data_tugas = dialog.get_data()
            # Simpan data tugas ke database
            self.db_cursor.execute('INSERT INTO tugas (nama, nim, nilai) VALUES (%s, %s, %s)', 
                                    (data_tugas['nama'], data_tugas['nim'], data_tugas['nilai']))
            self.db_conn.commit()
            self.update_dashboard()

    def input_kehadiran(self):
        dialog = InputKehadiranDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data_kehadiran = dialog.get_data()
            # Simpan data kehadiran ke database
            self.db_cursor.execute('INSERT INTO kehadiran (nim, nama, status) VALUES (%s, %s, %s)', 
                                    (data_kehadiran['nim'], data_kehadiran['nama'], data_kehadiran['status']))
            self.db_conn.commit()

    def lihat_laporan_kehadiran(self):
        self.db_cursor.execute('SELECT nim, nama, status FROM kehadiran')
        kehadiran_data = self.db_cursor.fetchall()
        dialog = LaporanKehadiranDialog(self, kehadiran_data)
        dialog.exec()

    def update_dashboard(self):
        # Update tampilan dashboard dengan data tugas dan lainnya
        pass

    def logout(self):
        # Menambahkan fungsionalitas logout
        self.close()

class KelolaTugasDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kelola Tugas")
        self.setFixedSize(400, 200)

        self.layout = QFormLayout(self)

        self.nama_edit = QLineEdit(self)
        self.nim_edit = QLineEdit(self)

        self.layout.addRow("Nama Tugas:", self.nama_edit)
        self.layout.addRow("NIM Mahasiswa:", self.nim_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_data(self):
        return {'nama': self.nama_edit.text(), 'nim': self.nim_edit.text(), 'nilai': 'B'}

class InputKehadiranDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Kehadiran")
        self.setFixedSize(400, 200)

        self.layout = QFormLayout(self)

        self.nim_edit = QLineEdit(self)
        self.nama_edit = QLineEdit(self)
        self.status_edit = QLineEdit(self)

        self.layout.addRow("NIM Mahasiswa:", self.nim_edit)
        self.layout.addRow("Nama Mahasiswa:", self.nama_edit)
        self.layout.addRow("Status Kehadiran (Hadir/Absen):", self.status_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_data(self):
        return {'nim': self.nim_edit.text(), 'nama': self.nama_edit.text(), 'status': self.status_edit.text()}

class LaporanKehadiranDialog(QDialog):
    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Laporan Kehadiran")
        self.setFixedSize(600, 400)

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["NIM", "Nama", "Status Kehadiran"])

        self.table.setRowCount(len(data))

        for row, kehadiran in enumerate(data):
            for col, value in enumerate(kehadiran):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)

        