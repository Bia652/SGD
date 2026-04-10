from flask import Flask, jsonify, request
import logging
import psycopg2
import time
import bcrypt
import jwt

app = Flask(__name__) 

@app.route('/')
def initial_page():
    return """Welcome!"""

#### 1.REGISTER USER ####
@app.route("/register/<user_role>", methods=['POST'], strict_slashes=True)
def add_sys_user(user_role):
    conn = db_connection()
    cur = conn.cursor()
    logger.info("---- POST / register sys_user ----") 
    payload = request.get_json()
    logger.debug(f'req: {payload}') 

    keys = ["user_id", "username", "email", "password"]
    
    if user_role == 'flight_attendant':
        keys += ["flight_num"]
    elif user_role == 'pilot':
        keys += ["flight_hours"]
    if not all(key in payload for key in keys):
        logger.error("Incomplete payload!")
        return jsonify({
            "status": 400,
            "errors": f"Incomplete payload! Please ensure the following fields are provided: {', '.join(keys)}",
            "results": None
        }), 400

    password_input = payload['password']
    password_bytes = password_input.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

    if user_role == 'administrator':
        autenticate, admin_id = verify_token("administrator")
        if autenticate['results'] == 'Token not found!':
            return jsonify(autenticate)
        message = '---- New administrator ----'
        statement = 'CALL add_administrator (%s::int, %s::varchar, %s::varchar, %s::varchar)'
        values = (
            payload['user_id'], 
            payload['username'], 
            payload['email'], 
            hashed_password
        )
    elif user_role == 'flight_attendant':
        message = '---- New flight_attendant ----'
        statement = 'CALL add_flight_attendant (%s::int, %s::varchar, %s::varchar, %s::varchar, %s::int)'
        values = (
            payload["user_id"], 
            payload["username"], 
            payload["email"], 
            hashed_password, 
            payload["flight_num"]
        )
    elif user_role == 'pilot':
        message = '---- New pilot ----'
        statement = 'CALL add_pilot (%s::int, %s::varchar, %s::varchar, %s::varchar, %s::int)'
        values = (
            payload["user_id"], 
            payload["username"], 
            payload["email"], 
            hashed_password,
            payload["flight_hours"]
        )
    elif user_role == 'costumer': 
        message = '---- New costumer ----'
        statement = 'CALL add_costumer (%s::int, %s::varchar, %s::varchar, %s::varchar)'
        values = (
            payload["user_id"], 
            payload["username"], 
            payload["email"], 
            hashed_password
        )
    else:
        res = {"status": 400, 
                "errors": f"Invalid user role: {user_role}", 
                "results": None}, 400
    try:
        cur.execute(statement, values)
        conn.commit()
        logger.debug (message)
        res = {"status": 200, 
                  "errors": None, 
                  "results": payload ["user_id"]}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {"status": 500, 
                  "errors": str(error), 
                  "results": None}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    logger.debug(f'res: {res}')
    return jsonify(res)

