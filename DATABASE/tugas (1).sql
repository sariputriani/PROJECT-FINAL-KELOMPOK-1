-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 10, 2025 at 11:45 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tugas_jadwal`
--

-- --------------------------------------------------------

--
-- Table structure for table `tugas`
--

CREATE TABLE `tugas` (
  `ID_Tugas` varchar(10) NOT NULL,
  `ID_MK` varchar(10) NOT NULL,
  `judul_tugas` varchar(255) NOT NULL,
  `Deskripsi_Tugas` text NOT NULL,
  `Tanggal_Pemberian` datetime NOT NULL,
  `Tanggal_Pengumpulan` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tugas`
--

INSERT INTO `tugas` (`ID_Tugas`, `ID_MK`, `judul_tugas`, `Deskripsi_Tugas`, `Tanggal_Pemberian`, `Tanggal_Pengumpulan`) VALUES
('TGS01', 'SO', 'Installasi MacOs dan Linux', 'Lakukan penginstallan Linus dan MacOs menggunakan Ubuntu atau Virtual Box', '2024-12-08 11:00:00', '2024-12-15 23:59:00'),
('TGS02', 'PPV', 'Jobsheet 1', 'Installah QT PySide6 di VsCode sesuai dengan panduan Jobsheet', '2024-12-04 10:30:00', '2024-12-07 23:59:00'),
('TGS03', 'AI', 'Video Permintaan Maaf', 'Buatlah video permintaan maaf ke orang tua', '2024-12-05 16:00:00', '2024-12-19 20:00:00'),
('TGS05', 'OM', 'Tugas Rencana Anggaran Biaya', 'Buatkan RAB yang dimana biayanya tidak melebihi anggaran yang tersedia dan sudah dibagi dengan rata', '2024-12-12 13:00:00', '2024-12-19 23:59:00'),
('TGS06', 'MN', 'Jobsheet Metode Gauss Seidel', 'Selesaikan studi kasus yang ada di Jobsheet dengan menggunakan metode Gauss Seidel', '2024-12-13 09:00:00', '2024-12-20 23:59:00'),
('TGS07', 'BI', 'Speech Video', 'Buatlah video pidato menggunakan Bahasa Inggris sesuai dengan panduan yang diberikan', '2024-12-21 20:00:00', '2025-01-17 23:59:00'),
('TGS08', 'PPV', 'Jobsheet 3 Layout', 'Buatlah Layout menggunakan QtDesigner dengan cara yang sesuai dengan panduan Jobsheet', '2024-12-20 12:00:00', '2025-01-02 23:00:00'),
('TGS09', 'MN', 'Jobsheet Metode Jacobi', 'Buatkan program dan excel menggunakan metode Jacobi', '2024-12-07 09:00:00', '2024-12-14 22:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tugas`
--
ALTER TABLE `tugas`
  ADD PRIMARY KEY (`ID_Tugas`),
  ADD KEY `id_mk` (`ID_MK`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tugas`
--
ALTER TABLE `tugas`
  ADD CONSTRAINT `tugas_ibfk_1` FOREIGN KEY (`ID_MK`) REFERENCES `matakuliah` (`ID_MK`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
