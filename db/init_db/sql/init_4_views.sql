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
        COALESCE(monthly_donation_amount.amount, 0) AS amount
    FROM 
        cte
    LEFT JOIN
        monthly_donation_amount ON monthly_donation_amount.month = cte.month;


CREATE VIEW forecasts AS
    SELECT
        id,
        type,
        series,
        date,
        ROUND(AVG(forecast), 2) AS mean,
        PERCENTILE_DISC(0.05) WITHIN GROUP (ORDER BY forecast) AS p5,
        PERCENTILE_DISC(0.1) WITHIN GROUP (ORDER BY forecast) AS p10,
        PERCENTILE_DISC(0.2) WITHIN GROUP (ORDER BY forecast) AS p20,
        PERCENTILE_DISC(0.3) WITHIN GROUP (ORDER BY forecast) AS p30,
        PERCENTILE_DISC(0.4) WITHIN GROUP (ORDER BY forecast) AS p40,
        PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY forecast) AS p50,
        PERCENTILE_DISC(0.6) WITHIN GROUP (ORDER BY forecast) AS p60,
        PERCENTILE_DISC(0.7) WITHIN GROUP (ORDER BY forecast) AS p70,
        PERCENTILE_DISC(0.8) WITHIN GROUP (ORDER BY forecast) AS p80,
        PERCENTILE_DISC(0.9) WITHIN GROUP (ORDER BY forecast) AS p90,
        PERCENTILE_DISC(0.95) WITHIN GROUP (ORDER BY forecast) AS p95
    FROM
        sample_forecasts
    GROUP BY
        id, series, date, type
    ORDER BY
        id, series, date;


CREATE VIEW item_level_forecast_metrics AS
    WITH cte as (
        SELECT
            f.*,
            a.amount as actual
        FROM forecasts f
        LEFT JOIN monthly_donation_amount a ON f.date = a.month WHERE f.type = 'Donations'
    )

    SELECT
        id,
        series,
        AVG(SQUARED_ERROR(actual, mean)) as mse,
        AVG(QUANTILE_LOSS(actual, p5, 0.05)) as mql_p5,
        AVG(QUANTILE_LOSS(actual, p10, 0.1)) as mql_p10,
        AVG(QUANTILE_LOSS(actual, p20, 0.2)) as mql_p20,
        AVG(QUANTILE_LOSS(actual, p30, 0.3)) as mql_p30,
        AVG(QUANTILE_LOSS(actual, p40, 0.4)) as mql_p40,
        AVG(QUANTILE_LOSS(actual, p50, 0.5)) as mql_p50,
        AVG(QUANTILE_LOSS(actual, p60, 0.6)) as mql_p60,
        AVG(QUANTILE_LOSS(actual, p70, 0.7)) as mql_p70,
        AVG(QUANTILE_LOSS(actual, p80, 0.8)) as mql_p80,
        AVG(QUANTILE_LOSS(actual, p90, 0.9)) as mql_p90,
        AVG(QUANTILE_LOSS(actual, p95, 0.95)) as mql_p95
    FROM 
        cte
    GROUP BY
        id, series;

CREATE VIEW aggregate_forecast_metrics AS
    SELECT
        id,
        AVG(mse) as mse,
        AVG(mql_p5) as mql_p5,
        AVG(mql_p10) as mql_p10,
        AVG(mql_p20) as mql_p20,
        AVG(mql_p30) as mql_p30,
        AVG(mql_p40) as mql_p40,
        AVG(mql_p50) as mql_p50,
        AVG(mql_p60) as mql_p60,
        AVG(mql_p70) as mql_p70,
        AVG(mql_p80) as mql_p80,
        AVG(mql_p90) as mql_p90,
        AVG(mql_p95) as mql_p95
    FROM
        item_level_forecast_metrics
    GROUP BY
        id;