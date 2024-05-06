CREATE EXTENSION citext;
CREATE DOMAIN domain_email AS citext
CHECK(VALUE ~ '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$');

CREATE TABLE
    users (
        id SERIAL,
        email_address domain_email NOT NULL UNIQUE,
        create_date DATE DEFAULT CURRENT_DATE,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (email_address)
    );

CREATE TABLE
    people (
        id SERIAL,
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