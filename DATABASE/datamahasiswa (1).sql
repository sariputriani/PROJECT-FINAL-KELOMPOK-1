-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 10, 2025 at 11:42 AM
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
-- Table structure for table `datamahasiswa`
--

CREATE TABLE `datamahasiswa` (
  `nim` varchar(20) NOT NULL,
  `nama` varchar(50) DEFAULT NULL,
  `jurusan` varchar(255) DEFAULT NULL,
  `prodi` varchar(255) DEFAULT NULL,
  `semester` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `datamahasiswa`
--

INSERT INTO `datamahasiswa` (`nim`, `nama`, `jurusan`, `prodi`, `semester`) VALUES
('3202216101', 'Deronimus Chrismas', 'Teknik Elektro', 'D3 Teknik Informatika', 3),
('3202316005', 'Sari putriani', 'Teknik Elektro', 'D3 Teknik Informatika', 3),
('3202316054', 'Divan Tri Anugrah Januari', 'Teknik Elektro', 'D3 Teknik Informatika', 3),
('3202316087', 'Bagas Anggara Katim', 'Teknik Elektro', 'D3 Teknik Informatika', 3),
('3202316102', 'Ismail', 'Teknik Elektro', 'D3 Teknik Informatika', 3),
('3202316107', 'Alvonda Zulikram', 'Teknik Elektro', 'D3 Teknik Informatika', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `datamahasiswa`
--
ALTER TABLE `datamahasiswa`
  ADD PRIMARY KEY (`nim`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
