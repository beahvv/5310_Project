import psycopg2, os
import psycopg2.extras
from datetime import datetime, timedelta
from config import postgresql_host, postgresql_port, postgresql_database, postgresql_user, postgresql_password
import json


class SuperTravelStaff(object):
    def __init__(self):
        self.conn = psycopg2.connect(
                host= postgresql_host,
                port= postgresql_port,
                database= postgresql_database,
                user= postgresql_user,
                password= postgresql_password
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # return as a dict type
        self.username = None

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def reset(self):
        self.username = None

    def getUsername(self):
        return self.username

    def setUsername(self, name):
        self.username = name

    def staffLogin(self, info):
        username = info['username'][0]
        passwd = info['passwd'][0]
        sql = 'select username,passwd from Staff'
        self.cursor.execute(sql)
        for temp in self.cursor.fetchall():
            if username == temp['username'] and passwd == temp['passwd']:
                return True
            else:
                pass
        return False

    def staffAddPlane(self, info):
        sql_check = "select * from Airplane where plane_id = %s;"
        self.cursor.execute(sql_check, (info['plane_id'][0],))
        if(self.cursor.fetchone() is not None):
            return False

        sql = """insert into Airplane values(%s,%s,%s,%s,%s); """
        paras = (info['plane_id'][0], info['aircraft_age'][0],info['capacity'][0],info['airplane_type'][0],info['description'][0])
        self.cursor.execute(sql, paras)
        self.conn.commit()
        return True

    def staffAddPort(self, info):
        sql_check = "select * from Airport where airport_name = %s;"
        self.cursor.execute(sql_check, (info['port_name'][0],))
        if(self.cursor.fetchone() is not None):
            return False

        sql = """insert into Airport values(%s,%s,%s,%s,%s); """
        paras = (info['port_name'][0].upper(), info['city'][0],info['state'][0],info['country'][0],info['zip_code'][0])
        self.cursor.execute(sql, paras)
        self.conn.commit()
        return True
    
    def staffAddAirline(self, info):
        sql_check = "select * from Airline where airline_name = %s;"
        self.cursor.execute(sql_check, (info['airline_name'][0],))
        if(self.cursor.fetchone() is not None):
            return False

        sql = """insert into Airline values(%s,%s,%s,%s); """
        paras = (info['airline_name'][0], info['headquarter_city'][0],info['headquarter_state'][0],info['headquarter_country'][0])
        self.cursor.execute(sql, paras)
        self.conn.commit()
        return True

    def staffChangeStatus(self, info):
        flightNumber = info['flight_num'][0]
        flightDate = datetime.strptime(info['depart_date'][0], "%Y-%m-%d")
        flightTime = datetime.strptime(info['depart_time'][0], "%H:%M")
        stamp = datetime(flightDate.year, flightDate.month,
                         flightDate.day, flightTime.hour, flightTime.minute)
        sql = """
            SELECT O.plane_id
            FROM Flight as F,Operate as O
            WHERE F.flight_num = O.flight_num AND
            F.flight_num = %s AND F.depart_time = %s"""
        self.cursor.execute(sql, (flightNumber, stamp))
        temp = self.cursor.fetchone()
        if temp is None:
            return (False, "Plane Not Found")
        else:
            sql = """UPDATE Flight SET flight_status = %s WHERE flight_num = %s AND depart_time = %s;"""
            paras = (info['status'][0], flightNumber, stamp)
            self.cursor.execute(sql, paras)
            self.conn.commit()
            return (True, "Flight Status Updated")



    def staffAddFlight(self, info):
        sql_check_airline = """select * from Airline where airline_name = %s"""
        self.cursor.execute(sql_check_airline, (info['airline_name'][0],))
        if self.cursor.fetchone() is None:
            # plane haven't created
            return (False, "Airline Doesn't Exist")
        else:
            pass
        
        sql_check_airplane = """select * from Airplane where plane_id = %s"""
        self.cursor.execute(sql_check_airplane, (info['plane_id'][0],))
        if self.cursor.fetchone() is None:
            # plane haven't created
            return (False, "Airline Doesn't Exist")
        else:
            pass

        sql_check_plane_availability = """select F.depart_time, F.arrival_time
            FROM Operate as O,Flight as F
            WHERE O.plane_id = %s AND O.flight_num = F.flight_num
            AND O.depart_time=F.depart_time;"""
        self.cursor.execute(sql_check_plane_availability, (info['plane_id'][0],))
        departDate = datetime.strptime(info['depart_date'][0], "%Y-%m-%d")
        departTime = datetime.strptime(info['depart_time'][0], "%H:%M")
        departStamp = datetime(departDate.year, departDate.month,
                               departDate.day, departTime.hour, departTime.minute)
        arrivalDate = datetime.strptime(info['arrival_date'][0], "%Y-%m-%d")
        arrivalTime = datetime.strptime(info['arrival_time'][0], "%H:%M")
        arrivalStamp = datetime(arrivalDate.year, arrivalDate.month,
                                arrivalDate.day, arrivalTime.hour, arrivalTime.minute)
        for temp in self.cursor.fetchall():
            if (temp['depart_time'] > departStamp and temp['depart_time'] < arrivalStamp) \
                    or (temp['arrival_time'] > departStamp and temp['arrival_time'] < arrivalStamp):
                # when the plane has time comflicts with the new flight
                return (False, "Time Conflict for This Plane")
            else:
                pass

        if departStamp > arrivalStamp:
            return (False, "Arrival Time in Ahead of Depart Time")
        else:
            pass

        sql_check_airport = """select airport_name from Airport;"""
        self.cursor.execute(sql_check_airport)
        database_ports = [temp['airport_name']
                          for temp in self.cursor.fetchall()]
        # when airports of FROM and TO doesn't exist
        if info['depart_port'][0].upper() not in database_ports:
            return (False, "Departure Airport Doesn't Exist")
        elif info['arrival_port'][0].upper() not in database_ports:
            return (False, "Destination Airport Doesn't Exist")
        else:
            pass

        sql_insert_flight = """insert into Flight values(%s,%s,%s,%s,%s,%s,%s,%s);"""
        flight_paras = (info['flight_num'][0], departStamp, info['depart_port'][0].upper(),
                        arrivalStamp, info['arrival_port'][0].upper(), info['airline_name'][0],info['base_price'][0],info['flight_status'][0])
        self.cursor.execute(sql_insert_flight, flight_paras)
        self.conn.commit()

        sql_insert_operate = """insert into Operate values(%s,%s,%s);"""
        self.cursor.execute(
            sql_insert_operate, (info['flight_num'][0], departStamp, info['plane_id'][0]))
        self.conn.commit()
        return (True, "New Flight Added")

    def staffViewFlightReport(self, info):
        start = datetime.now() - timedelta(days=180)
        end = datetime.now()
        if 'start_date' in info.keys() and info['start_date'][0] != "":
            start = datetime.strptime(info['start_date'][0], "%Y-%m-%d")
        if 'end_date' in info.keys() and info['end_date'][0] != "":
            end = datetime.strptime(info['end_date'][0], "%Y-%m-%d")
        
        sql = """ SELECT airline_name,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, airline_name,number
		                FROM 
	 		                (SELECT F.airline_name, COUNT(T.ticket_id) AS number
			                FROM Ticket as T, TicketFlight as TF, Flight as F
                            WHERE T.ticket_id = TF.ticket_id AND TF.flight_num = F.flight_num
                            AND T.purchase_date > %s AND T.purchase_date < %s
			                GROUP BY F.airline_name) AS airline) AS airline_rank
                    WHERE ranking <= 5;
                """  
        self.cursor.execute(sql, (start, end))
        
        ret_total = {"airline_name":[],"number":[]}
        for temp in self.cursor.fetchall():
            ret_total['airline_name'].append(temp['airline_name'])
            ret_total['number'].append(temp['number'])
        
        sql_top_destination = """ SELECT city,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, city,number
		                FROM 
	 		                (SELECT A.city, COUNT(T.ticket_id) AS number
			                FROM Ticket as T, TicketFlight as TF, Flight as F, Airport as A
                            WHERE TF.flight_num = F.flight_num AND TF.depart_time = F.depart_time
                            AND F.arrival_airport = A.airport_name AND T.ticket_id = TF.ticket_id
                            AND T.purchase_date > %s AND T.purchase_date < %s
			                GROUP BY A.city) AS destination) AS destination_rank
                    WHERE ranking <= 10;
                """  
        self.cursor.execute(sql_top_destination, (start, end))
        
        ret_destination = {"city":[],"number":[]}
        for temp in self.cursor.fetchall():
            ret_destination['city'].append(temp['city'])
            ret_destination['number'].append(temp['number'])
        
        sql_rating_airline =  """ SELECT airline_name,rate
                    FROM (SELECT rank() OVER (ORDER BY(rate) DESC) AS ranking, airline_name,rate
		                FROM 
	 		                (SELECT F.airline_name, CAST(AVG(R.rating) AS DECIMAL(10,2)) as rate
                            FROM Airplane as AP, Operate as O, rate_flight as R, Flight as F
                            WHERE O.plane_id = AP.plane_id 
                            AND O.flight_num = R.flight_num AND O.depart_time = R.depart_time
                            AND O.flight_num = F.flight_num
                            AND R.date > %s AND R.date < %s
			                GROUP BY F.airline_name) AS airline_name) AS rating_rank
                    WHERE ranking <= 5;
                """
        self.cursor.execute(sql_rating_airline, (start, end))
        
        ret_rating_airline = {"airline_name":[],"rate":[]}
        for temp in self.cursor.fetchall():
            ret_rating_airline['airline_name'].append(temp['airline_name'])
            ret_rating_airline['rate'].append(temp['rate'])      
        
        return (ret_total, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"),ret_destination,ret_rating_airline)

    def staffViewRentalReport(self,info):
        start = datetime.now() - timedelta(days=180)
        end = datetime.now()
        if 'start_date' in info.keys() and info['start_date'][0] != "":
            start = datetime.strptime(info['start_date'][0], "%Y-%m-%d")
        if 'end_date' in info.keys() and info['end_date'][0] != "":
            end = datetime.strptime(info['end_date'][0], "%Y-%m-%d")

        sql_company = """ SELECT name,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, name, number
		                FROM 
	 		                (SELECT RC.name, COUNT(*) AS number
			                FROM Rent as R, Car as C, rental_company as RC
                            WHERE R.car_id = C.car_id AND C.company_id = RC.company_id
                            AND R.purchase_date > %s AND R.purchase_date < %s
			                GROUP BY RC.name) AS name) AS company_rank
                    WHERE ranking <= 3;
                """  
        self.cursor.execute(sql_company, (start, end))

        company_total = {"name":[],"number":[]}
        for temp in self.cursor.fetchall():
            company_total['name'].append(temp['name'])
            company_total['number'].append(temp['number'])
        
        sql_brand = """ SELECT brand,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, brand, number
		                FROM 
	 		                (SELECT C.brand, COUNT(*) AS number
			                FROM Rent as R, Car as C
                            WHERE R.car_id = C.car_id
                            AND R.purchase_date > %s AND R.purchase_date < %s
			                GROUP BY C.brand) AS brand) AS brand_rank
                    WHERE ranking <= 5;
                """          
        self.cursor.execute(sql_brand, (start, end))

        brand_total = {"brand":[],"number":[]}
        for temp in self.cursor.fetchall():
            brand_total['brand'].append(temp['brand'])
            brand_total['number'].append(temp['number'])

        sql_type = """ SELECT type,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, type, number
		                FROM 
	 		                (SELECT C.type, COUNT(*) AS number
			                FROM Rent as R, Car as C
                            WHERE R.car_id = C.car_id
                            AND R.purchase_date > %s AND R.purchase_date < %s
			                GROUP BY C.type) AS type) AS type_rank
                    WHERE ranking <= 5;
                """          
        self.cursor.execute(sql_type, (start, end))

        type_total = {"type":[],"number":[]}
        for temp in self.cursor.fetchall():
            type_total['type'].append(temp['type'])
            type_total['number'].append(temp['number'])

        sql_rating_company =  """ SELECT name,rate
                    FROM (SELECT rank() OVER (ORDER BY(rate) DESC) AS ranking, name,rate
		                FROM 
	 		                (SELECT R.name, CAST(AVG(RC.rating) AS DECIMAL(10,2)) as rate
                            FROM rate_company as RC, rental_company as R
                            WHERE RC.company_id = R.company_id
                            AND RC.date > %s AND RC.date < %s
			                GROUP BY R.name) AS name) AS company_rating_rank
                    WHERE ranking <= 3;
                """
        self.cursor.execute(sql_rating_company, (start, end))
        
        ret_rating_company = {"name":[],"rate":[]}
        for temp in self.cursor.fetchall():
            ret_rating_company['name'].append(temp['name'])
            ret_rating_company['rate'].append(temp['rate'])   


        return (company_total, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"),brand_total,type_total,ret_rating_company)
    
    def staffViewHotelReport(self,info):
        start = datetime.now() - timedelta(days=180)
        end = datetime.now()
        if 'start_date' in info.keys() and info['start_date'][0] != "":
            start = datetime.strptime(info['start_date'][0], "%Y-%m-%d")
        if 'end_date' in info.keys() and info['end_date'][0] != "":
            end = datetime.strptime(info['end_date'][0], "%Y-%m-%d")

        sql_hotel = """ SELECT name,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, name, number
		                FROM 
	 		                (SELECT H.name, COUNT(*) AS number
			                FROM Reserve as R, Room as Ro, Hotel as H
                            WHERE R.room_id = Ro.room_id AND Ro.hotel_id = H.hotel_id
                            AND R.purchase_date > %s AND R.purchase_date < %s
			                GROUP BY H.name) AS name) AS hotel_rank
                    WHERE ranking <= 5;
                """  
        self.cursor.execute(sql_hotel, (start, end))

        hotel_total = {"name":[],"number":[]}
        for temp in self.cursor.fetchall():
            hotel_total['name'].append(temp['name'])
            hotel_total['number'].append(temp['number'])

        sql_city = """ SELECT city,state,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, city, state,number
		                FROM 
	 		                (SELECT H.city, H.state,COUNT(*) AS number
			                FROM Reserve as R, Room as Ro, Hotel as H
                            WHERE R.room_id = Ro.room_id AND Ro.hotel_id = H.hotel_id
                            AND R.purchase_date > %s AND R.purchase_date < %s
			                GROUP BY H.city,H.state) AS city) AS city_rank
                    WHERE ranking <= 5;
                """  
        self.cursor.execute(sql_city, (start, end))

        city_total = {"city":[],"number":[]}
        for temp in self.cursor.fetchall():
            city_total['city'].append(str(temp['city']) + "-" + str(temp['state']))
            city_total['number'].append(temp['number'])

        sql_room_type = """ SELECT type,number
                    FROM (SELECT rank() OVER (ORDER BY(number) DESC) AS ranking, type,number
		                FROM 
	 		                (SELECT Ro.type,COUNT(*) AS number
			                FROM Reserve as R, Room as Ro, Hotel as H
                            WHERE R.room_id = Ro.room_id AND Ro.hotel_id = H.hotel_id
                            AND R.purchase_date > %s AND R.purchase_date < %s
			                GROUP BY Ro.type) AS type) AS type_rank
                    WHERE ranking <= 5;
                """  
        self.cursor.execute(sql_room_type, (start, end))

        type_total = {"type":[],"number":[]}
        for temp in self.cursor.fetchall():
            type_total['type'].append(str(temp['type']))
            type_total['number'].append(temp['number'])

        sql_rating_hotel =  """ SELECT name,rate
                    FROM (SELECT rank() OVER (ORDER BY(rate) DESC) AS ranking, name, rate
		                FROM 
	 		                (SELECT H.name, CAST(AVG(R.rating) AS DECIMAL(10,2)) as rate
                            FROM rate_hotel as R, hotel as H
                            WHERE R.hotel_id = H.hotel_id
                            AND R.date > %s AND R.date < %s
			                GROUP BY H.name) AS name) AS hotel_rating_rank
                    WHERE ranking <= 5;
                """
        self.cursor.execute(sql_rating_hotel, (start, end))

        ret_rating_hotel = {"name":[],"rate":[]}
        for temp in self.cursor.fetchall():
            ret_rating_hotel['name'].append(temp['name'])
            ret_rating_hotel['rate'].append(temp['rate'])

        return (hotel_total, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"),city_total,type_total,ret_rating_hotel)
