-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Jan 2025 pada 07.47
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
-- Struktur dari tabel `datamatakuliah`
--

CREATE TABLE `datamatakuliah` (
  `ID_MK` varchar(10) DEFAULT NULL,
  `NIP_Dosen` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `datamatakuliah`
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
-- Indeks untuk tabel `datamatakuliah`
--
ALTER TABLE `datamatakuliah`
  ADD KEY `ID_MK` (`ID_MK`),
  ADD KEY `NIP_Dosen` (`NIP_Dosen`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `datamatakuliah`
--
ALTER TABLE `datamatakuliah`
  ADD CONSTRAINT `datamatakuliah_ibfk_1` FOREIGN KEY (`ID_MK`) REFERENCES `matakuliah` (`ID_MK`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `datamatakuliah_ibfk_2` FOREIGN KEY (`NIP_Dosen`) REFERENCES `dosen` (`NIP_Dosen`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
