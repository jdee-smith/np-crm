CREATE OR REPLACE FUNCTION last_day(date)
    /*
    Returns the last day in the month from a date.
    */
    RETURNS date
    LANGUAGE 'sql'
    IMMUTABLE STRICT
    AS
    $$
        SELECT (DATE_TRUNC('MONTH', $1) + INTERVAL '1 MONTH - 1 day')::date;
    $$;

CREATE OR REPLACE FUNCTION month(date)
    /*
    Returns the month from a date.
    */
    RETURNS integer
    LANGUAGE 'sql'
    IMMUTABLE
    AS
    $$
        SELECT EXTRACT(MONTH FROM $1)::integer;
    $$;

CREATE OR REPLACE FUNCTION year(date)
    /*
    Returns the year from a date.
    */
    RETURNS integer
    LANGUAGE 'sql'
    IMMUTABLE
    AS
    $$
        SELECT EXTRACT(YEAR FROM $1)::integer;
    $$;

CREATE OR REPLACE FUNCTION squared_error(y_true DECIMAL, y_pred DECIMAL)
    /*
    Returns the squared error.
    */
    RETURNS DECIMAL
    LANGUAGE 'sql'
    IMMUTABLE
    AS
    $$
        SELECT POWER(y_true - y_pred, 2);
    $$;