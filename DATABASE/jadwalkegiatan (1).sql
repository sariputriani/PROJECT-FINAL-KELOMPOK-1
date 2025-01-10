-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Jan 2025 pada 07.48
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kelompok1`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `jadwalkegiatan`
--

CREATE TABLE `jadwalkegiatan` (
  `id_kegiatan` int(255) NOT NULL,
  `nim` varchar(20) DEFAULT NULL,
  `Nama_kegiatan` varchar(255) NOT NULL,
  `Hari` varchar(15) NOT NULL,
  `TanggalMulai_Kegiatan` datetime NOT NULL,
  `tanggal_AkhirKegiatan` datetime NOT NULL,
  `status` enum('selesai','tidak selesai') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `jadwalkegiatan`
--

INSERT INTO `jadwalkegiatan` (`id_kegiatan`, `nim`, `Nama_kegiatan`, `Hari`, `TanggalMulai_Kegiatan`, `tanggal_AkhirKegiatan`, `status`) VALUES
(24, '3202316005', 'test', 'Selesai', '2025-01-07 00:00:00', '2025-01-01 00:00:01', 'tidak selesai'),
(25, '3202316005', 'joging', 'Kamis', '2025-01-07 23:00:00', '2025-01-06 23:00:00', 'tidak selesai'),
(27, '3202316005', 'Kerja Kelompok', 'Senin', '2025-01-10 23:00:00', '2025-01-09 23:00:00', 'selesai'),
(29, '3202316005', 'cuci baju', 'Senin', '2025-01-10 23:00:00', '2025-01-09 23:00:00', 'selesai'),
(30, '3202316005', 'Bobok', 'Senin', '2025-01-17 23:00:00', '2025-01-10 23:00:00', 'selesai');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `jadwalkegiatan`
--
ALTER TABLE `jadwalkegiatan`
  ADD PRIMARY KEY (`id_kegiatan`),
  ADD KEY `fk_nim` (`nim`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `jadwalkegiatan`
--
ALTER TABLE `jadwalkegiatan`
  MODIFY `id_kegiatan` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `jadwalkegiatan`
--
ALTER TABLE `jadwalkegiatan`
  ADD CONSTRAINT `fk_nim` FOREIGN KEY (`nim`) REFERENCES `datamahasiswa` (`nim`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
