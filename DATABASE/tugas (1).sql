-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Jan 2025 pada 07.49
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
-- Struktur dari tabel `tugas`
--

CREATE TABLE `tugas` (
  `ID_Tugas` varchar(10) NOT NULL,
  `ID_MK` varchar(10) NOT NULL,
  `id_user` int(11) NOT NULL,
  `judul_tugas` varchar(255) NOT NULL,
  `Deskripsi_Tugas` text NOT NULL,
  `Tanggal_Pemberian` datetime NOT NULL,
  `Tanggal_Pengumpulan` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tugas`
--

INSERT INTO `tugas` (`ID_Tugas`, `ID_MK`, `id_user`, `judul_tugas`, `Deskripsi_Tugas`, `Tanggal_Pemberian`, `Tanggal_Pengumpulan`) VALUES
('TGS01', 'SO', 0, '', 'Installasi Linux dan MacOs', '2024-12-08 11:00:00', '2024-12-15 23:59:00'),
('TGS02', 'PPV', 0, '', 'Penginstallan PySide6 di VsCode', '2024-12-04 10:30:00', '2024-12-07 23:59:00'),
('TGS03', 'AI', 0, '', 'Pengumpulan Tugas Video', '2024-12-05 16:00:00', '2024-12-19 20:00:00'),
('TGS05', 'OM', 0, '', 'Tugas Rencana Anggaran Biaya', '2024-12-12 13:00:00', '2024-12-19 23:59:00'),
('TGS06', 'MN', 0, '', 'Metode Gauss Jordan', '2024-12-13 09:00:00', '2024-12-20 23:59:00'),
('tugas 1', 'BI', 0, 'UAS Video ', 'BLABLABLKABKLA', '2025-01-06 10:00:00', '2025-01-17 16:00:00'),
('tugas 2', 'BI', 0, 'hahha', 'kirim lewat email', '2025-01-07 23:00:00', '2025-01-08 23:00:00'),
('tugas 3', 'BI', 0, '', 'kirim', '2025-01-07 23:00:00', '2025-01-10 23:00:00');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD PRIMARY KEY (`ID_Tugas`),
  ADD KEY `id_mk` (`ID_MK`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD CONSTRAINT `tugas_ibfk_1` FOREIGN KEY (`ID_MK`) REFERENCES `matakuliah` (`ID_MK`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
