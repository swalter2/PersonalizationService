CREATE TABLE feedback_tmp (
id char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
nutzerid INT(11) NOT NULL,
feedback INT(11),
FOREIGN KEY (id) REFERENCES artikel(id) ON DELETE CASCADE,
FOREIGN KEY (nutzerid) REFERENCES nutzer(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE feedback_permanent (
id char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
nutzerid INT(11) NOT NULL,
feedback INT(11),
FOREIGN KEY (nutzerid) REFERENCES nutzer(id) ON DELETE CASCADE
) ENGINE=InnoDB;

ALTER TABLE feedback_permanent
ADD PRIMARY KEY (id,nutzerid);

CREATE TABLE IF NOT EXISTS artikel_permanent (
id char(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
titel varchar(250) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
text text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
tags text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
datum char(10) NOT NULL,
ressort varchar(255) NOT NULL,
seite int(11) NOT NULL,
anzahl_woerter int(11) NOT NULL,
FOREIGN KEY (id) REFERENCES feedback_permanent(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;