#### 2. LOGIN USER ####
@app.route("/login", methods=['PUT'])
def login_user():
    logger.info("---- PUT / login ----");   
    payload = request.get_json()
    logger.debug (f'req: {payload}')
    conn = db_connection()
    cur = conn.cursor()

    if "username" not in payload or "password" not in payload:
        res = {'status': 400,
               'errors': None, 
               'results': 'Username or password are required to login!'}
        return jsonify(res)
    
    statement = '''SELECT user_id, password FROM sys_user WHERE username = %s'''

    values = (payload["username"],)

    try:
        cur.execute(statement, values)
        result = cur.fetchone()
        if result is None:
            res = {'status': 400,
                   'errors': None, 
                   'results': 'User not found!!'}
            return jsonify(res)
        else:
            password = payload ["password"].encode('utf-8')
            password_db = result[1].encode ('utf-8')
            if not bcrypt.checkpw(password, password_db):
                res = {'status': '400', 'errors': None,'results': 'Wrong password!'}
                return jsonify(res)
            user_id = str(result[0])
            cur.execute ('''SELECT sys_user_user_id FROM administrator WHERE sys_user_user_id = %s''', (user_id,))
            id_exists = cur.fetchone ()
            if id_exists is None:
                cur.execute ('''SELECT sys_user_user_id FROM flight_attendant WHERE sys_user_user_id = %s''', (user_id,))
                id_exists = cur.fetchone ()
                if id_exists is None:
                    cur.execute ('''SELECT sys_user_user_id FROM pilot WHERE sys_user_user_id = %s''', (user_id,))
                    id_exists = cur.fetchone ()
                    if id_exists is None:
                        user_role = "costumer"   
                    else:
                        user_role = "pilot"
                else:
                    user_role = "flight_attendant"
            else:
                user_role = "administrator"

        user_inf = {"user_id": user_id, "role" : user_role}
        token = jwt.encode(payload = user_inf, key = 'secret', algorithm = 'HS256') 
        res = {"status": 200, 
               "errors": None, 
               "results": token}         

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {"status": 500, 
               "errors": str(error), 
               "results": None}
    finally:
        if conn is not None:
            conn.close()

    logger.debug(f'res: {res}')
    return jsonify(res)

def verify_token(allowedUser):
    authorization_header = request.headers.get('Authorization')

    if authorization_header and authorization_header.startswith('Bearer '):
        # extracts token
        token = authorization_header.split(' ')[1]
        # decodes token
        decoded_token = jwt.decode(token, 'secret', algorithms = "HS256")
        # extracts and verifies user type
        if not decoded_token['role'] == allowedUser:
            # user cannot use this endpoint
            response = {'status': 400, 
                        'errors': None,
                        'results': 'User is not authorized!'}
            return response, 0
        response = {'status': 200, 
                      'errors': None, 
                      'results': 'User Authorized!'}
        return response, decoded_token['user_id'] 
    else:
        response = {'status': 400, 
                    'errors': None,
                    'results': 'Token not found!'}
        return response, 0
    
#### 3. ADD AIRPORT ####
@app.route("/airport", methods=['POST'])
def add_airport():
    autenticate, admin_id = verify_token("administrator")
    if autenticate['results'] == 'Token not found!':
        return jsonify(autenticate)
    
    logger.info ("---- POST / airport ----")
    payload = request.get_json()
    keys = ["airport_id", "name", "city", "country"]
    if not all(key in payload for key in keys):
        logger.error("Incomplete payload!")
        return jsonify ({
            "status": 400,
            "errors": "Incomplete payload! Please ensure 'airport_id', 'name', 'city' and 'country' are provided correctly!",
            "results": None
        })

    logger.debug(f'payload: {payload}')

    conn = db_connection()
    cur = conn.cursor()
    
    verify_id = '''SELECT airport_id FROM airport WHERE airport_id = %s'''
    cur.execute (verify_id, (payload ["airport_id"],))
    exists = cur.fetchone ()

    if (exists != None):
        logger.error("Airport id already exists!")
        res = {'status': 400,
            'errors': None, 
            'results': 'Airport id already exists!'}
        return jsonify(res)
    
    logger.debug(f'payload: {payload}')
    
    try:
        statement = 'CALL add_airport (%s::int, %s::varchar, %s::varchar, %s::varchar, %s:: int)'
        values = (payload ["airport_id"],payload["name"], payload["city"], payload["country"], admin_id)
   
        cur.execute(statement, values)
        conn.commit()
        logger.info("---- New airport ----")
        res = {
            "status": 200,
            "errors": None,
            "results": payload ["airport_id"]
        }
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }
    finally:
        if conn is not None:
            conn.close()
    
    logger.debug(f'res: {res}')
    return jsonify(res)


