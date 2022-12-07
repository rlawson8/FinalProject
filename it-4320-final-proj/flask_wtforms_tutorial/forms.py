"""Form class declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
)
#from datetime import date
#from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class UserOptionForm(FlaskForm):
    """Generate Your Graph."""
    
    #THIS IS WHERE YOU WILL IMPLEMENT CODE TO POPULATE THE SYMBOL FIELD WITH STOCK OPTIONS
    option = SelectField("Choose an Option",[DataRequired()],
        choices=[
            ("", "Choose an option"),
            ("1", "Admin Login"),
            ("2", "Reserve a seat"),
        ],
    )

    submit = SubmitField("Submit")


class ReservationForm(FlaskForm):
    """Reservation Form"""
    
    #THIS IS WHERE YOU WILL IMPLEMENT CODE TO POPULATE THE SYMBOL FIELD WITH STOCK OPTIONS
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    row = SelectField("Choose Row", [DataRequired()],
        choices=[
            ("", "Choose a Row"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
    )
    seat = SelectField("Choose Seat", [DataRequired()],
        choices=[
            ("", "Choose a Seat"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
        ],
    )

    reserve = SubmitField("Reserve a Seat")

class AdminLoginForm(FlaskForm):
    """Admin login form"""
    
    #THIS IS WHERE YOU WILL IMPLEMENT CODE TO POPULATE THE SYMBOL FIELD WITH STOCK OPTIONS
    username = StringField('Username', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    login = SubmitField("Login")

def loadTakenSeats():
    f = open("reservations.txt")
    taken_seats = []
    d = True
    while d == True:
        line = f.readline().replace("\n","")
        if line == "":
            d = False
        else:
            line_separated = line.split(',')
            seats = [line_separated[1],line_separated[2]]
            taken_seats.append(seats)
    f.close()
    return taken_seats

def addToFile(first_name, row, seat, reservation_code):
    f = open("reservations.txt", "a")
    f.write(first_name + ", " + row + ", " + seat + ", " + reservation_code + "\n")
    f.close()
    
def checkIfSeatTaken(row, seat):
    f = open("reservations.txt", "r")
    lines = f.readlines()
    seat_value = row + ", " + seat

    for line in lines:
        print(line)
        if seat_value in line:
            f.close()
            return False
        else:
            f.close()
            return True

def createSeatingChart(taken_seats):
    seating = []
    for x in range(12):
        row = []
        a = 0
        for a in range(4):
            row.append("O")
        seating.append(row)
    for x in taken_seats:
        seating[int(x[0])][int(x[1])] = "X"
    return seating

def check_passcodes(username, password):
    f = open("passcodes.txt", "r")
    passcode_verified = False
    passcodes = f.read().splitlines()
    for line in passcodes:
        line = line.split(",")
        line[1] = line[1].lstrip()
        if line[0] == username and line[1] == password:
            passcode_verified = True
            break
    f.close()
    return passcode_verified

def create_reservation_code(first_name, last_name, row, seat):
    INFOTC4320 = "INFOTC4320"
    if len(first_name) < len(INFOTC4320):
        difference = len(INFOTC4320) - len(first_name)
        for x in range(difference):
            first_name += " "
    elif len(first_name) > len(INFOTC4320):
        difference = len(first_name) - len(INFOTC4320)
        for x in range(difference):
            INFOTC4320 += " "
    reservation_code = ''.join([''.join(t) for t in zip(first_name, INFOTC4320)])
    reservation_code = reservation_code.replace(" ", "")
    return reservation_code
