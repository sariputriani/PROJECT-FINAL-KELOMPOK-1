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
-- Struktur dari tabel `jadwal`
--

CREATE TABLE `jadwal` (
  `Hari` varchar(20) DEFAULT NULL,
  `Jam` varchar(20) DEFAULT NULL,
  `ID_MK` varchar(10) DEFAULT NULL,
  `NIP_Dosen` varchar(35) DEFAULT NULL,
  `Nama_Ruang` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `jadwal`
--

INSERT INTO `jadwal` (`Hari`, `Jam`, `ID_MK`, `NIP_Dosen`, `Nama_Ruang`) VALUES
('Senin', '07.00 - 15.30', 'PPV', '199407162022031006', 'TI 04'),
('Selasa', '07.00 - 11.25', 'BI', '198211052008012014', 'TI 08'),
(' ', '13.00 - 14.40', 'AI', '9900981028', 'TI 08'),
('Rabu', '07.00 - 14.40', 'MN', '198806042019092001', 'TI 08'),
('Kamis', '07.00 - 15.30', 'SO', '198904052024061001', 'TI 03'),
('Jumat', '07.00 - 08.40', 'OM', '199407162022031006', 'TI 08'),
(' ', '09.45 - 14.40', 'PPV', '199407162022031006', 'TI 05');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `jadwal`
--
ALTER TABLE `jadwal`
  ADD KEY `ID_MK` (`ID_MK`),
  ADD KEY `ID_Dosen` (`NIP_Dosen`),
  ADD KEY `Nama_Ruang` (`Nama_Ruang`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`ID_MK`) REFERENCES `matakuliah` (`ID_MK`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `jadwal_ibfk_2` FOREIGN KEY (`Nama_Ruang`) REFERENCES `ruang` (`Nama_Ruang`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `jadwal_ibfk_3` FOREIGN KEY (`NIP_Dosen`) REFERENCES `dosen` (`NIP_Dosen`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
