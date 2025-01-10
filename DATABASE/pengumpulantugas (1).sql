-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 10, 2025 at 11:44 AM
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
-- Table structure for table `pengumpulantugas`
--

CREATE TABLE `pengumpulantugas` (
  `id_pengumpulan` int(11) NOT NULL,
  `id_tugas` varchar(10) DEFAULT NULL,
  `id_mk` varchar(10) DEFAULT NULL,
  `nim` varchar(20) DEFAULT NULL,
  `tanggal_pengumpulan` datetime DEFAULT NULL,
  `file_tugas` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pengumpulantugas`
--
ALTER TABLE `pengumpulantugas`
  ADD PRIMARY KEY (`id_pengumpulan`),
  ADD KEY `id_tugas` (`id_tugas`),
  ADD KEY `nim` (`nim`),
  ADD KEY `id_mk` (`id_mk`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pengumpulantugas`
--
ALTER TABLE `pengumpulantugas`
  MODIFY `id_pengumpulan` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pengumpulantugas`
--
ALTER TABLE `pengumpulantugas`
  ADD CONSTRAINT `pengumpulantugas_ibfk_2` FOREIGN KEY (`nim`) REFERENCES `datamahasiswa` (`nim`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `pengumpulantugas_ibfk_3` FOREIGN KEY (`id_mk`) REFERENCES `matakuliah` (`ID_MK`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
