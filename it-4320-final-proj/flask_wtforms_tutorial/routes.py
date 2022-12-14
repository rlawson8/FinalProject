from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *


#@app.route("/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():

    form = AdminLoginForm()
    load = loadTakenSeats()
    createChart = createSeatingChart(load)
    sales= get_total_sales()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            passcode_verified = check_passcodes(username, password)
            if passcode_verified:
                err = None
                return render_template("admin.html", form=form, template="form-template", err=err, seatingChart=createChart, totalsales=sales)
            else:
                err = "Bad username/password combination. Try Again"
                return render_template("admin.html", form=form, template="form-template", err=err)

        
    return render_template("admin.html", form=form, template="form-template")

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()
    load = loadTakenSeats()
    createChart = createSeatingChart(load)

    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            row = int(request.form['row'])-1
            seat = int(request.form['seat'])-1
            
            seatTaken = checkIfSeatTaken(row, seat)
            if seatTaken:
                reservation_code = create_reservation_code(first_name, last_name, row, seat)

                err = None
                addToFile(first_name, str(row), str(seat), reservation_code)
                load = loadTakenSeats()
                createChart = createSeatingChart(load)
                return render_template("reservations.html", form=form, template="form-template", err = err, seatingChart=createChart, reservation_code=reservation_code, first_name=first_name, row=row+1, seat=seat+1)
            else:
                err = "Seat is already taken. Try Again"
                return render_template("reservations.html", form=form, template="form-template", err = err, seatingChart=createChart)


    return render_template("reservations.html", form=form, template="form-template", seatingChart=createChart)

