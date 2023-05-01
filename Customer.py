import psycopg2, os
import psycopg2.extras
from datetime import datetime, timedelta
from config import postgresql_host, postgresql_port, postgresql_database, postgresql_user, postgresql_password
import json


class Customer(object):

    def __init__(self):
        self.conn = psycopg2.connect(
                host= postgresql_host,
                port= postgresql_port,
                database= postgresql_database,
                user= postgresql_user,
                password= postgresql_password
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) # return as a dict type
        self.email = None
        self.ticket_id = None

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.email = None
        self.ticket_id = None


    def setEmail(self, email):
        self.email = email

    def getEmail(self):
        return self.email

    def reset(self):
        self.email = None

    def find_set_ticket_ID(self):
        # find the largest ticket id in table.,
        # saved for generating the next ticket
        query = """SELECT max(ticket_id) as ID FROM Ticket;"""
        self.cursor.execute(query)
        rec = self.cursor.fetchone()
        rec = json.dumps(rec)
        rec = json.loads(rec)
        val = rec['id']
        self.ticket_id = val

    # When a user logs in, a session should be initiated

    def custLogin(self, info):
        username = info['username'][0]
        passwd = info['passwd'][0]
        query = 'select cust_email, passwd as passwd from Customer'
        self.cursor.execute(query)

        for temp in self.cursor.fetchall():
            if username == temp['cust_email'] and passwd == temp['passwd']:
                return True

        return False

    # Customer sign up
    def cust_Signup(self, info):
        email = info['email'][0]
        first_name = info['first_name'][0]
        last_name = info['last_name'][0]
        password = info['password'][0]
        street = info['street'][0]
        city = info['city'][0]
        state = info['state'][0]
        country = info['country'][0]
        zip_code = info['zip_code'][0]
        phone = info['phone'][0]
        passport_number = info['passport_number'][0]
        passport_expiration = info['passport_expiration'][0]
        passport_country = info['passport_country'][0]
        dob = info['dob'][0]
        # Check if a customer use same email to sign up twice
        query1 = 'SELECT cust_email FROM Customer'
        self.cursor.execute(query1)

        for temp in self.cursor.fetchall():
            print(temp)
            if temp['cust_email'] == email:
                print(
                    "This email has already been registered. Please enter another email.")
                return False
            
        query2 = """INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        paras = (email, first_name, last_name, password, street, city, state,
                 country, zip_code, phone, passport_number, passport_expiration, passport_country,dob)
        self.cursor.execute(query2, paras)
        self.conn.commit()
        return True

    # Customer Ticket Search
    def customer_ticket_search(self, info):
        depart_airport = info['depart_port'][0]
        arrival_airport = info['arrival_port'][0]
        depart_date = datetime.strptime(info['depart_date'][0], "%Y-%m-%d")
        
        query = """
            SELECT AP.capacity, F.airline_name,F.flight_num,F.depart_time,F.arrival_time,F.base_price
            FROM Airplane as AP, Operate as O, Flight as F
            WHERE O.flight_num = F.flight_num 
              AND O.depart_time = F.depart_time
              AND O.plane_id = AP.plane_id
              AND F.depart_airport = %s AND F.arrival_airport = %s"""

        query_ticket_count = """SELECT COUNT(ticket_id) as num_ticket FROM TicketFlight
            WHERE flight_num = %s AND depart_time = %s"""

        if info['trip_type'][0] == "Single Trip":
            ret = []
            self.cursor.execute(query, (depart_airport, arrival_airport))
            flights = self.cursor.fetchall()
            for temp in flights:
                self.cursor.execute(
                    query_ticket_count, (temp['flight_num'], temp['depart_time']))
                ticket_count = self.cursor.fetchone()
                ticket_count = json.dumps(ticket_count)
                ticket_count = json.loads(ticket_count)
                val = ticket_count['num_ticket']
                ticket_count = val
                if temp['depart_time'] >= depart_date:
                    if ticket_count == temp['capacity']:
                        pass
                    else:
                        ret.append(temp)
                else:
                    pass
            return ret
        elif info['trip_type'][0] == "Round Trip":
            return_date = datetime.strptime(info['return_date'][0], "%Y-%m-%d")
            ret1 = []
            ret2 = []
            self.cursor.execute(query, (depart_airport, arrival_airport))
            flights = self.cursor.fetchall()
            for temp in flights:
                self.cursor.execute(
                    query_ticket_count, (temp['flight_num'], temp['depart_time']))
                ticket_count = self.cursor.fetchone()
                ticket_count = json.dumps(ticket_count)
                ticket_count = json.loads(ticket_count)
                val = ticket_count['num_ticket']
                ticket_count = val
                if temp['depart_time'] >= depart_date:
                    if ticket_count == temp['capacity']:
                        pass
                    else:
                        ret1.append(temp)
                else:
                    pass
            self.cursor.execute(query, (arrival_airport, depart_airport))
            flights = self.cursor.fetchall()
            for temp in flights:
                self.cursor.execute(
                    query_ticket_count, (temp['flight_num'], temp['depart_time']))
                ticket_count = self.cursor.fetchone()
                ticket_count = json.dumps(ticket_count)
                ticket_count = json.loads(ticket_count)
                val = ticket_count['num_ticket']
                ticket_count = val
                if temp['depart_time'] >= return_date:
                    if ticket_count == temp['capacity']:
                        pass
                    else:
                        ret2.append(temp)
                else:
                    pass
            return (ret1, ret2)
        
    # Customer Car Search
    def customer_car_search(self,info):
        ret = []
        rent_date = datetime.strptime(info['rent_date'][0], "%Y-%m-%d")
        city = info['city'][0]
        state = info['state'][0]
        country = info['country'][0]

        query = """ SELECT R.name, CA.car_id, CA.brand, CA.type, CA.color, CA.base_price, RT.rent_date, RT.return_date
        FROM Rent as RT, Car as CA, rental_company as R
        WHERE RT.car_id = CA.car_id AND CA.company_id = R.company_id
        AND R.city = %s AND R.state = %s AND R.country = %s"""
        self.cursor.execute(query, (city, state,country))
        cars = self.cursor.fetchall()
        for temp in cars:
            if rent_date > temp['return_date']:
                ret.append(temp)
            else:
                pass
        
        # Append unused car to the list
        query2 = """  WITH check_rental as (SELECT car.car_id, car.company_id, car.brand, car.type, car.color, car.base_price
        FROM rent FULL outer join car ON rent.car_id = car.car_id
		WHERE rent.car_id IS NULL)
        SELECT R.name, CA.car_id, CA.brand, CA.type, CA.color, CA.base_price
        FROM check_rental as CA, rental_company as R
        WHERE CA.company_id = R.company_id AND R.city = %s AND R.state = %s AND R.country = %s"""
        self.cursor.execute(query2, (city, state,country))
        cars_unused = self.cursor.fetchall()
        for temp in cars_unused:
            ret.append(temp)
        print(ret)
        return ret
    
    # Customer Hotel Search
    def customer_hotel_search(self,info):
        ret = []
        check_in_date = datetime.strptime(info['check_in_date'][0], "%Y-%m-%d")
        city = info['city'][0]
        state = info['state'][0]
        country = info['country'][0]

        query = """ SELECT H.name, H.stars, R.room_id, R.price, Re.check_in_date, Re.check_out_date
        FROM Reserve as Re, Room as R, Hotel as H
        WHERE R.room_id = Re.room_id AND R.hotel_id = H.hotel_id
        AND H.city = %s AND H.state = %s AND H.country = %s"""
        self.cursor.execute(query, (city, state,country))
        hotels = self.cursor.fetchall()
        for temp in hotels:
            if check_in_date > temp['check_out_date']:
                ret.append(temp)
            else:
                pass

        # Append unused room to the list
        query2 = """  WITH check_room as (SELECT room.room_id,room.hotel_id,room.price
        FROM reserve  FULL outer join room ON reserve.room_id = room.room_id
		WHERE reserve.room_id IS NULL)
        SELECT H.name, H.stars, CR.room_id, CR.price
        FROM check_room as CR, hotel as H
        WHERE CR.hotel_id = H.hotel_id AND H.city = %s AND H.state = %s AND H.country = %s"""
        self.cursor.execute(query2, (city, state,country))
        cars_unused = self.cursor.fetchall()
        for temp in cars_unused:
            ret.append(temp)
        return ret


    # Customer Flight Status Search
    def customer_flight_status_search(self, info):
        flightNumber = info['flight_num'][0]
        flightDepartDate = datetime.strptime(info['depart_date'][0], "%Y-%m-%d")
        flightDepartTime = datetime.strptime(info['depart_time'][0], "%H:%M")
        stamp = datetime(flightDepartDate.year, flightDepartDate.month,
                         flightDepartDate.day, flightDepartTime.hour, flightDepartTime.minute)
        query = """SELECT * FROM Flight where flight_num = %s and depart_time = %s;"""
        self.cursor.execute(query, (flightNumber, stamp))
        temp = self.cursor.fetchone()
        if temp == None:
            return "No Matched Results"
        else:
            return temp['flight_status']

    # Customer view Past Flights
    def customer_past_flights(self):
        stamp = datetime.now()

        query = """
        SELECT F.depart_time, F.arrival_time,F.airline_name,TF.flight_num, F.depart_airport,F.arrival_airport
        FROM Flight as F,TicketFlight as TF, Ticket as T 
        WHERE T.ticket_id = TF.ticket_id AND TF.flight_num = F.flight_num 
        AND TF.depart_time = F.depart_time AND T.cust_email = %s and F.arrival_time < %s;"""      

        self.cursor.execute(query, (self.email, stamp))
        ret = []
        for temp in self.cursor.fetchall():
            if temp['depart_time'] < stamp:
                ret.append(temp)
        return ret


    # Customer view Past Bookings
    def customer_past_bookings(self):
        stamp = datetime.now()

        query = """
        SELECT H.name, R.number, Re.check_in_date, Re.check_out_date,H.city,H.state
        FROM Reserve as Re, Room as R, Hotel as H
        WHERE Re.room_id = R.room_id AND R.hotel_id = H.hotel_id 
        AND Re.guest_email = %s AND Re.check_out_date < %s;"""     

        self.cursor.execute(query, (self.email, stamp))
        ret = []
        for temp in self.cursor.fetchall():
            if temp['check_in_date'] < stamp:
                ret.append(temp)
        return ret
    
    # Customer view Past Rentals
    def customer_past_rentals(self):
        stamp = datetime.now()

        query = """
        SELECT C.name, CA.brand, RT.rent_date, RT.return_date,C.city,C.state
        FROM Rent as RT, Car as CA, rental_company as C
        WHERE RT.car_id = CA.car_id AND CA.company_id = C.company_id 
        AND RT.cust_email = %s AND RT.return_date < %s;"""     

        self.cursor.execute(query, (self.email, stamp))
        ret = []
        for temp in self.cursor.fetchall():
            if temp['rent_date'] < stamp:
                ret.append(temp)
        return ret
        
    # Customer view Future Flights
    def customer_future_flights(self):
        stamp = datetime.now()

        query = """
        SELECT F.depart_time, F.arrival_time,F.airline_name,TF.flight_num, F.depart_airport, F.arrival_airport
        FROM Flight as F,TicketFlight as TF, Ticket as T 
        WHERE T.ticket_id = TF.ticket_id AND TF.flight_num = F.flight_num 
        AND TF.depart_time = F.depart_time AND T.cust_email = %s and F.depart_time > %s;"""

        self.cursor.execute(query, (self.email, stamp))
        return self.cursor.fetchall()

    # Customer view Future Bookings
    def customer_future_bookings(self):
        stamp = datetime.now()

        query = """
        SELECT H.name, R.number, Re.check_in_date, Re.check_out_date, H.city,H.state
        FROM Reserve as Re, Room as R, Hotel as H
        WHERE Re.room_id = R.room_id AND R.hotel_id = H.hotel_id 
        AND Re.guest_email = %s AND Re.check_in_date > %s;"""     

        self.cursor.execute(query, (self.email, stamp))
        return self.cursor.fetchall()
    
    # Customer view Future Rentals
    def customer_future_rentals(self):
        stamp = datetime.now()

        query = """
        SELECT C.name, CA.brand, RT.rent_date, RT.return_date, C.city, C.state
        FROM Rent as RT, Car as CA, rental_company as C
        WHERE RT.car_id = CA.car_id AND CA.company_id = C.company_id 
        AND RT.cust_email = %s AND RT.rent_date > %s;"""     

        self.cursor.execute(query, (self.email, stamp))
        return self.cursor.fetchall()
        
    # Customer purchase ticket
    def customer_purchase(self, info):
        # create a new Ticket
        ticket_id = self.ticket_id + 1
        purchase_date = datetime.now().replace(microsecond=0)
        card_expiration = datetime.strptime(info['card_expiration'][0], "%m/%Y")

        query2 = """insert into Ticket values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        values = (ticket_id, info['cust_email'][0], purchase_date,
                  info['seat_num'][0], info['price'][0],info['card_number'][0],
                  info['card_holder'][0], info['card_type'][0], card_expiration, info['CVV_code'][0])
        self.cursor.execute(query2, values)
        self.conn.commit()

        # Update TicketFlight Table
        sql = """insert into TicketFlight values(%s,%s,%s);"""
        depart_time = datetime.strptime(
            info['depart_date'][0], "%Y %b %d %H:%M")
        self.cursor.execute(
            sql, (ticket_id, info['flight_num'][0], depart_time))
        self.conn.commit()

        self.ticket_id += 1
        return True

    # Customer purchase rental
    def customer_purchaseRental(self, info):

        purchase_date = datetime.now().replace(microsecond=0)
        card_expiration = datetime.strptime(info['card_expiration'][0], "%m/%Y")

        query2 = """insert into Rent values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        values = (info['cust_email'][0], info['car_id'][0], info['rent_date'][0],
                  info['return_date'][0],purchase_date,info['base_price'][0],info['card_number'][0],
                  info['card_holder'][0], info['card_type'][0], card_expiration, info['CVV_code'][0])
        self.cursor.execute(query2, values)
        self.conn.commit()

        # Update rate_company table
        return True
    
    # Customer purchase Booking
    def customer_purchaseBooking(self, info):
        # create a new booking_id
        booking_id = self.booking_id + 1
        purchase_date = datetime.now().replace(microsecond=0)
        card_expiration = datetime.strptime(info['card_expiration'][0], "%m/%Y")

        query2 = """insert into Reserve values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        values = (info['cust_email'][0], info['room_id'][0], info['check_in_date'][0],
                  booking_id, info['check_out_date'][0],purchase_date,info['rate_per_night'][0],info['card_number'][0],
                  info['card_holder'][0], info['card_type'][0], card_expiration, info['CVV_code'][0])
        self.cursor.execute(query2, values)
        self.conn.commit()
        
        self.booking_id += 1
        return True
    
    # Track Flight Spending
    def track_my_spending_flights(self, info):
        start = datetime.now() - timedelta(days=180)
        end = datetime.now()
        if 'start_date' in info.keys() and info['start_date'][0] != "":
            start = datetime.strptime(info['start_date'][0], "%Y-%m-%d")
        if 'end_date' in info.keys() and info['end_date'][0] != "":
            end = datetime.strptime(info['end_date'][0], "%Y-%m-%d")

        query_total = """SELECT sum(price) as spending 
                    FROM Ticket WHERE cust_email =%s AND purchase_date >%s AND purchase_date <%s 
                    GROUP BY cust_email"""
        self.cursor.execute(query_total, (self.email, start, end))
        ret_total = self.cursor.fetchone()
        ret_total = json.dumps(ret_total)
        ret_total = json.loads(ret_total)
        ret_total = ret_total['spending']

        query_by_month = """Select sum(price) as monthly_spending, EXTRACT(YEAR FROM purchase_date) as year ,
                        EXTRACT(MONTH FROM purchase_date) as month
                        FROM Ticket
                        WHERE cust_email = %s AND purchase_date >%s AND purchase_date < %s
                        GROUP BY year,month;"""
        self.cursor.execute(query_by_month, (self.email, start, end))
        ret_month = {"month": [], "monthly_spending": []}
        for temp in self.cursor.fetchall():
            ret_month['month'].append(
                str(temp['year']) + "-" + str(temp['month']))
            ret_month['monthly_spending'].append(temp['monthly_spending'])

        return (ret_total, ret_month, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
    
   # Track Hotel Spending
    def track_my_spending_hotels(self, info):
        start = datetime.now() - timedelta(days=180)
        end = datetime.now()
        if 'start_date' in info.keys() and info['start_date'][0] != "":
            start = datetime.strptime(info['start_date'][0], "%Y-%m-%d")
        if 'end_date' in info.keys() and info['end_date'][0] != "":
            end = datetime.strptime(info['end_date'][0], "%Y-%m-%d")

        query_total = """SELECT sum(rate_per_night * EXTRACT(DAY FROM (check_out_date)- (check_in_date))) as spending 
                    FROM Reserve WHERE guest_email =%s AND purchase_date >%s AND purchase_date <%s 
                    GROUP BY guest_email"""
        self.cursor.execute(query_total, (self.email, start, end))
        ret_total = self.cursor.fetchone()
        ret_total = json.dumps(ret_total)
        ret_total = json.loads(ret_total)
        ret_total = ret_total['spending']

        query_by_month = """Select sum(rate_per_night * EXTRACT(DAY FROM (check_out_date)- (check_in_date))) as monthly_spending, EXTRACT(YEAR FROM purchase_date) as year ,
                        EXTRACT(MONTH FROM purchase_date) as month
                        FROM Reserve
                        WHERE guest_email = %s AND purchase_date >%s AND purchase_date < %s
                        GROUP BY year,month;"""
        self.cursor.execute(query_by_month, (self.email, start, end))
        ret_month = {"month": [], "monthly_spending": []}
        for temp in self.cursor.fetchall():
            ret_month['month'].append(
                str(temp['year']) + "-" + str(temp['month']))
            ret_month['monthly_spending'].append(temp['monthly_spending'])

        return (ret_total, ret_month, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))


   # Track Rental Spending
    def track_my_spending_rentals(self, info):
        start = datetime.now() - timedelta(days=180)
        end = datetime.now()
        if 'start_date' in info.keys() and info['start_date'][0] != "":
            start = datetime.strptime(info['start_date'][0], "%Y-%m-%d")
        if 'end_date' in info.keys() and info['end_date'][0] != "":
            end = datetime.strptime(info['end_date'][0], "%Y-%m-%d")

        query_total = """SELECT sum(rate_per_day * EXTRACT(DAY FROM (return_date)- (rent_date))) as spending 
                    FROM rent WHERE cust_email =%s AND purchase_date >%s AND purchase_date <%s 
                    GROUP BY cust_email"""
        self.cursor.execute(query_total, (self.email, start, end))
        ret_total = self.cursor.fetchone()
        ret_total = json.dumps(ret_total)
        ret_total = json.loads(ret_total)
        ret_total = ret_total['spending']

        query_by_month = """Select sum(rate_per_day * EXTRACT(DAY FROM (return_date)- (rent_date))) as monthly_spending, EXTRACT(YEAR FROM purchase_date) as year ,
                        EXTRACT(MONTH FROM purchase_date) as month
                        FROM rent
                        WHERE cust_email = %s AND purchase_date >%s AND purchase_date < %s
                        GROUP BY year,month;"""
        self.cursor.execute(query_by_month, (self.email, start, end))
        ret_month = {"month": [], "monthly_spending": []}
        for temp in self.cursor.fetchall():
            ret_month['month'].append(
                str(temp['year']) + "-" + str(temp['month']))
            ret_month['monthly_spending'].append(temp['monthly_spending'])

        return (ret_total, ret_month, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

    def register_rating(self, info):
        depart_time = datetime.strptime(
            info['depart_date'][0], "%Y %b %d %H:%M")
        sql_check = """SELECT depart_time FROM rate_flight WHERE cust_email = %s;"""
        paras = (self.email,)
        self.cursor.execute(sql_check, paras)
        for temp in self.cursor.fetchall():
            if temp['depart_time'] == depart_time:
                return False
            else:
                pass
        stamp = datetime.now().replace(microsecond=0)
        sql = """INSERT INTO rate_flight VALUES(%s,%s,%s,%s,%s,%s)"""
        paras = (self.email, info['flight_num'][0], depart_time,
                 stamp,info['rating'][0], info['comments'][0])
        self.cursor.execute(sql, paras)
        self.conn.commit()
        return True
    

    def register_ratingH(self, info):

        sql_check = """SELECT rating,comments FROM rate_hotel WHERE cust_email = %s;"""
        paras = (self.email,)
        self.cursor.execute(sql_check, paras)
        for temp in self.cursor.fetchall():
            if temp['rating'] is not None:
                return False
            else:
                pass
        stamp = datetime.now().replace(microsecond=0)
        sql = """INSERT INTO rate_hotel VALUES(%s,%s,%s,%s,%s)"""
        paras = (self.email, info['hotel_id'][0],
                 stamp,info['rating'][0], info['comments'][0])
        self.cursor.execute(sql, paras)
        self.conn.commit()
        return True

    def register_ratingC(self, info):

        sql_check = """SELECT rating,comments FROM rate_company WHERE cust_email = %s;"""
        paras = (self.email,)
        self.cursor.execute(sql_check, paras)
        for temp in self.cursor.fetchall():
            if temp['rating'] is not None:
                return False
            else:
                pass
        stamp = datetime.now().replace(microsecond=0)
        sql = """INSERT INTO rate_company VALUES(%s,%s,%s,%s,%s,%s)"""
        paras = (self.email, info['company_id'][0],
                 stamp,info['rating'][0], info['comments'][0])
        self.cursor.execute(sql, paras)
        self.conn.commit()
        return True

