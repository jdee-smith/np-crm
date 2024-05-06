INSERT INTO users (email_address, password)
VALUES ('superuser@example.com', 'superuser');

COPY people (first_name, last_name)
FROM '/db-data/people.csv'
HEADER CSV DELIMITER ',';

COPY donations (id, person_id, date, amount, method)
FROM '/db-data/donations.csv'
HEADER CSV DELIMITER ',';

/*
LOAD DATA INFILE
    '/db-data/people.csv'
INTO TABLE
    people
FIELDS TERMINATED BY
    ','
IGNORE 
    1 LINES
(first_name, last_name);


LOAD DATA INFILE
    '/db-data/donations.csv'
INTO TABLE
    donations
FIELDS TERMINATED BY
    ','
IGNORE
    1 LINES
(id, person_id, date, amount, method);
*/