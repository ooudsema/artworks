SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS era, medium, movement, artwork, artwork_subject, subject, artist, country, temp_art, temp_json, subject_list;
SET FOREIGN_KEY_CHECKS=1;


CREATE TABLE IF NOT EXISTS era
  (
    era_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    era_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (era_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO era (era_name) VALUES
  ('18th century'), ('19th century'), ('20th century post-1945');

CREATE TABLE IF NOT EXISTS movement
  (
    movement_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movement_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (movement_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO movement (movement_name) VALUES
  ('Geometry of Fear'), ('Orientalist'), ('Picturesque'), ('Pre-Raphaelite Brotherhood'), ('Romanticism'), 
  ('Shoreham / The Ancients'), ('Sublime'), ('Victorian/Genre');


CREATE TABLE IF NOT EXISTS medium
  (
    medium_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    medium_name VARCHAR(250) NOT NULL UNIQUE,
    PRIMARY KEY (medium_id)
  )

ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/USER/Desktop/artworks/SI664-scripts-master/scripts/output/art_medium.csv'
INTO TABLE medium
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
(medium_name)

SET medium_name = IF(medium_name = '', NULL, medium_name);


CREATE TABLE IF NOT EXISTS artist
  (
    artist_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artist_last_name VARCHAR(300),
    artist_first_name VARCHAR(100),
    PRIMARY KEY (artist_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/USER/Desktop/artworks/SI664-scripts-master/scripts/output/artistCleaned.csv'
INTO TABLE artist
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
(artist_last_name, artist_first_name)

SET artist_last_name = IF(artist_last_name = '', NULL, artist_last_name),
artist_first_name = IF(artist_first_name = '', NULL, artist_first_name);

CREATE TABLE IF NOT EXISTS subject
  (
    subject_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    subject_name VARCHAR(250),
    PRIMARY KEY (subject_id)
  )


ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/USER/Desktop/artworks/SI664-scripts-master/scripts/output/subjects_unique.csv'
INTO TABLE subject
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
(subject_name)

SET subject_name = IF(subject_name = '', NULL, subject_name);


CREATE TABLE IF NOT EXISTS artwork
  (
    artwork_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    accession_number VARCHAR(250),
    artwork_title VARCHAR(500),
    artwork_date VARCHAR(200),
    artist_id INTEGER,
    era_id INTEGER,
    movement_id INTEGER,
    medium_id INTEGER,
    PRIMARY KEY (artwork_id),
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (era_id) REFERENCES era(era_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (movement_id) REFERENCES movement(movement_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (medium_id) REFERENCES medium(medium_id) ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET latin1
COLLATE latin1_swedish_ci;

CREATE TABLE IF NOT EXISTS artwork_subject
  (
    artwork_subject_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artwork_id INTEGER,
    subject_id INTEGER,
    PRIMARY KEY (artwork_subject_id),
    FOREIGN KEY (artwork_id) REFERENCES artwork(artwork_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id) ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- CREATE TEMPORARY TABLE temp_art

CREATE TEMPORARY TABLE temp_art
(
    temp_art_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    tate_art_id INTEGER,
    accession_number VARCHAR(100),
    artist VARCHAR(100),
    lastname VARCHAR(100),
    firstname VARCHAR(100),
    tate_artist_id INTEGER,
    title VARCHAR(500),
    datetext VARCHAR(100),
    medium TEXT,
    PRIMARY KEY (temp_art_id)
 )

ENGINE=InnoDB
CHARACTER SET latin1
COLLATE latin1_swedish_ci;

LOAD DATA LOCAL INFILE '/Users/USER/Desktop/artworks/SI664-scripts-master/scripts/artwork_data_a.csv'
INTO TABLE temp_art
CHARACTER SET latin1
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(tate_art_id, accession_number, artist, lastname, firstname, tate_artist_id, title, datetext, medium)

SET accession_number= IF(accession_number = '', NULL, accession_number),
artist = IF(artist = '', NULL, artist),
lastname = IF(lastname = '', NULL, lastname),
firstname = IF(firstname = '', NULL, firstname),
tate_artist_id = IF(tate_artist_id = '', NULL, tate_artist_id), 
title = IF(title = '', NULL, title),
datetext = IF(datetext = '', NULL, datetext),
medium = IF(medium = '', NULL, medium);

CREATE TEMPORARY TABLE temp_json
(
    temp_json_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    accession_number VARCHAR(100),
    title VARCHAR(500),
    medium TEXT,
    movement VARCHAR(200),
    era VARCHAR(200),
    subject VARCHAR(250), 
    datetext VARCHAR(250),
    PRIMARY KEY (temp_json_id)
 )

ENGINE=InnoDB
CHARACTER SET latin1
COLLATE latin1_swedish_ci;

LOAD DATA LOCAL INFILE '/Users/USER/Desktop/artworks/SI664-scripts-master/scripts/artworksjson_cleaned.csv'
INTO TABLE temp_json
CHARACTER SET latin1
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
(accession_number, title, medium, movement, era, subject, datetext)

SET accession_number= IF(accession_number = '', NULL, accession_number),
title = IF(title = '', NULL, title),
medium = IF(medium = '', NULL, medium),
movement = IF(movement = '', NULL, movement),
era = IF(era = '', NULL, era),
subject = IF(subject = '', NULL, subject),
datetext = IF(datetext = '', NULL, datetext);

INSERT IGNORE INTO artwork (accession_number, artwork_title, artwork_date, artist_id,
       era_id, movement_id, medium_id)
SELECT temp_json.accession_number,
       temp_json.title,
       temp_json.datetext,
       artist.artist_id,
       era.era_id,
       movement.movement_id,
       medium.medium_id
  FROM temp_json
      LEFT JOIN artwork
              ON artwork.accession_number = temp_json.accession_number
      LEFT JOIN temp_art 
        ON temp_json.accession_number = temp_art.accession_number
      LEFT JOIN artist
        ON artist.artist_first_name = temp_art.firstname AND artist.artist_last_name = temp_art.lastname
      LEFT JOIN era
        ON era.era_name = temp_json.era
      LEFT JOIN movement 
        ON movement.movement_name = temp_json.movement
      LEFT JOIN medium 
        ON TRIM(medium.medium_name) = TRIM(temp_json.medium)
 ORDER BY artwork.accession_number;

CREATE TEMPORARY TABLE subject_list
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    accession_number VARCHAR(100) NOT NULL,
    subject_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (id)
  )

ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/USER/Desktop/artworks/SI664-scripts-master/scripts/output/artwork_subjects.csv'
INTO TABLE subject_list
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
(accession_number, subject_name);

INSERT IGNORE INTO artwork_subject (artwork_id, subject_id)
SELECT artwork.artwork_id,
       subject.subject_id
  FROM subject_list
       LEFT JOIN artwork
              ON TRIM(subject_list.accession_number) = TRIM(artwork.accession_number)
       LEFT JOIN subject
              ON TRIM(subject_list.subject_name) = TRIM(subject.subject_name)
 ORDER BY subject_list.id;

 DROP TEMPORARY TABLE temp_art, temp_json, subject_list;