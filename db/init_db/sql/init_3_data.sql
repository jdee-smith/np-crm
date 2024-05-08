INSERT INTO users (id, email_address, password)
VALUES (1, 'superuser@example.com', 'superuser');

COPY people (id, first_name, last_name)
FROM '/db-data/people.csv'
HEADER CSV DELIMITER ',';

COPY donations (id, person_id, date, amount, method)
FROM '/db-data/donations.csv'
HEADER CSV DELIMITER ',';