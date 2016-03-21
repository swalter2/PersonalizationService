-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 21. Mrz 2016 um 15:31
-- Server Version: 5.6.21
-- PHP-Version: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `wikipedia_new`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nutzer`
--

DROP TABLE IF EXISTS `nutzer`;
CREATE TABLE IF NOT EXISTS `nutzer` (
  `id` int(11) NOT NULL,
  `age` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `nutzer`
--

INSERT INTO `nutzer` (`id`, `age`) VALUES
(1, 13),
(2, 44),
(3, 39),
(4, 72),
(5, 78),
(6, 3),
(7, 20);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nutzer_interessen`
--

DROP TABLE IF EXISTS `nutzer_interessen`;
CREATE TABLE IF NOT EXISTS `nutzer_interessen` (
  `id` int(11) NOT NULL,
  `interesse` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `nutzer_interessen`
--

INSERT INTO `nutzer_interessen` (`id`, `interesse`) VALUES
(1, 'BMX'),
(1, 'Fussball'),
(1, 'Fußball'),
(2, 'Fitness'),
(3, 'Pilates'),
(3, 'Rennrad'),
(3, 'Gesund Ernährung'),
(4, 'Gartenarbeit'),
(4, 'Sauna'),
(4, 'Kaffeekranz'),
(4, 'Walking'),
(4, 'Aquajogging'),
(4, 'klassische Musik'),
(5, 'musik 68er und 70er'),
(6, 'mit großem Bruder spielen'),
(7, 'Social media'),
(7, 'Flohmarkt'),
(7, 'Schwimmen');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `nutzer`
--
ALTER TABLE `nutzer`
 ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `nutzer_interessen`
--
ALTER TABLE `nutzer_interessen`
 ADD KEY `id` (`id`), ADD KEY `id_2` (`id`);

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `nutzer_interessen`
--
ALTER TABLE `nutzer_interessen`
ADD CONSTRAINT `nutzer_interessen_ibfk_1` FOREIGN KEY (`id`) REFERENCES `nutzer` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
