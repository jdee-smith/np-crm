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