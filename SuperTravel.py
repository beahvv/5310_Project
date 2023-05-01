from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from Customer import Customer
from Staff import SuperTravelStaff
from Public import Public

app = Flask(__name__)

methd = ['GET', 'POST']


cust = Customer()
staff = SuperTravelStaff()
public = Public()


#
#
#
#
#
#
#
#
#
#
########## Public Dir ##########
@app.route('/')
def index():
    return render_template('public/index.html')


# Login page
@app.route('/login')
def login():
    return render_template('public/login.html')


@app.route('/loginAuth', methods=methd)
def loginAuth():
    info = request.form.to_dict(flat=False)
    if info['type'][0] == "Customer":
        if cust.custLogin(info):
            cust.setEmail(info['username'][0])
            cust.find_set_ticket_ID()
            return render_template('custHome/home.html')
        else:
            return render_template('public/login.html', error='Wrong Username or Password')

    elif info['type'][0] == "Staff":
        if staff.staffLogin(info):
            staff.setUsername(info['username'][0])
            return redirect('/staffHome')
        else:
            return render_template('public/login.html', error='Wrong Username or Password')

# Log out


@app.route('/logout')
def logout():
    cust.reset()
    staff.reset()
    return redirect('/login')

# Sign up


@app.route('/custSnp')
def custSnp():
    return render_template('public/custSnp.html')

# signup processing
@app.route('/snpAuth', methods=methd)
def snpAuth():
    info = request.form.to_dict(flat=False)
    if info['type'][0] == 'Customer':
        if cust.cust_Signup(info):
            return redirect('/login')
        else:
            return render_template('public/custSnp.html',
                                   error="This Email Already Exist")
    return redirect('/')

# Ticket Search in Customer Home
@app.route('/pubTktSrh', methods=methd)
def pubTktSrh():
    return render_template('public/index.html')

@app.route('/pubDisplay', methods=methd)
def pubDisplay():
    info = request.form.to_dict(flat=False)
    ret = public.publicTicketSearch(info)
    if info['trip_type'][0] == "Single Trip":
        return render_template('public/display.html', info=ret, ports=info)
    elif info['trip_type'][0] == "Round Trip":
        return render_template('public/display_round.html', info=ret, ports=info)

@app.route('/pubStsSrh', methods=methd)
def pubStsSrh():
    return render_template('public/stsSrh.html')

@app.route('/pubStsRes', methods=methd)
def pubStsRes():
    info = request.form.to_dict(flat=False)
    ret = public.check_flight_status(info)
    return render_template('public/stsRes.html', info=info, status=ret)

@app.route('/pubHotelSrh', methods=methd)
def pubHotelSrh():
    return render_template('public/hotelSrh.html')

@app.route('/pubHotelRes', methods=methd)
def pubHotelRes():
    info = request.form.to_dict(flat=False)
    ret = public.publicHotelSearch(info)
    return render_template('public/displayHotel.html', info=ret, ports=info)

@app.route('/pubCarSrh', methods=methd)
def pubCarSrh():
    return render_template('public/CarSrh.html')    

@app.route('/pubCarRes', methods=methd)
def pubCarRes():
    info = request.form.to_dict(flat=False)
    ret = public.publicCarSearch(info)
    return render_template('public/displayCar.html', info=ret, ports=info)


########## End of Public Dir ##########
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
########## Customer Home Dir ##########


@app.route('/custHome')
def custHome():
    return render_template('custHome/home.html')


# Ticket Search in Customer Home
@app.route('/custHome/ticketSrh', methods=methd)
def custHome_ticketSrh():
    if (cust.getEmail()):
        return render_template('custHome/ticketSrh.html')
    else:
        return redirect("/login")
    
# Hotel Search in Customer Home
@app.route('/custHome/hotelSrh', methods=methd)
def custHome_hotelSrh():
    if (cust.getEmail()):
        return render_template('custHome/hotelSrh.html')
    else:
        return redirect("/login")
    
