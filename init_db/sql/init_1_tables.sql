CREATE TABLE 
    population (
        id INT NOT NULL AUTO_INCREMENT, 
        state VARCHAR(255), 
        state_code VARCHAR(255), 
        state_code_id INT, 
        year INT, 
        population INT,
        PRIMARY KEY (id)
    );

CREATE TABLE
    donations (
        id INT NOT NULL AUTO_INCREMENT,
        person_id INT,
        date DATE,
        amount DECIMAL(10, 2),
        method ENUM(
            'Cash',
            'Credit',
            'Debit',
            'Check',
            'Other'
            ),
        PRIMARY KEY (id)
    );

/*
transaction_id (PK)
person_id
date
gift amount
frequency of giving
method of giving (cash, credit, debit, PayPal, check, etc.)
Lifetime value view
upgrade/downgrade view
donor pyramid
*/

CREATE TABLE
    people (
        id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        PRIMARY KEY (id)
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