#### 4. CREATE A FLIGHT ####
@app.route("/flight", methods=['POST'])
def add_flight():
    autenticate, admin_id = verify_token("administrator")
    if autenticate['results'] == 'Token not found!':
        return jsonify(autenticate)
    
    logger.info("---- POST / flight ----")  
    payload = request.get_json ()
    logger.debug(f'req: {payload}')

    conn = db_connection()
    cur = conn.cursor()

    keys = ["seats_num", "flight_id", "origin", "destiny"]
    if not all(key in payload for key in keys):
        logger.error("Incomplete payload!")
        return jsonify ({
            "status": 400,
            "errors": "Incomplete payload! Please ensure 'seats_num', 'flight_id', 'origin' and 'destiny' are provided correctly!",
            "results": None
        })
    
    cur.execute ('''SELECT airport_id FROM airport WHERE airport_id = %s''', (payload["origin"],))
    origin_exists = cur.fetchone ()
    if origin_exists is None:
        logger.error ("Airport (origin) id does not exist!")
        res = {'status': 400,
               'errors': None, 
               'results': 'Airport (origin) id does not exist!'}
        return jsonify(res)
    
    cur.execute ('''SELECT airport_id FROM airport WHERE airport_id = %s''', (payload["destiny"],))
    destiny_exists = cur.fetchone ()
    if destiny_exists is None:
        logger.error("Airport (destiny) id does not exist!")
        res = {'status': 400,
               'errors': None, 
               'results': 'Airport (destiny) id does not exist!'}
        return jsonify(res)

    if (payload ["origin"] == payload ["destiny"]):
        logger.error("Unable to create flight with same origin and destiny!")
        res = {'status': 400,
               'errors': None, 
               'results': 'Unable to create flight with same origin and destiny!'}
        return jsonify(res)

    statement = 'CALL add_flight (%s::int, %s::int, %s::int, %s::int, %s::int)'
    values = (payload ["seats_num"], payload ["flight_id"], payload ["origin"], payload ["destiny"], admin_id,)

    try:
        cur.execute (statement, values)
        cur.execute ("commit")
        logger.info ('---- New flight ----')
        res = {'status': 200,
               'errors': None, 
               'results': payload ["flight_id"]}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }
    finally:
        if conn is not None:
            conn.close()
    
    logger.debug(f'res: {res}')
    return jsonify(res)

#### 5. CREATE SCHEDULE ####
@app.route("/schedule", methods=['POST'])
def add_schedule():
    autenticate, admin_id = verify_token("administrator")
    if autenticate['results'] == 'Token not found!':
        return jsonify(autenticate)

    logger.info("---- POST / schedule----");   
    payload = request.get_json()
    logger.debug (f'req: {payload}')

    conn = db_connection()
    cur = conn.cursor()

    keys = ["date_time", "flight_id"]
    if not all(key in payload for key in keys):
        logger.error("Incomplete payload!")
        return jsonify ({
            "status": 400,
            "errors": "Incomplete payload! Please ensure 'date_time' and 'flight_id' are provided correctly!",
            "results": None
        })
    
    cur.execute ('SELECT flight_id FROM flight WHERE flight_id = %s', (payload ["flight_id"],))
    flight_exists = cur.fetchone ()
    if flight_exists is None:
        logger.error("Flight id does not exist!")
        res = {'status': 400,
               'errors': None, 
               'results': 'Flight id does not exist!'}
        return jsonify(res)
    
    cur.execute ('''SELECT date_time FROM schedule WHERE date_time = %s and flight_flight_id = %s''', (payload ["date_time"],payload ["flight_id"],))
    same_date = cur.fetchone ()
    if same_date is not None:
        logger.error("There is already a flight with the same id on the given date!")
        res = {'status': 400,
               'errors': None, 
               'results': 'There is already a flight with the same id on the given date!'}
        return jsonify(res)

    statement = 'CALL add_schedule (%s::timestamp, %s::int, %s::int)'             
    values = (payload["date_time"],admin_id, payload["flight_id"])

    try:
        cur.execute(statement, values)
        conn.commit()
        cur.execute ('''SELECT schedule_id FROM schedule WHERE date_time = %s and flight_flight_id = %s''', (payload ["date_time"],payload ["flight_id"],))
        schedule = cur.fetchone ()
        id = schedule[0]
        logger.info("---- New schedule  ----")
        res = {
            "status": 200,
            "errors": None,
            "results": id
        }

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }

    try:
        cur.execute ('''SELECT seats_num FROM flight WHERE flight_id = %s''', (payload["flight_id"],))
        conn.commit()
        create_tickets( payload ["flight_id"], id, cur)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }

    finally:
        if conn is not None:
            conn.close()

    logger.debug(f'res: {res}')
    return jsonify(res)

