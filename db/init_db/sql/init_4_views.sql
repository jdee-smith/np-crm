/*
Shows the total amount donated for each person over all 
time.
*/
CREATE VIEW lifetime_value AS
    /*
    For anyone that has ever donated, get the
    sum of their donations.
    */
    WITH cte AS (
        SELECT
            person_id,
            SUM(amount) as lifetime_value
        FROM
            donations
        GROUP BY
            person_id
    )
    /*
    If a person has ever donated, merge in their
    lifetime amount. If a person has never donated,
    set their lifetime value to 0.00. The result
    is ALL people and the sum of their donations.
    */
    SELECT
        people.first_name,
        people.last_name,
        COALESCE(cte.lifetime_value, 0.00) as lifetime_value
    FROM
        people
    LEFT JOIN
        cte ON people.id = cte.person_id
    ORDER BY
        lifetime_value DESC;

/*
Shows the total amount donated for each month.
*/
CREATE VIEW monthly_donation_amount AS
    WITH cte AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY id ORDER BY id) AS r
        FROM
            donations
    )
    /*
    Compute the sum of all donations for each month using. Use 
    only 1 row from each donation in the calculation.
    */
    SELECT
        LAST_DAY(date) AS month,
        SUM(amount) AS amount
    FROM
        cte
    WHERE
        r = 1
    GROUP BY
        LAST_DAY(date)
    ORDER BY
        month ASC;

/*
Shows an expanded view of the total donation amount by month.
Values for months where there are no donations are filled with Null.
*/
CREATE VIEW monthly_donation_amount_expanded AS
    /*
    Create a list of months beginning with the first month in which 
    there was a donation and ending in the current month.
    */
    WITH RECURSIVE cte AS (
        SELECT
            (SELECT LAST_DAY(CAST(MIN(date) AS date)) AS date FROM donations) as month
        UNION ALL
        SELECT
            LAST_DAY(CAST(month + INTERVAL '1' MONTH as date))
        FROM
            cte
        WHERE
            month < (SELECT LAST_DAY(CURRENT_DATE))
    )
    /*
    Left join the donations table, leaving months without donation
    information as Null.
    */
    SELECT
        cte.month,
        monthly_donation_amount.amount AS amount
    FROM 
        cte
    LEFT JOIN
        monthly_donation_amount ON monthly_donation_amount.month = cte.month;