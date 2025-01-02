-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 01, 2025 at 09:12 AM
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
  `Deskripsi_Tugas` text NOT NULL,
  `Tanggal_Pemberian` datetime NOT NULL,
  `Tanggal_Pengumpulan` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tugas`
--

INSERT INTO `tugas` (`ID_Tugas`, `ID_MK`, `Deskripsi_Tugas`, `Tanggal_Pemberian`, `Tanggal_Pengumpulan`) VALUES
('TGS01', 'SO', 'Installasi Linux dan MacOs', '2024-12-08 11:00:00', '2024-12-15 23:59:00'),
('TGS02', 'PPV', 'Penginstallan PySide6 di VsCode', '2024-12-04 10:30:00', '2024-12-07 23:59:00'),
('TGS03', 'AI', 'Pengumpulan Tugas Video', '2024-12-05 16:00:00', '2024-12-19 20:00:00'),
('TGS04', 'BI', 'Speech Video', '2024-12-30 19:30:00', '2025-01-17 23:59:00'),
('TGS05', 'OM', 'Tugas Rencana Anggaran Biaya', '2024-12-12 13:00:00', '2024-12-19 23:59:00'),
('TGS06', 'MN', 'Metode Gauss Jordan', '2024-12-13 09:00:00', '2024-12-20 23:59:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tugas`
--
ALTER TABLE `tugas`
  ADD PRIMARY KEY (`ID_Tugas`),
  ADD KEY `id_mk` (`ID_MK`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
