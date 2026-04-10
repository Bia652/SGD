-- Add sys_user--
CREATE OR REPLACE PROCEDURE add_sys_user( 
    user_id sys_user.user_id%TYPE,
    username sys_user.username%TYPE,
    email sys_user.email%TYPE,
    password sys_user.password%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN 
    INSERT INTO sys_user (user_id, username, email, password)
    VALUES (user_id, username, email, password);

EXCEPTION
	WHEN unique_violation THEN
		raise exception 'The user_id already exists!!';
	WHEN others THEN
		raise exception 'error: %', SQLERRM;
END;
$$;

-- Add administrador to sys_userand to administrador table --
CREATE OR REPLACE PROCEDURE add_administrator (
    user_id sys_user.user_id%TYPE,
    username sys_user.username%TYPE,
    email sys_user.email%TYPE,
    password sys_user.password%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
    CALL add_sys_user (user_id, username, email, password);
    INSERT INTO administrator (sys_user_user_id)
    VALUES (user_id);
EXCEPTION
	WHEN unique_violation THEN
		raise exception 'The id already exists!!';
	WHEN others THEN
		raise exception 'error: %', SQLERRM;
END;
$$;

-- Add flight_attendant to sys_userand to flight_attendant table --
CREATE OR REPLACE PROCEDURE add_flight_attendant (
    user_id sys_user.user_id%TYPE,
    username sys_user.username%TYPE,
    email sys_user.email%TYPE,
    password sys_user.password%TYPE,
    flight_num flight_attendant.flight_num%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
    CALL add_sys_user(user_id, username, email, password);
    INSERT INTO flight_attendant (flight_num,sys_user_user_id)
    VALUES (flight_num,user_id);
EXCEPTION
	WHEN unique_violation THEN
		raise exception 'The id already exists!!';
	WHEN others THEN
		raise exception 'error: %', SQLERRM;
END;
$$;

-- Add pilot to sys_userand to pilot table --
CREATE OR REPLACE PROCEDURE add_pilot (
    user_id sys_user.user_id%TYPE,
    username sys_user.username%TYPE,
    email sys_user.email%TYPE,
    password sys_user.password%TYPE,
    flight_hours pilot.flight_hours%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
    CALL add_sys_user(user_id, username, email, password);
    INSERT INTO pilot (flight_hours, sys_user_user_id)
    VALUES (flight_hours,user_id);

EXCEPTION
	WHEN unique_violation THEN
		raise exception 'The id already exists!!';
	WHEN others THEN
		raise exception 'error: %', SQLERRM;
END;
$$;

CREATE OR REPLACE PROCEDURE add_costumer (
    user_id sys_user.user_id%TYPE,
    username sys_user.username%TYPE,
    email sys_user.email%TYPE,
    password sys_user.password%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
    CALL add_sys_user(user_id, username, email, password);
    INSERT INTO costumer(sys_user_user_id)
    VALUES (user_id);

EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'The id already exists!!';
    WHEN others THEN
        RAISE EXCEPTION 'error: %', SQLERRM;
END;
$$;

CREATE OR REPLACE PROCEDURE add_airport (
    airport_id airport.airport_id%TYPE,
	name airport.name%TYPE,
	city airport.city%TYPE,
	country	airport.country%TYPE,
	creator airport.administrator_sys_user_user_id%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
    VALUES (airport_id, name, city, country, creator);

EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'That airport id already exists!!';
    WHEN others THEN
        RAISE EXCEPTION 'error: %', SQLERRM;
END;
$$;

-- Add flight --
CREATE OR REPLACE PROCEDURE add_flight(
    seats_num flight.seats_num%TYPE, 
    flight_id flight.flight_id%TYPE, 
	origin flight.airport_airport_id%TYPE, 
	destiny flight.airport_airport_id1%TYPE, 
    creator flight.administrator_sys_user_user_id %TYPE
)
LANGUAGE plpgsql 
AS $$
BEGIN 
    INSERT INTO flight(seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
    VALUES(seats_num, flight_id, creator, origin, destiny);
EXCEPTION 
    WHEN unique_violation THEN
         RAISE EXCEPTION 'That flight id already exists!!';
    WHEN others THEN
        RAISE EXCEPTION 'error: %', SQLERRM;
END;
$$

-- Add schedule to schedule table --
CREATE OR REPLACE PROCEDURE add_schedule(
    date_time schedule.date_time%TYPE, 
    creator schedule.administrator_sys_user_user_id%TYPE,
	flight_id schedule.flight_flight_id%TYPE
)
LANGUAGE plpgsql 
AS $$
BEGIN 
    INSERT INTO schedule(date_time, administrator_sys_user_user_id, flight_flight_id)
    VALUES(date_time, creator, flight_id);
EXCEPTION 
    WHEN others THEN
        RAISE EXCEPTION 'error: %', SQLERRM;
END
$$;

-- INITIAL TABLE INFO --
-- Users: --
INSERT INTO sys_user (user_id, username, email, password) 
VALUES (1, 'admin1', 'admin1@example.com','$2b$12$5sMmIw/u/EK7kxt9MK569e/ndaQ8IMVhnFhVHMiMlkIczP8th96Tq')

INSERT INTO administrator (sys_user_user_id) 
VALUES (1)

INSERT INTO sys_user (user_id, username, email, password) 
VALUES (2, 'flight_attendant1', 'flight_attendant1@example.com','$2b$12$5sMmIw/u/EK7kxt9MK569e/ndaQ8IMVhnFhVHMiMlkIczP8th96Tq')

INSERT INTO flight_attendant (flight_num, sys_user_user_id) 
VALUES (26, 2)

INSERT INTO sys_user (user_id, username, email, password) 
VALUES (3, 'pilot1', 'pilot1@example.com', '$2b$12$5sMmIw/u/EK7kxt9MK569e/ndaQ8IMVhnFhVHMiMlkIczP8th96Tq')

INSERT INTO pilot (flight_hours, sys_user_user_id) 
VALUES (150, 3)

INSERT INTO sys_user (user_id, username, email, password) 
VALUES (4, 'costumer1', 'costumer1@example.com', '$2b$12$5sMmIw/u/EK7kxt9MK569e/ndaQ8IMVhnFhVHMiMlkIczP8th96Tq')

INSERT INTO costumer (sys_user_user_id) 
VALUES (4)

-- Airports: --
INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
VALUES (1, 'Lisbon International Airport', 'Lisbon', 'Portugal', 1);

INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
VALUES (2, 'John F. Kennedy International Airport', 'New York', 'USA', 1);

INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
VALUES (3, 'Tokyo Haneda Airport', 'Tokyo', 'Japan', 1);

INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
VALUES (4, 'Heathrow Airport', 'London', 'UK', 1);

INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
VALUES (5, 'Charles de Gaulle Airport', 'Paris', 'France', 1);

INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
VALUES (6, 'Dubai International Airport', 'Dubai', 'UAE', 1);

INSERT INTO airport (airport_id, name, city, country, administrator_sys_user_user_id)
VALUES (7, 'Sydney Kingsford Smith Airport', 'Sydney', 'Australia', 1);


-- Flights: --
INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (180, 1, 1, 5, 6);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (220, 2, 1, 7, 5);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (200, 3, 1, 6, 7);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (250, 4, 1, 5, 7);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (190, 5, 1, 6, 5);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (240, 6, 1, 7, 6);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (230, 7, 1, 5, 7);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (210, 8, 1, 7, 6);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (200, 9, 1, 6, 5);

INSERT INTO flight (seats_num, flight_id, administrator_sys_user_user_id, airport_airport_id, airport_airport_id1)
VALUES (260, 10, 1, 5, 6);

