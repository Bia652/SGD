CREATE TABLE ticket_seat (
	ticket_id		 SERIAL,
	seat_seat_num	 VARCHAR(512),
	schedule_schedule_id INTEGER NOT NULL,
	flight_flight_id	 INTEGER NOT NULL,
	PRIMARY KEY(ticket_id)
);

CREATE TABLE booking (
	booking_code		 SERIAL,
	ticket_seat_ticket_id INTEGER NOT NULL,
	PRIMARY KEY(booking_code)
);

CREATE TABLE company (
	name VARCHAR(512)
);

CREATE TABLE flight_attendant (
	flight_num	 INTEGER,
	sys_user_user_id INTEGER,
	PRIMARY KEY(sys_user_user_id)
);

CREATE TABLE airport (
	airport_id			 INTEGER,
	name				 VARCHAR(512),
	city				 VARCHAR(512),
	country			 VARCHAR(512),
	administrator_sys_user_user_id INTEGER NOT NULL,
	PRIMARY KEY(airport_id)
);

CREATE TABLE administrator (
	sys_user_user_id INTEGER,
	PRIMARY KEY(sys_user_user_id)
);

CREATE TABLE sys_user (
	user_id	 INTEGER,
	username VARCHAR(512),
	email	 VARCHAR(512),
	password VARCHAR(512),
	PRIMARY KEY(user_id)
);

CREATE TABLE pilot (
	flight_hours	 INTEGER,
	sys_user_user_id INTEGER,
	PRIMARY KEY(sys_user_user_id)
);

CREATE TABLE flight (
	seats_num			 INTEGER,
	flight_id			 INTEGER,
	administrator_sys_user_user_id INTEGER NOT NULL,
	airport_airport_id		 INTEGER NOT NULL,
	airport_airport_id1		 INTEGER NOT NULL,
	PRIMARY KEY(flight_id)
);

CREATE TABLE schedule (
	date_time			 TIMESTAMP,
	schedule_id			 SERIAL,
	administrator_sys_user_user_id INTEGER NOT NULL,
	flight_flight_id		 INTEGER NOT NULL,
	PRIMARY KEY(schedule_id)
);

CREATE TABLE payment (
	credit_card		 FLOAT(8),
	mbway		 FLOAT(8),
	money		 FLOAT(8),
	total		 FLOAT(8),
	booking_booking_code INTEGER NOT NULL
);

CREATE TABLE costumer (
	sys_user_user_id INTEGER,
	PRIMARY KEY(sys_user_user_id)
);

CREATE TABLE booking_costumer (
	booking_booking_code	 INTEGER,
	costumer_sys_user_user_id INTEGER NOT NULL,
	PRIMARY KEY(booking_booking_code)
);

CREATE TABLE pilot_pilot (
	pilot_sys_user_user_id	 INTEGER,
	pilot_sys_user_user_id1 INTEGER NOT NULL,
	PRIMARY KEY(pilot_sys_user_user_id)
);

CREATE TABLE flight_attendant_flight_attendant (
	flight_attendant_sys_user_user_id	 INTEGER,
	flight_attendant_sys_user_user_id1 INTEGER NOT NULL,
	PRIMARY KEY(flight_attendant_sys_user_user_id)
);

CREATE TABLE pilot_schedule (
	pilot_sys_user_user_id INTEGER,
	schedule_schedule_id	 INTEGER,
	PRIMARY KEY(pilot_sys_user_user_id,schedule_schedule_id)
);

CREATE TABLE flight_attendant_schedule (
	flight_attendant_sys_user_user_id INTEGER,
	schedule_schedule_id		 INTEGER,
	PRIMARY KEY(flight_attendant_sys_user_user_id,schedule_schedule_id)
);

CREATE TABLE administrator_administrator (
	administrator_sys_user_user_id	 INTEGER,
	administrator_sys_user_user_id1 INTEGER NOT NULL,
	PRIMARY KEY(administrator_sys_user_user_id)
);