#### TO ADD TICKETS TO THE TICKET_SEAT TABLE WHEN A SCHEDULE IS CREATED ####
def create_tickets(flight_id, schedule_id, cur):
    try:
        cur.execute('SELECT seats_num FROM flight WHERE flight_id = %s', (flight_id,))
        num_seats = cur.fetchone()[0]
        alpha = 'ABCDEF'
        tickets = []

        for i in range(num_seats):
            l = alpha[i % 6]
            q = str(i // 7 + 1)
            seat = q + l
            tickets.append((seat, schedule_id, flight_id))
        
        logger.debug(f"Batch inserting {len(tickets)} tickets")
        cur.executemany('''
            INSERT INTO ticket_seat (seat_seat_num, schedule_schedule_id, flight_flight_id)
            VALUES (%s, %s, %s)
        ''', tickets)
    except Exception as error:
        logger.error(f"Failed during batch ticket creation: {error}")
        raise 

#### 6. CHECK AVAILABLE ROUTES ####
@app.route("/check_routes", methods=['GET'])
def getRoutes():
    logger.info("---- GET / routes ----");   
    conn = db_connection()
    cur = conn.cursor()

    payload = request.get_json()
    logger.debug(f'req: {payload}')

    origin = payload["origin"]
    destiny = payload["destiny"]

    statement = """
    SELECT flight_id, seats_num, airport_airport_id, airport_airport_id1, schedule.date_time
    FROM flight
    JOIN schedule ON flight.flight_id = schedule.flight_flight_id
    """
    
    conditions = []
    if origin is not None:
        conditions.append(f"flight.airport_airport_id = '{origin}'")
    if destiny is not None:
        conditions.append(f"flight.airport_airport_id1 = '{destiny}'")
    
    if conditions is not None:
        statement += " WHERE " + " AND ".join(conditions) 

    cur.execute(statement)
    rows = cur.fetchall()

    results = []
    for row in rows:
        route = {
            "origin": row[2],
            "destiny": row[3],
            "flight_id": row[0],
            "schedules": row[4]
        }
        results.append(route)
    try:
        cur.execute(statement)
        logger.info ("---- Routes with the given info ----")
        res ={
        "status": 200,
        "errors": None,
        "results": results
        }
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }
    finally:
        if conn is not None:
            conn.close()

    logger.debug(f'res: {res}')
    return jsonify(res)