# Ticket Search in Customer Home
@app.route('/custHome/carSrh', methods=methd)
def custHome_carSrh():
    if (cust.getEmail()):
        return render_template('custHome/carSrh.html')
    else:
        return redirect("/login")


@app.route('/custHome/stsSrh', methods=methd)
def custHome_stsSrh():
    if (cust.getEmail()):
        return render_template('custHome/stsSrh.html')
    else:
        return redirect("/login")


@app.route('/custHome/stsRes', methods=methd)
def custHome_stsRes():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        ret = cust.customer_flight_status_search(info)
        return render_template('custHome/stsRes.html', info=info, status=ret)
    else:
        return redirect("/login")


@app.route('/custHome/info', methods=methd)
def custHome_info():
    info = request.form.to_dict(flat=False)
    return render_template('custHome/info.html', info=request.form)


@app.route('/custHome/display', methods=methd)
def custHome_display():
    if(cust.getEmail()):
        info = request.form.to_dict(flat=False)
        ret = cust.customer_ticket_search(info)
        if info['trip_type'][0] == "Single Trip":
            return render_template('custHome/display.html', info=ret, ports=info)
        elif info['trip_type'][0] == "Round Trip":
            return render_template('custHome/display_round.html', info=ret, ports=info)
    else:
        return redirect("/login")


@app.route('/custHome/purch', methods=methd)
def custHome_purch():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        return render_template('custHome/purch.html', info=info, email=cust.getEmail())
    else:
        return redirect("/login")

@app.route('/custHome/placeOrder', methods=methd)
def custHome_placeOrder():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        if cust.customer_purchase(info):
            return render_template('custHome/home.html', alert_msg="Purchase is seccessful!")
    else:
        return redirect("/login")

@app.route('/custHome/displayHotel', methods=methd)
def custHome_displayHotel():
    if(cust.getEmail()):
        info = request.form.to_dict(flat=False)
        ret = cust.customer_hotel_search(info)
        return render_template('custHome/displayHotel.html', info=ret, ports=info)
    else:
        return redirect("/login")
    
@app.route('/custHome/purchHotel', methods=methd)
def custHome_purchHotel():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        return render_template('custHome/purchHotel.html', info=info, email=cust.getEmail())
    else:
        return redirect("/login")

@app.route('/custHome/placeOrderHotel', methods=methd)
def custHome_placeOrderHotel():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        if cust.customer_purchaseBooking(info):
            return render_template('custHome/home.html', alert_msg="Purchase is seccessful!")
    else:
        return redirect("/login")


@app.route('/custHome/displayCar', methods=methd)
def custHome_displayCar():
    if(cust.getEmail()):
        info = request.form.to_dict(flat=False)
        ret = cust.customer_car_search(info)
        return render_template('custHome/displayCar.html', info=ret, ports=info)
    else:
        return redirect("/login")

@app.route('/custHome/purchCar', methods=methd)
def custHome_purchCar():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        return render_template('custHome/purchCar.html', info=info, email=cust.getEmail())
    else:
        return redirect("/login")

@app.route('/custHome/placeOrderCar', methods=methd)
def custHome_placeOrderCar():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        if cust.customer_purchaseRental(info):
            return render_template('custHome/home.html', alert_msg="Purchase is seccessful!")
    else:
        return redirect("/login")

@app.route('/custHome/futureF', methods=methd)
def custHome_futureF():
    if (cust.getEmail()):
        ret = cust.customer_future_flights()
        return render_template('custHome/futureFlights.html', info=ret)
    else:
        return redirect("/login")
    
@app.route('/custHome/futureB', methods=methd)
def custHome_futureB():
    if (cust.getEmail()):
        ret = cust.customer_future_bookings()
        return render_template('custHome/futureBookings.html', info=ret)
    else:
        return redirect("/login")
    
