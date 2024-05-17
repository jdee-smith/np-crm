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
    LANGUAGE 'plpgsql'
    IMMUTABLE
    AS
    $$
    BEGIN
        RETURN POWER(y_true - y_pred, 2);
    END;
    $$;

CREATE OR REPLACE FUNCTION quantile_loss(y_true DECIMAL, y_pred DECIMAL, alpha DECIMAL)
    /*
    Returns quantile loss as a specified quantile.
    */
    RETURNS DECIMAL
    LANGUAGE 'plpgsql'
    IMMUTABLE
    AS
    $$
    DECLARE
        error DECIMAL;
        sign DECIMAL;
    BEGIN
        SELECT y_true - y_pred INTO error;
        SELECT CASE WHEN error >= 0.0 THEN 1.0 ELSE 0.0 END INTO sign;
        
        RETURN alpha * sign * error - (1 - alpha) * (1 - sign) * error;
    END;
    $$;