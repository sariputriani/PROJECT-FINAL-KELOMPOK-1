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
-- Table structure for table `datamatakuliah`
--

CREATE TABLE `datamatakuliah` (
  `ID_MK` varchar(10) DEFAULT NULL,
  `NIP_Dosen` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `datamatakuliah`
--

INSERT INTO `datamatakuliah` (`ID_MK`, `NIP_Dosen`) VALUES
('PPV', '199407162022031006'),
('OM', '199407162022031006'),
('AI', '9900981028'),
('SO', '198904052024061001'),
('MN', '198806042019092001'),
('BI', '198211052008012014');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `datamatakuliah`
--
ALTER TABLE `datamatakuliah`
  ADD KEY `ID_MK` (`ID_MK`),
  ADD KEY `NIP_Dosen` (`NIP_Dosen`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `datamatakuliah`
--
ALTER TABLE `datamatakuliah`
  ADD CONSTRAINT `datamatakuliah_ibfk_1` FOREIGN KEY (`ID_MK`) REFERENCES `matakuliah` (`ID_MK`),
  ADD CONSTRAINT `datamatakuliah_ibfk_2` FOREIGN KEY (`NIP_Dosen`) REFERENCES `dosen` (`NIP_Dosen`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