@app.route('/custHome/futureR', methods=methd)
def custHome_futureR():
    if (cust.getEmail()):
        ret = cust.customer_future_rentals()
        return render_template('custHome/futureRentals.html', info=ret)
    else:
        return redirect("/login")


@app.route('/custHome/pastF', methods=methd)
def custHome_pastF():
    if (cust.getEmail()):
        ret = cust.customer_past_flights()
        return render_template('custHome/pastFlights.html', info=ret)
    else:
        return redirect("/login")
    

@app.route('/custHome/pastB', methods=methd)
def custHome_pastB():
    if (cust.getEmail()):
        ret = cust.customer_past_bookings()
        return render_template('custHome/pastBookings.html', info=ret)
    else:
        return redirect("/login")
    

@app.route('/custHome/pastR', methods=methd)
def custHome_pastR():
    if (cust.getEmail()):
        ret = cust.customer_past_rentals()
        return render_template('custHome/pastRentals.html', info=ret)
    else:
        return redirect("/login")


@app.route('/custHome/rate', methods=methd)
def custHome_tktRate():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        return render_template('custHome/rate.html', info=request.form.to_dict(flat=False), email=cust.getEmail())
    else:
        return redirect("/login")


@app.route('/custHome/regRate', methods=methd)
def custHome_tktRateProcess():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        if cust.register_rating(info):
            return render_template('custHome/home.html', alert_msg="Rate Successful!")
        else:
            return render_template("custHome/rate.html", info=request.form.to_dict(flat=False), email=cust.getEmail(), error="Rating Or Comment Already Exists")
    else:
        return redirect("/login")
    
@app.route('/custHome/rateH', methods=methd)
def custHome_hotelRate():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        return render_template('custHome/rateH.html', info=request.form.to_dict(flat=False), email=cust.getEmail())
    else:
        return redirect("/login")


@app.route('/custHome/regRateH', methods=methd)
def custHome_hotelRateProcess():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        if cust.register_ratingH(info):
            return render_template('custHome/home.html', alert_msg="Rate Successful!")
        else:
            return render_template("custHome/rateH.html", info=request.form.to_dict(flat=False), email=cust.getEmail(), error="Rating Or Comment Already Exists")
    else:
        return redirect("/login")
    
@app.route('/custHome/rateC', methods=methd)
def custHome_companyRate():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        
        return render_template('custHome/rateC.html', info=request.form.to_dict(flat=False), email=cust.getEmail())
    else:
        return redirect("/login")


@app.route('/custHome/regRateC', methods=methd)
def custHome_companyRateProcess():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        if cust.register_ratingC(info):
            return render_template('custHome/home.html', alert_msg="Rate Successful!")
        else:
            return render_template("custHome/rateC.html", info=request.form.to_dict(flat=False), email=cust.getEmail(), error="Rating Or Comment Already Exists")
    else:
        return redirect("/login")


@app.route('/custHome/spendingF', methods=methd)
def custHome_spending_flights():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        ret = cust.track_my_spending_flights(info)
        return render_template('custHome/spendingF.html',
                               ret_total=ret[0], ret_month=ret[1],
                               start=ret[2], end=ret[3])
    else:
        return redirect("/login")
    
@app.route('/custHome/spendingB', methods=methd)
def custHome_spending_hotels():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        ret = cust.track_my_spending_hotels(info)
        return render_template('custHome/spendingB.html',
                               ret_total=ret[0], ret_month=ret[1],
                               start=ret[2], end=ret[3])
    else:
        return redirect("/login")
    
@app.route('/custHome/spendingR', methods=methd)
def custHome_spending_rentals():
    if (cust.getEmail()):
        info = request.form.to_dict(flat=False)
        ret = cust.track_my_spending_rentals(info)
        return render_template('custHome/spendingR.html',
                               ret_total=ret[0], ret_month=ret[1],
                               start=ret[2], end=ret[3])
    else:
        return redirect("/login")

