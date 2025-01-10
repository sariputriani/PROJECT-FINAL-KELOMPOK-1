-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 10, 2025 at 11:43 AM
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
-- Table structure for table `jadwalkegiatan`
--

CREATE TABLE `jadwalkegiatan` (
  `id_kegiatan` int(255) NOT NULL,
  `nim` varchar(20) DEFAULT NULL,
  `Nama_kegiatan` varchar(255) NOT NULL,
  `Hari` varchar(15) NOT NULL,
  `TanggalMulai_Kegiatan` datetime NOT NULL,
  `tanggal_AkhirKegiatan` datetime NOT NULL,
  `status` enum('selesai','tidak selesai') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `jadwalkegiatan`
--

INSERT INTO `jadwalkegiatan` (`id_kegiatan`, `nim`, `Nama_kegiatan`, `Hari`, `TanggalMulai_Kegiatan`, `tanggal_AkhirKegiatan`, `status`) VALUES
(1, '3202316107', 'Kerja Kelompok Metode Numerik', 'Rabu', '2024-12-18 12:30:00', '2025-01-12 23:59:00', ''),
(2, '3202216101', 'Mengerjakan Jobsheet 14', 'Senin', '2024-12-23 10:30:00', '2024-12-30 23:59:00', 'selesai'),
(3, '3202316005', 'Mengerjakan Essay Bahasa Inggris', 'Selasa', '2025-01-07 13:45:00', '2025-01-09 23:59:00', 'tidak selesai'),
(4, '3202316054', 'Membuat laporan penginstallan MacOs', 'Minggu', '2024-12-23 14:00:00', '2024-12-30 20:30:00', 'selesai'),
(5, '3202316087', 'Membuat video pidato bahasa inggris', 'Sabtu', '2024-12-22 15:30:00', '2025-01-17 17:00:00', ''),
(6, '3202316102', 'Melakukan wawancara ke perusahaan', 'Kamis', '2024-12-12 09:00:00', '2024-12-19 16:00:00', 'tidak selesai');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `jadwalkegiatan`
--
ALTER TABLE `jadwalkegiatan`
  ADD PRIMARY KEY (`id_kegiatan`),
  ADD KEY `fk_nim` (`nim`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `jadwalkegiatan`
--
ALTER TABLE `jadwalkegiatan`
  MODIFY `id_kegiatan` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `jadwalkegiatan`
--
ALTER TABLE `jadwalkegiatan`
  ADD CONSTRAINT `fk_nim` FOREIGN KEY (`nim`) REFERENCES `datamahasiswa` (`nim`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
