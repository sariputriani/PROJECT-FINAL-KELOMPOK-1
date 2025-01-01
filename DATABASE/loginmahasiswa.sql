-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 01, 2025 at 09:11 AM
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
-- Table structure for table `loginmahasiswa`
--

CREATE TABLE `loginmahasiswa` (
  `username` varchar(15) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `loginmahasiswa`
--

INSERT INTO `loginmahasiswa` (`username`, `password`) VALUES
('3202216101', 'dillo098'),
('3202316005', 'ademsari44'),
('3202316054', 'divantau99'),
('3202316087', 'Anggarajin11'),
('3202316102', 'maelketua83'),
('3202316107', 'jokowi32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `loginmahasiswa`
--
ALTER TABLE `loginmahasiswa`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