#### 7. CHECK AVAILABLE SEATS ####
@app.route("/check_seats", methods=['GET'])
def check_seats ():
    logger.info("---- GET / check available seats ----") 
    conn = db_connection ()
    cur = conn.cursor ()
    payload = request.get_json ()

    keys = ["flight_id","schedule_id"]
    if not all(key in payload for key in keys):
        logger.error("Incomplete payload!")
        return jsonify ({
            "status": 400,
            "errors": "Incomplete payload! Please ensure 'flight_id' and 'schedule_id' are provided correctly!",
            "results": None
        }) 
    
    cur.execute ('''SELECT schedule_id FROM schedule WHERE schedule_id = %s AND flight_flight_id = %s''', (payload ["schedule_id"], payload ["flight_id"]))
    schedule_exists = cur.fetchone ()
    if schedule_exists is None:
        logger.error("The flight you're trying to check with the given schedule does not exist!")
        res = {
            "status": 400,
            "errors": "The flight you're trying to check with the given schedule does not exist!",
            "results": None
        }
        return jsonify (res)
    
    statement = '''SELECT seat_seat_num FROM ticket_seat WHERE schedule_schedule_id = %s 
                EXCEPT 
                SELECT seat_seat_num FROM ticket_seat
                JOIN booking ON ticket_seat_ticket_id = ticket_seat.ticket_id
                ORDER BY seat_seat_num ASC'''
    values = (
        payload ["schedule_id"],
    )

    try:
        cur.execute (statement,values)
        fetch = cur.fetchall()
        list = []
        for i in fetch:
            list += i
        logger.info ("---- Check available seats ----")
        res = {
            "status": 200,
            "errors": None,
            "results": list
        }

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }

    finally:
        if conn is not None:
            conn.close()

    logger.debug(f'res: {res}')
    return jsonify(res)

#### 8. BOOK A FLIGHT ####
@app.route("/book_flight", methods=['GET'])
def book_flight ():
    logger.info ("---- POST / ")
    conn = db_connection ()
    cur = conn.cursor ()
    payload = request.get_json ()
    
    keys = ["flight_id","schedule_id", "seat_num"]
    if not all(key in payload for key in keys):
        logger.error("Incomplete payload!")
        res = {
            "status": 400,
            "errors": "Incomplete payload! Please ensure 'flight_id', 'schedule_id' and 'seat_num' are provided correctly!",
            "results": None
        }
        return jsonify (res)
    
    cur.execute ('''SELECT schedule_id FROM schedule WHERE schedule_id = %s AND flight_flight_id = %s''', (payload ["schedule_id"], payload ["flight_id"]))
    schedule_exists = cur.fetchone ()
    if schedule_exists is None:
        logger.error("The flight you're trying to book with the given schedule does not exist!")
        res = {
            "status": 400,
            "errors": "The flight you're trying to book with the given schedule does not exist!",
            "results": None
        }
        return jsonify (res)
    try:
        cur.execute ('''(SELECT ticket_id FROM ticket_seat WHERE schedule_schedule_id = %s AND flight_flight_id = %s AND seat_seat_num = %s)
                    EXCEPT 
                    (SELECT ticket_id FROM ticket_seat 
                    JOIN booking ON ticket_seat.ticket_id = booking.ticket_seat_ticket_id)''', (payload ["schedule_id"], payload ["flight_id"],payload ["seat_num"],))

        ticket_exists = cur.fetchone ()

        if ticket_exists is None:
            logger.error("Ticket not available!")
            res = {
                "status": 400,
                "errors": "Ticket not available!",
                "results": None
            }
            return jsonify (res)
        
        logger.info ("---- New booking ----")
        ticket_id = ticket_exists [0]
        cur.execute ('''INSERT INTO booking (ticket_seat_ticket_id)
                     VALUES (%s)''', (ticket_id,))
        conn.commit ()
        res = {
            "status": 200,
            "errors": None,
            "results": payload ["schedule_id"]
        }
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }

    finally:
        if conn is not None:
            conn.close()

    logger.debug(f'res: {res}')
    return jsonify(res)

