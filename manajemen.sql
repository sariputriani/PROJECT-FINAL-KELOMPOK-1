-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 19 Des 2024 pada 14.10
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
-- Database: `manajemen`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `userdosen`
--

CREATE TABLE `userdosen` (
  `username` varchar(10) NOT NULL,
  `password` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `userdosen`
--

INSERT INTO `userdosen` (`username`, `password`) VALUES
('Divan', 123),
('Sari', 999);

-- --------------------------------------------------------

--
-- Struktur dari tabel `usermahasiswa`
--

CREATE TABLE `usermahasiswa` (
  `username` varchar(10) NOT NULL,
  `password` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `usermahasiswa`
--

INSERT INTO `usermahasiswa` (`username`, `password`) VALUES
('Bagas', 1010),
('Dillo', 456),
('Ismail', 789),
('Vonda', 123);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `userdosen`
--
ALTER TABLE `userdosen`
  ADD PRIMARY KEY (`username`);

--
-- Indeks untuk tabel `usermahasiswa`
--
ALTER TABLE `usermahasiswa`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