ALTER TABLE ticket_seat ADD CONSTRAINT ticket_seat_fk1 FOREIGN KEY (schedule_schedule_id) REFERENCES schedule(schedule_id);
ALTER TABLE ticket_seat ADD CONSTRAINT ticket_seat_fk2 FOREIGN KEY (flight_flight_id) REFERENCES flight(flight_id);
ALTER TABLE booking ADD UNIQUE (ticket_seat_ticket_id);
ALTER TABLE booking ADD CONSTRAINT booking_fk1 FOREIGN KEY (ticket_seat_ticket_id) REFERENCES ticket_seat(ticket_id);
ALTER TABLE flight_attendant ADD CONSTRAINT flight_attendant_fk1 FOREIGN KEY (sys_user_user_id) REFERENCES sys_user(user_id);
ALTER TABLE airport ADD CONSTRAINT airport_fk1 FOREIGN KEY (administrator_sys_user_user_id) REFERENCES administrator(sys_user_user_id);
ALTER TABLE administrator ADD CONSTRAINT administrator_fk1 FOREIGN KEY (sys_user_user_id) REFERENCES sys_user(user_id);
ALTER TABLE pilot ADD CONSTRAINT pilot_fk1 FOREIGN KEY (sys_user_user_id) REFERENCES sys_user(user_id);
ALTER TABLE flight ADD CONSTRAINT flight_fk1 FOREIGN KEY (administrator_sys_user_user_id) REFERENCES administrator(sys_user_user_id);
ALTER TABLE flight ADD CONSTRAINT flight_fk2 FOREIGN KEY (airport_airport_id) REFERENCES airport(airport_id);
ALTER TABLE flight ADD CONSTRAINT flight_fk3 FOREIGN KEY (airport_airport_id1) REFERENCES airport(airport_id);
ALTER TABLE schedule ADD CONSTRAINT schedule_fk1 FOREIGN KEY (administrator_sys_user_user_id) REFERENCES administrator(sys_user_user_id);
ALTER TABLE schedule ADD CONSTRAINT schedule_fk2 FOREIGN KEY (flight_flight_id) REFERENCES flight(flight_id);
ALTER TABLE payment ADD CONSTRAINT payment_fk1 FOREIGN KEY (booking_booking_code) REFERENCES booking(booking_code);
ALTER TABLE costumer ADD CONSTRAINT costumer_fk1 FOREIGN KEY (sys_user_user_id) REFERENCES sys_user(user_id);
ALTER TABLE booking_costumer ADD CONSTRAINT booking_costumer_fk1 FOREIGN KEY (booking_booking_code) REFERENCES booking(booking_code);
ALTER TABLE booking_costumer ADD CONSTRAINT booking_costumer_fk2 FOREIGN KEY (costumer_sys_user_user_id) REFERENCES costumer(sys_user_user_id);
ALTER TABLE pilot_pilot ADD CONSTRAINT pilot_pilot_fk1 FOREIGN KEY (pilot_sys_user_user_id) REFERENCES pilot(sys_user_user_id);
ALTER TABLE pilot_pilot ADD CONSTRAINT pilot_pilot_fk2 FOREIGN KEY (pilot_sys_user_user_id1) REFERENCES pilot(sys_user_user_id);
ALTER TABLE flight_attendant_flight_attendant ADD CONSTRAINT flight_attendant_flight_attendant_fk1 FOREIGN KEY (flight_attendant_sys_user_user_id) REFERENCES flight_attendant(sys_user_user_id);
ALTER TABLE flight_attendant_flight_attendant ADD CONSTRAINT flight_attendant_flight_attendant_fk2 FOREIGN KEY (flight_attendant_sys_user_user_id1) REFERENCES flight_attendant(sys_user_user_id);
ALTER TABLE pilot_schedule ADD CONSTRAINT pilot_schedule_fk1 FOREIGN KEY (pilot_sys_user_user_id) REFERENCES pilot(sys_user_user_id);
ALTER TABLE pilot_schedule ADD CONSTRAINT pilot_schedule_fk2 FOREIGN KEY (schedule_schedule_id) REFERENCES schedule(schedule_id);
ALTER TABLE flight_attendant_schedule ADD CONSTRAINT flight_attendant_schedule_fk1 FOREIGN KEY (flight_attendant_sys_user_user_id) REFERENCES flight_attendant(sys_user_user_id);
ALTER TABLE flight_attendant_schedule ADD CONSTRAINT flight_attendant_schedule_fk2 FOREIGN KEY (schedule_schedule_id) REFERENCES schedule(schedule_id);
ALTER TABLE administrator_administrator ADD CONSTRAINT administrator_administrator_fk1 FOREIGN KEY (administrator_sys_user_user_id) REFERENCES administrator(sys_user_user_id);
ALTER TABLE administrator_administrator ADD CONSTRAINT administrator_administrator_fk2 FOREIGN KEY (administrator_sys_user_user_id1) REFERENCES administrator(sys_user_user_id);

