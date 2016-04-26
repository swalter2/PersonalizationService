-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 26. Apr 2016 um 16:14
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
-- Tabellenstruktur für Tabelle `annotationen`
--

DROP TABLE IF EXISTS `annotationen`;
CREATE TABLE IF NOT EXISTS `annotationen` (
  `nutzerid` int(11) NOT NULL,
  `artikelid` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `bewertung` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `annotierte_artikel`
--

DROP TABLE IF EXISTS `annotierte_artikel`;
CREATE TABLE IF NOT EXISTS `annotierte_artikel` (
  `id` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `titel` varchar(250) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `text` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `datum` char(10) NOT NULL,
  `ressort` varchar(255) NOT NULL,
  `autor` varchar(255) NOT NULL,
  `seite` int(11) NOT NULL,
  `anzahl_woerter` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `artikel`
--

DROP TABLE IF EXISTS `artikel`;
CREATE TABLE IF NOT EXISTS `artikel` (
  `id` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `titel` varchar(250) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `text` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `tags` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `datum` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `interessen`
--

DROP TABLE IF EXISTS `interessen`;
CREATE TABLE IF NOT EXISTS `interessen` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `interessen_vector_alle`
--

DROP TABLE IF EXISTS `interessen_vector_alle`;
CREATE TABLE IF NOT EXISTS `interessen_vector_alle` (
  `id` int(11) NOT NULL,
  `wikipediaid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `interessen_vector_ohne_personen`
--

DROP TABLE IF EXISTS `interessen_vector_ohne_personen`;
CREATE TABLE IF NOT EXISTS `interessen_vector_ohne_personen` (
  `id` int(11) NOT NULL,
  `wikipediaid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `interessen_vector_personen`
--

DROP TABLE IF EXISTS `interessen_vector_personen`;
CREATE TABLE IF NOT EXISTS `interessen_vector_personen` (
  `id` int(11) NOT NULL,
  `wikipediaid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nutzer`
--

DROP TABLE IF EXISTS `nutzer`;
CREATE TABLE IF NOT EXISTS `nutzer` (
  `id` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `geschlecht` char(1) NOT NULL,
  `abschluss` varchar(255) NOT NULL,
  `interessen_kultur` int(11) NOT NULL,
  `interessen_lokales` int(11) NOT NULL,
  `interessen_lokalsport` int(11) NOT NULL,
  `interessen_politik` int(11) NOT NULL,
  `interessen_sport` int(11) NOT NULL,
  `interessanteste_rubrik` varchar(255) NOT NULL,
  `plz` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nutzer_interessen`
--

DROP TABLE IF EXISTS `nutzer_interessen`;
CREATE TABLE IF NOT EXISTS `nutzer_interessen` (
  `nutzerid` int(11) NOT NULL,
  `interessensid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `personalisierung_alle`
--

DROP TABLE IF EXISTS `personalisierung_alle`;
CREATE TABLE IF NOT EXISTS `personalisierung_alle` (
  `articleid` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `userid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `personalisierung_ohne_personen`
--

DROP TABLE IF EXISTS `personalisierung_ohne_personen`;
CREATE TABLE IF NOT EXISTS `personalisierung_ohne_personen` (
  `articleid` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `userid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `personalisierung_personen`
--

DROP TABLE IF EXISTS `personalisierung_personen`;
CREATE TABLE IF NOT EXISTS `personalisierung_personen` (
  `articleid` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `userid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `vector_alle`
--

DROP TABLE IF EXISTS `vector_alle`;
CREATE TABLE IF NOT EXISTS `vector_alle` (
  `id` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `wikipediaid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `vector_ohne_personen`
--

DROP TABLE IF EXISTS `vector_ohne_personen`;
CREATE TABLE IF NOT EXISTS `vector_ohne_personen` (
  `id` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `wikipediaid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `vector_personen`
--

DROP TABLE IF EXISTS `vector_personen`;
CREATE TABLE IF NOT EXISTS `vector_personen` (
  `id` char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `wikipediaid` int(11) NOT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wikipedia`
--

DROP TABLE IF EXISTS `wikipedia`;
CREATE TABLE IF NOT EXISTS `wikipedia` (
  `id` int(10) unsigned NOT NULL,
  `person` int(10) unsigned NOT NULL,
  `title` varchar(200) NOT NULL,
  `body` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `annotationen`
--
ALTER TABLE `annotationen`
 ADD KEY `nutzerid` (`nutzerid`), ADD KEY `artikelid` (`artikelid`);

--
-- Indizes für die Tabelle `annotierte_artikel`
--
ALTER TABLE `annotierte_artikel`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `id` (`id`), ADD FULLTEXT KEY `titel` (`titel`,`text`), ADD FULLTEXT KEY `text` (`text`);

--
-- Indizes für die Tabelle `artikel`
--
ALTER TABLE `artikel`
 ADD PRIMARY KEY (`id`), ADD KEY `datum` (`datum`), ADD FULLTEXT KEY `titel` (`titel`,`text`), ADD FULLTEXT KEY `text` (`text`);

--
-- Indizes für die Tabelle `interessen`
--
ALTER TABLE `interessen`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `id` (`id`);

--
-- Indizes für die Tabelle `interessen_vector_alle`
--
ALTER TABLE `interessen_vector_alle`
 ADD KEY `id` (`id`);

--
-- Indizes für die Tabelle `interessen_vector_ohne_personen`
--
ALTER TABLE `interessen_vector_ohne_personen`
 ADD KEY `id` (`id`);

--
-- Indizes für die Tabelle `interessen_vector_personen`
--
ALTER TABLE `interessen_vector_personen`
 ADD KEY `id` (`id`);

--
-- Indizes für die Tabelle `nutzer`
--
ALTER TABLE `nutzer`
 ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `nutzer_interessen`
--
ALTER TABLE `nutzer_interessen`
 ADD KEY `nutzerid` (`nutzerid`), ADD KEY `interessensid` (`interessensid`);

--
-- Indizes für die Tabelle `personalisierung_alle`
--
ALTER TABLE `personalisierung_alle`
 ADD KEY `articleid` (`articleid`), ADD KEY `userid` (`userid`);

--
-- Indizes für die Tabelle `personalisierung_ohne_personen`
--
ALTER TABLE `personalisierung_ohne_personen`
 ADD KEY `articleid` (`articleid`), ADD KEY `userid` (`userid`);

--
-- Indizes für die Tabelle `personalisierung_personen`
--
ALTER TABLE `personalisierung_personen`
 ADD KEY `articleid` (`articleid`), ADD KEY `userid` (`userid`);

--
-- Indizes für die Tabelle `vector_alle`
--
ALTER TABLE `vector_alle`
 ADD KEY `id` (`id`);

--
-- Indizes für die Tabelle `vector_ohne_personen`
--
ALTER TABLE `vector_ohne_personen`
 ADD KEY `id` (`id`);

--
-- Indizes für die Tabelle `vector_personen`
--
ALTER TABLE `vector_personen`
 ADD KEY `id` (`id`);

--
-- Indizes für die Tabelle `wikipedia`
--
ALTER TABLE `wikipedia`
 ADD PRIMARY KEY (`id`), ADD FULLTEXT KEY `body` (`body`);

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `annotationen`
--
ALTER TABLE `annotationen`
ADD CONSTRAINT `annotationen_ibfk_1` FOREIGN KEY (`nutzerid`) REFERENCES `nutzer` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `annotationen_ibfk_2` FOREIGN KEY (`artikelid`) REFERENCES `annotierte_artikel` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `interessen_vector_alle`
--
ALTER TABLE `interessen_vector_alle`
ADD CONSTRAINT `interessen_vector_alle_ibfk_1` FOREIGN KEY (`id`) REFERENCES `interessen` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `interessen_vector_ohne_personen`
--
ALTER TABLE `interessen_vector_ohne_personen`
ADD CONSTRAINT `interessen_vector_ohne_personen_ibfk_1` FOREIGN KEY (`id`) REFERENCES `interessen` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `interessen_vector_personen`
--
ALTER TABLE `interessen_vector_personen`
ADD CONSTRAINT `interessen_vector_personen_ibfk_1` FOREIGN KEY (`id`) REFERENCES `interessen` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `nutzer_interessen`
--
ALTER TABLE `nutzer_interessen`
ADD CONSTRAINT `nutzer_interessen_ibfk_1` FOREIGN KEY (`nutzerid`) REFERENCES `nutzer` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `nutzer_interessen_ibfk_2` FOREIGN KEY (`interessensid`) REFERENCES `interessen` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `personalisierung_alle`
--
ALTER TABLE `personalisierung_alle`
ADD CONSTRAINT `personalisierung_alle_ibfk_1` FOREIGN KEY (`articleid`) REFERENCES `artikel` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `personalisierung_alle_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `nutzer` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `personalisierung_ohne_personen`
--
ALTER TABLE `personalisierung_ohne_personen`
ADD CONSTRAINT `personalisierung_ohne_personen_ibfk_1` FOREIGN KEY (`articleid`) REFERENCES `artikel` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `personalisierung_ohne_personen_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `nutzer` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `personalisierung_personen`
--
ALTER TABLE `personalisierung_personen`
ADD CONSTRAINT `personalisierung_personen_ibfk_1` FOREIGN KEY (`articleid`) REFERENCES `artikel` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `personalisierung_personen_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `nutzer` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `vector_alle`
--
ALTER TABLE `vector_alle`
ADD CONSTRAINT `vector_alle_ibfk_1` FOREIGN KEY (`id`) REFERENCES `artikel` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `vector_ohne_personen`
--
ALTER TABLE `vector_ohne_personen`
ADD CONSTRAINT `vector_ohne_personen_ibfk_1` FOREIGN KEY (`id`) REFERENCES `artikel` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `vector_personen`
--
ALTER TABLE `vector_personen`
ADD CONSTRAINT `vector_personen_ibfk_1` FOREIGN KEY (`id`) REFERENCES `artikel` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
