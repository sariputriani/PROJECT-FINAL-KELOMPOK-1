# PROJECT-FINAL-KELOMPOK-1
Syarat-Syarat yang diperlukan untuk menjalankan aplikasi ini adalah : 
1.	Menyediakan aplikasi vscode untuk menjalankan aplikasi.
Jika tidak ada, anda bisa mengunduh di website resmi vscode (https://code.visualstudio.com/download)
2.	Menyediakan xampp untuk database.
Jika tidak ada, anda bisa mengunduh di website resmi xampp (https://www.apachefriends.org/download.html)
3.	Mengunduh bahasa pemograman python (unduh python extension pack) di dalam vscode
4.	Mengunduh library pyside6 di python (pip install pyside6) masukkan kode tersebut kedalam terminal untuk mengunduhnya

Langkah-Langkah untuk Menjalankan Aplikasi :
1.	Buka vscode 
2.	Mengunduh codingan file di github 
   -	Open github
   -	Klik tombol code
   -	Setelah itu pilih opsi Download Zip
3.	Setelah mengunduh file codingan nya di github, open xampp dan ikuti langkah-langkah di bawah ini:
   - create database dengan nama ‘manajemen_tugas_jadwal’ 
   - import file tabel yang berasal dari folder database dari unduhan zip barusan kedalam database manajemen_tugas_jadwal yang kita           buat atau nama database kalian. 
4.	Open folder GitHub yang kita download tersebut ke VsCode (Visual Studio Code)
5.	Run file main.py
6.	Setelah run maka akan muncul halaman login. Dibagian halaman login ini kalian bisa pilih antara mau login sebagai dosen atau mahasiswa. 
-	Jika anda ingin login sebagai mahasiswa, anda bisa melihat username dan password mahasiswa dalam table loginmahasiswa yang terdapat di database manajemen_tugas_jadwal. 
-	Jika anda ingin login sebagai dosen, anda bisa melihat username dan password dosen di tabel logindosen yang terdapat di database manajemen_tugas_jadwal.
7.	Jika kalian login sebagai mahasiswa maka akan muncul tampilan berikut ini :
- Login Sebagai Mahasiswa : ![alt text](https://github.com/sariputriani/PROJECT-FINAL-KELOMPOK-1/blob/main/gambar_readme/WhatsApp%20Image%202025-01-10%20at%2018.27.01_7e6f05dc.jpg?raw=true)

Fitur-Fitur Jika Login Sebagai Mahasiswa
 -	Button Kumpulkan :
   Fitur ini berguna sebagai tombol untuk mengumpulkan tugas
 -	Button Pengingat Deadline :
   Fitur ini berfungsi sebagai tombol untuk mengingatkan mahasiswa akan deadline tugasnya.
 -	Button Analisis Waktu :
   Fitur ini berfungsi sebagai tombol yang berguna untuk menganalisis waktu dalam melihat/memperkirakan tugas yang ada.
 -	Button Melihat Jadwal :
   Fitur ini berguna untuk melihat jadwal perkuliahan yang ada.
 -	Button Melihat Jadwal Kegiatan :
   Berbeda dengan yang sebelumnya, fitur ini berguna untuk melihat jadwal kegiatan/tugas yang ada.
 
8.	Jika kalian login sebagai dosen maka akan muncul tampilan berikut ini :
- Login Sebagai Dosen : ![alt text](https://github.com/sariputriani/PROJECT-FINAL-KELOMPOK-1/blob/main/gambar_readme/WhatsApp%20Image%202025-01-10%20at%2020.24.19_a3a3b8e9.jpg?raw=true)

Fitur-Fitur Jika Login Sebagai Dosen
 -	Action View :
   Fitur ini berfungsi sebagai tombol yang dapat melihat mahasiswa yang mengumpulkan tugas.
 -	Button Hapus :
   Fitur ini berguna sebagai tombol untuk menghapus tugas yang ada.
 -	Button Edit :
   Fitur ini berfungsi sebagai tombol untuk mengedit tugas yang sudah ada, contohnya kita dapat mengedit deskripsinya.
 -	Button Add :
   Fitur ini berfungsi sebagai tombol yang dapat menambahkan tugas baru dari dosen. 

