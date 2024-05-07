CREATE EXTENSION citext;
CREATE DOMAIN domain_email AS citext
CHECK(VALUE ~ '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$');

CREATE TABLE
    users (
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id SERIAL,
        email_address domain_email NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (email_address)
    );

CREATE TABLE
    people (
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id SERIAL,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        PRIMARY KEY (id)
    );

CREATE TABLE
    donations (
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id INT NOT NULL,
        person_id INT NOT NULL,
        date DATE,
        amount DECIMAL(10, 2),
        method VARCHAR(255),
        PRIMARY KEY (id, person_id)
    );