########## End of Customer Home Dir ##########
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
########## Staff Home Dir ##########
@app.route('/staffHome')
def staffHome():
    if (staff.getUsername()):
        return render_template('staffHome/home.html')
    else:
        return redirect("/login")


@app.route('/staffHome/createF')
def staffHome_createF():
    if (staff.getUsername()):
        return render_template('staffHome/createF.html')
    else:
        return redirect("/login")


@app.route('/staffHome/createFlightAuth', methods=methd)
def staffHome_createFAuth():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        ret = staff.staffAddFlight(info)
        if ret[0]:
            return render_template('staffHome/home.html', alert_msg=ret[1])
        else:
            return render_template('staffHome/createF.html', error=ret[1])
    else:
        return redirect("/login")


@app.route('/staffHome/addPlaneAirport')
def staffHome_addPlaneAirport():
    if (staff.getUsername()):
        return render_template('staffHome/addPlanePort.html')
    else:
        return redirect("/login")


@app.route('/staffHome/addPlaneAuth', methods=methd)
def staffHome_addPlaneAuth():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        if(staff.staffAddPlane(info)):
            return render_template('staffHome/home.html', alert_msg="New Plane Added")
        else:
            return render_template('staffHome/addPlanePort.html',
                                   error_plane="Plane ID Already Exist")
    else:
        return redirect("/login")



@app.route('/staffHome/addPortAuth', methods=methd)
def staffHome_addPortAuth():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        if(staff.staffAddPort(info)):
            return render_template('staffHome/home.html', alert_msg="New Airport Added")
        else:
            return render_template('staffHome/addPlanePort.html',
                                   error_port="Port Name Already Exist")
    else:
        return redirect("/login")

@app.route('/staffHome/addAirlineAuth', methods=methd)
def staffHome_addAirlineAuth():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        if(staff.staffAddAirline(info)):
            return render_template('staffHome/home.html', alert_msg="New Airline Added")
        else:
            return render_template('staffHome/addPlanePort.html',
                                   error_airline="Airline Already Exist")
    else:
        return redirect("/login")

@app.route('/staffHome/changeSts')
def staffHome_changeStatus():
    if (staff.getUsername()):
        return render_template('staffHome/changeSts.html')
    else:
        return redirect("/login")


@app.route('/staffHome/changeStsAuth', methods=methd)
def staffHome_changeStatusAuth():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        ret = staff.staffChangeStatus(info)
        if(ret[0]):
            return render_template('staffHome/home.html', alert_msg=ret[1])
        else:
            return render_template('staffHome/changeSts.html', error=ret[1])
    else:
        return redirect("/login")

@app.route('/staffHome/viewFlightReport', methods=methd)
def staffHome_viewFlightReport():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        ret = staff.staffViewFlightReport(info)
        return render_template('staffHome/viewFlightReport.html',
                               ret_total=ret[0],
                               start=ret[1], end=ret[2],ret_destination = ret[3],ret_rating_airline = ret[4])
    else:
        return redirect("/login")


@app.route('/staffHome/viewRentalReport', methods=methd)
def staffHome_viewRentalReport():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        ret = staff.staffViewRentalReport(info)
        return render_template('staffHome/viewRentalReport.html',
                               company_total=ret[0], start=ret[1],end=ret[2],brand_total = ret[3],type_total = ret[4]
                               ,ret_rating_company = ret[5])
    else:
        return redirect("/login")
    
@app.route('/staffHome/viewHotelReport', methods=methd)
def staffHome_viewHotelReport():
    if (staff.getUsername()):
        info = request.form.to_dict(flat=False)
        ret = staff.staffViewHotelReport(info)
        return render_template('staffHome/viewHotelReport.html',
                                hotel_total=ret[0], start=ret[1],end=ret[2],city_total = ret[3],type_total = ret[4]
                               ,ret_rating_hotel = ret[5])
    else:
        return redirect("/login")


########## End of Staff Home Dir ##########
#
#
#
#
#
#
#
#
#
if __name__ == '__main__':
    app.run()
