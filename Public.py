import psycopg2, os
import psycopg2.extras
from datetime import datetime, timedelta
from config import postgresql_host, postgresql_port, postgresql_database, postgresql_user, postgresql_password
import random

class Public(object):
    def __init__(self):
        self.conn = psycopg2.connect(
                host= postgresql_host,
                port= postgresql_port,
                database= postgresql_database,
                user= postgresql_user,
                password= postgresql_password
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # return as a dict type

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def publicTicketSearch(self, info):
        depart_airport = info['depart_port'][0]
        arrival_airport = info['arrival_port'][0]
        depart_date = datetime.strptime(info['depart_date'][0], "%Y-%m-%d")

        sql = """
            SELECT F.airline_name,F.flight_num,F.depart_time,F.arrival_time,F.base_price
            FROM Airplane as AP, Operate as O, Flight as F
            WHERE O.flight_num = F.flight_num AND O.depart_time = F.depart_time
            AND O.plane_id = AP.plane_id AND F.depart_airport = %s AND F.arrival_airport = %s"""
        
        if info['trip_type'][0] == "Single Trip":
            ret = []
            self.cursor.execute(sql, (depart_airport, arrival_airport))
            for temp in self.cursor.fetchall():
                if temp['depart_time'] >= depart_date:
                    ret.append(temp)
                else:
                    return False
            return ret
        elif info['trip_type'][0] == "Round Trip":
            return_date = datetime.strptime(info['return_date'][0], "%Y-%m-%d")
            ret1 = []
            ret2 = []
            self.cursor.execute(sql, (depart_airport, arrival_airport))
            for temp in self.cursor.fetchall():
                if temp['depart_time'] >= depart_date:
                    ret1.append(temp)
                else:
                    pass
            self.cursor.execute(sql, (arrival_airport, depart_airport))
            for temp in self.cursor.fetchall():
                if temp['depart_time'] >= return_date:
                    ret2.append(temp)
                else:
                    pass
            return (ret1, ret2)

    def check_flight_status(self, info):
        flightNumber = info['flight_num'][0]
        flightDate = datetime.strptime(info['depart_date'][0], "%Y-%m-%d")
        flightTime = datetime.strptime(info['depart_time'][0], "%H:%M")
        stamp = datetime(flightDate.year, flightDate.month,
                         flightDate.day, flightTime.hour, flightTime.minute)
        sql = """select * from Flight where flight_num=%s and depart_time=%s;"""
        self.cursor.execute(sql, (flightNumber, stamp))
        temp = self.cursor.fetchone()
        if temp == None:
            return "No Matched Result"
        else:
            return temp['flight_status']
        
       # Customer Car Search
    def publicCarSearch(self,info):
        ret = []
        rent_date = datetime.strptime(info['rent_date'][0], "%Y-%m-%d")
        city = info['city'][0]
        state = info['state'][0]
        country = info['country'][0]

        query = """ SELECT R.name, CA.brand, CA.type, CA.color, CA.base_price, RT.rent_date, RT.return_date
        FROM Rent as RT, Car as CA, rental_company as R
        WHERE RT.car_id = CA.car_id AND CA.company_id = R.company_id
        AND R.city = %s AND R.state = %s AND R.country = %s"""
        self.cursor.execute(query, (city, state,country))
        cars = self.cursor.fetchall()
        for temp in cars:
            if rent_date > temp['return_date']:
                ret.append(temp)
            else:
                return False
        
        # Append unused car to the list
        query2 = """  WITH check_rental as (SELECT *
        FROM rent  FULL outer join car ON rent.car_id = car.car_id
		WHERE rent.car_id IS NULL)
        SELECT R.name, CA.brand, CA.type, CA.color, CA.base_price
        FROM check_rental as CA, rental_company as R
        WHERE CA.company_id = R.company_id AND R.city = %s AND R.state = %s AND R.country = %s"""
        self.cursor.execute(query2, (city, state,country))
        cars_unused = self.cursor.fetchall()
        for temp in cars_unused:
            ret.append(temp)

        return ret
    
    # Customer Hotel Search
    def publicHotelSearch(self,info):
        ret = []
        check_in_date = datetime.strptime(info['check_in_date'][0], "%Y-%m-%d")
        city = info['city'][0]
        state = info['state'][0]
        country = info['country'][0]

        query = """ SELECT H.name, H.stars, R.number, R.price, Re.check_in_date, Re.check_out_date
        FROM Reserve as Re, Room as R, Hotel as H
        WHERE R.room_id = Re.room_id AND R.hotel_id = H.hotel_id
        AND H.city = %s AND H.state = %s AND H.country = %s"""
        self.cursor.execute(query, (city, state,country))
        hotels = self.cursor.fetchall()
        for temp in hotels:
            if check_in_date > temp['check_out_date']:
                ret.append(temp)
            else:
                return False

        # Append unused room to the list
        query2 = """  WITH check_room as (SELECT *
        FROM reserve  FULL outer join room ON reserve.room_id = room.room_id
		WHERE reserve.room_id IS NULL)
        SELECT H.name, H.stars, CR.number, CR.price
        FROM check_room as CR, hotel as H
        WHERE CR.hotel_id = H.hotel_id AND H.city = %s AND H.state = %s AND H.country = %s"""
        self.cursor.execute(query2, (city, state,country))
        cars_unused = self.cursor.fetchall()
        for temp in cars_unused:
            ret.append(temp)

        return ret