#### 9. GENERATE A REPORT WITH TOP N DESTINATIONS ####
@app.route("/report/topDestinations/<N>", methods=['GET'])
def get_topDestinations(N):
    if int (N) <= 0:
        logger.error ("Invalid value for N!")
        res = jsonify({"status": 400, 
                       "errors": "Invalid value for N", 
                       "results": None})
        return jsonify (res)
    
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute ('''SELECT flight.airport_airport_id1 AS destiny, 
                        COUNT(flight.flight_id) AS number_flights
                        FROM flight
                        JOIN schedule ON flight.flight_id = schedule.flight_flight_id
                        WHERE schedule.date_time >= CURRENT_DATE - INTERVAL '12 months'
                        GROUP BY flight.airport_airport_id1
                        ORDER BY number_flights DESC
                        LIMIT %s''', (N,))
        
        rows = cur.fetchall()
        results = [{"destination_airport": row[0], "number_flights": row[1]} for row in rows]
        logger.info ('---- Top N destinations ----')
        res = {
            "status": 200,
            "errors": None,
            "results": results
        }

    except Exception as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }
    finally:
        cur.close()
        conn.close()

    logger.debug (f'res: {res}')    
    return jsonify (res)

#### 10. GENERATE A (MONTHLY) REPORT WITH THE TOP N ROUTES WITH MORE PASSENGERS ####
@app.route("/report/topRoutes/<N>", methods=['GET'])
def topRoutes (N):
    conn = db_connection ()
    cur = conn.cursor () 
    if int (N) <= 0:
        logger.error ("Invalid value for N!")
        res = jsonify({"status": 400, 
                       "errors": "Invalid value for N", 
                       "results": None})
        return jsonify (res)
    
    try:
        statement = '''SELECT 
                            subquery.month,
                            subquery.flight_flight_id,
                            subquery.number_of_passengers
                        FROM (
                            SELECT 
                                TO_CHAR(schedule.date_time, 'YYYY-MM') AS month, -- Extracts the month and year
                                schedule.flight_flight_id,
                                COUNT(ticket_seat.ticket_id) AS number_of_passengers,
                                RANK() OVER (
                                    PARTITION BY TO_CHAR(schedule.date_time, 'YYYY-MM') 
                                    ORDER BY COUNT(ticket_seat.ticket_id) DESC
                                ) AS rank
                            FROM 
                                schedule
                            JOIN 
                                ticket_seat ON schedule.schedule_id = ticket_seat.schedule_schedule_id
                            JOIN booking ON ticket_seat_ticket_id = ticket_id
                            WHERE 
                                schedule.date_time >= (CURRENT_DATE - INTERVAL '12 months') -- Past 12 months
                            GROUP BY 
                                TO_CHAR(schedule.date_time, 'YYYY-MM'), schedule.flight_flight_id
                        ) AS subquery
                        WHERE 
                            subquery.rank <= %s
                        ORDER BY 
                            subquery.month, subquery.rank;
                        '''
        
        cur.execute (statement, (N,))
        rows = cur.fetchall ()

        date = rows[0][0]
        results = []
        topNList = []
        dic = {"month": date}


        for row in rows:
            print(row)
            if row[0] != date:
                dic['topN'] = topNList
                results.append(dic)
                date = row[0]
                dic = {"month": date}
                topNList = []

            topNList.append({"flight_id": row[1], "total_passengers": row[2]})
        
        dic['topN'] = topNList
        results.append(dic)

        logger.info ('---- Top N destinations ----')
        res = {
            "status": 200,
            "errors": None,
            "results": results
        }
        cur.execute (statement,N)
    except Exception as error:
        logger.error(error)
        res = {
            "status": 500,
            "errors": str(error),
            "results": None
        }
    finally:
        cur.close()
        conn.close()

    logger.debug (f'res: {res}')    
    return jsonify (res)


#### ACCESS TO THE DATABASE ####
def db_connection():
    db = psycopg2.connect(user = "project",
                            password = "project",
                            host = "localhost",
                            port = "5432",
                            database = "projectSGD")
    return db



#### MAIN ####
if __name__ == "__main__":
    logging.basicConfig(filename="python/app/logs/log_file.log")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s',
                              '%H:%M:%S')
    
    ch.setFormatter(formatter)
    logger.addHandler(ch)


    time.sleep(1) 


    logger.info("\n---------------------------------------------------------------\n" + 
                  "API v1.0 online: http://localhost:8080/projeto\n\n")

    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)

