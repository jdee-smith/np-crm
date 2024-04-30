USE db;

CREATE TABLE
    people (
        id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        PRIMARY KEY (id)
    );

CREATE TABLE
    donations (
        id INT NOT NULL,
        person_id INT NOT NULL,
        date DATE,
        amount DECIMAL(10, 2),
        method VARCHAR(255),
        PRIMARY KEY (id, person_id)
    );

/*
person_id (PK)
Demographics (DOB, gender),
name,
home address (address, city, state zip),
income
employer,
email address,
phone number,
social media
*/

/* events, places, users, volunteers */