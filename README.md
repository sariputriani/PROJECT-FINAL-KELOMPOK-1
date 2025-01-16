# PROJECT-FINAL-KELOMPOK-1
Syarat-Syarat yang diperlukan untuk menjalankan aplikasi ini adalah : 
1.	Menyediakan aplikasi vscode untuk menjalankan aplikasi.
Jika tidak ada, anda bisa mengunduh di website resmi vscode (https://code.visualstudio.com/download)
2.	Menyediakan xampp untuk database.
Jika tidak ada, anda bisa mengunduh di website resmi xampp (https://www.apachefriends.org/download.html)
3.	Mengunduh bahasa pemograman python (unduh python extension pack) di dalam vscode
4.	Mengunduh library pyside6 di python (pip install pyside6) masukkan kode tersebut kedalam terminal untuk mengunduhnya

=============================================
Langkah-Langkah untuk Menjalankan Aplikasi :
=========================================
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
6.	Setelah run maka akan muncul halaman login. Dibagian halaman login ini kalian bisa pilih antara ingin login sebagai dosen atau mahasiswa. 
-	Jika anda ingin login sebagai mahasiswa, anda bisa melihat username dan password mahasiswa dalam table loginmahasiswa yang terdapat di database manajemen_tugas_jadwal. 
-	Jika anda ingin login sebagai dosen, anda bisa melihat username dan password dosen di tabel logindosen yang terdapat di database manajemen_tugas_jadwal.
7.	Jika kalian login sebagai mahasiswa maka akan muncul tampilan berikut ini :
- Login Sebagai Mahasiswa : ![alt text](https://github.com/sariputriani/PROJECT-FINAL-KELOMPOK-1/blob/main/gambar_readme/WhatsApp%20Image%202025-01-10%20at%2018.27.01_7e6f05dc.jpg?raw=true)
- Dashboard Mahasiswa :![alt_text](https://github.com/user-attachments/assets/6faea38b-1cb7-4962-ab2b-c1d978cc4836)
- Daftar Tugas Mahasiswa :![alt_text](https://github.com/user-attachments/assets/7562b5c7-282c-45ff-ad7e-becd6c34d48c)
- Daftar Tugas Mahasiswa Setelah Ada Tugas Yang Dikumpulkan:![ppv4](https://github.com/user-attachments/assets/0dd1f68e-9ac6-4d9a-a762-4076de2271e0)
- Jadwal Perkuliahan :![alt_text](https://github.com/user-attachments/assets/b7c4ef05-f38e-4bdc-90f4-d5ce8c513c41)
- Jadwal Kegiatan :![alt_text](https://github.com/user-attachments/assets/d2d419fe-24ed-4dac-969a-c9795e9d94bf)
- Tampilan Pengaturan Profile :![alt_text](https://github.com/user-attachments/assets/31037769-60a9-45eb-87ba-5187d9a3ebad)
- Tampilan Pengaturan Ubah Password :![alt_text](https://github.com/user-attachments/assets/642e0f1d-aafc-4a5c-a9e0-cfe558fcc14a)

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
- Dashboard Dosen :![alt_text](https://github.com/user-attachments/assets/a8223438-7e83-4f04-8e40-e772930b12d1)
- Dashboard Tugas :![alt_text](https://github.com/user-attachments/assets/7ee37273-0c55-49a2-9550-2516c693828b)
- Penambahan Tugas :![alt_text](https://github.com/user-attachments/assets/c0f415ba-10a0-4d3c-8403-b3fbd2f9bacb)
- View Tugas Mahasiswa :![alt_text](https://github.com/user-attachments/assets/e459300a-ea46-4c12-92ef-1c5db551e4ba)
- ![alt_text](https://github.com/user-attachments/assets/19c07278-af7c-4262-8212-795fe8f092bd)
- Tugas Mahasiswa:![alt_text](https://github.com/user-attachments/assets/0f64a07d-91b3-4dc6-88ea-22e43c72daf9)
- Edit Tugas Mahasiswa:![alt_text](https://github.com/user-attachments/assets/7440811d-9581-4661-9460-442072506d09)
- ![alt_text](https://github.com/user-attachments/assets/a6151243-b15e-46d9-a5b1-2931bb675527)
- Menghapus Tugas:![alt_text](https://github.com/user-attachments/assets/25d6ae8f-1a8a-4aea-8e72-2db2ae563948)
- ![alt_text](https://github.com/user-attachments/assets/c9aff803-42e3-42e0-84cf-2dd136aeb711)
- Profil Dosen:![alt_text](https://github.com/user-attachments/assets/64f6f41e-e6ee-499c-8898-9cfc37dc8a3b)
- Ubah Password Dosen:![alt_text](https://github.com/user-attachments/assets/bac54b3e-9e94-42bd-a875-1043fe0169e8)

Fitur-Fitur Jika Login Sebagai Dosen
 -	Action View :
   Fitur ini berfungsi sebagai tombol yang dapat melihat mahasiswa yang mengumpulkan tugas.
 -	Button Hapus :
   Fitur ini berguna sebagai tombol untuk menghapus tugas yang ada.
 -	Button Edit :
   Fitur ini berfungsi sebagai tombol untuk mengedit tugas yang sudah ada, contohnya kita dapat mengedit deskripsinya.
 -	Button Add :
   Fitur ini berfungsi sebagai tombol yang dapat menambahkan tugas baru dari dosen. 

