-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 29, 2022 at 03:36 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Methods-Project-DB`
--

-- --------------------------------------------------------

--
-- Table structure for table `Cart`
--

CREATE TABLE `Cart` (
  `CartID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `Puchased` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `CartItem`
--

CREATE TABLE `CartItem` (
  `CartItemID` int(11) NOT NULL,
  `ISBN` varchar(25) DEFAULT NULL,
  `CartID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Inventory`
--

CREATE TABLE `Inventory` (
  `ISBN` varchar(25) NOT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `Price` int(11) DEFAULT NULL,
  `Author` varchar(50) DEFAULT NULL,
  `Title` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `UserID` int(11) NOT NULL,
  `PhoneNumber` varchar(75) DEFAULT NULL,
  `ShippingAddress` varchar(75) DEFAULT NULL,
  `Password` varchar(75) DEFAULT NULL,
  `FirstName` varchar(20) DEFAULT NULL,
  `LastName` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`UserID`, `PhoneNumber`, `ShippingAddress`, `Password`, `FirstName`, `LastName`) VALUES
(1, '222-222-2222', '123 Meadow Rd', 'PASS', 'Nathan', 'Lechner'),
(2, '333-333-3333', '456 Hill Dr', 'WORD', 'Guy', 'Dude');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Cart`
--
ALTER TABLE `Cart`
  ADD PRIMARY KEY (`CartID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `CartItem`
--
ALTER TABLE `CartItem`
  ADD PRIMARY KEY (`CartItemID`),
  ADD KEY `CartID` (`CartID`),
  ADD KEY `ISBN` (`ISBN`);

--
-- Indexes for table `Inventory`
--
ALTER TABLE `Inventory`
  ADD PRIMARY KEY (`ISBN`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`UserID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Cart`
--
ALTER TABLE `Cart`
  ADD CONSTRAINT `Cart_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `Users` (`UserID`);

--
-- Constraints for table `CartItem`
--
ALTER TABLE `CartItem`
  ADD CONSTRAINT `CartItem_ibfk_1` FOREIGN KEY (`CartID`) REFERENCES `Cart` (`CartID`),
  ADD CONSTRAINT `CartItem_ibfk_2` FOREIGN KEY (`ISBN`) REFERENCES `Inventory` (`ISBN`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
