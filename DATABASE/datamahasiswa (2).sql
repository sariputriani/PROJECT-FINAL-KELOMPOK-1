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
-- Struktur dari tabel `datamahasiswa`
--

CREATE TABLE `datamahasiswa` (
  `nim` varchar(20) NOT NULL,
  `nama` varchar(50) DEFAULT NULL,
  `jurusan` varchar(255) DEFAULT NULL,
  `prodi` varchar(255) DEFAULT NULL,
  `semester` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `datamahasiswa`
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
-- Indeks untuk tabel `datamahasiswa`
--
ALTER TABLE `datamahasiswa`
  ADD PRIMARY KEY (`nim`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `datamahasiswa`
--
ALTER TABLE `datamahasiswa`
  ADD CONSTRAINT `datamahasiswa_ibfk_1` FOREIGN KEY (`nim`) REFERENCES `loginmahasiswa` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
