#Libraries Import
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import re
import hashlib

#Flask App Start
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration for the default database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin551@localhost/flights_1'

# Configuration for the two separate database connections flights1 and flights2
app.config['SQLALCHEMY_BINDS'] = {
    'flights_1': 'postgresql://postgres:admin551@localhost/flights_1',
    'flights_2': 'postgresql://postgres:admin551@localhost/flights_2'
}

db = SQLAlchemy(app)


# Defining a model for the flight_1 and flight_2 data
class Flight_1(db.Model):
    __tablename__ = 'flights_1'
    __bind_key__ = 'flights_1'
    flight_id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.VARCHAR(255), nullable=False)
    flight_type = db.Column(db.VARCHAR(255), nullable=False)
    from_dest = db.Column(db.VARCHAR(255), nullable=False)
    to_dest = db.Column(db.VARCHAR(255), nullable=False)
    flight_status = db.Column(db.VARCHAR(255), nullable=False)
    arrival_time = db.Column(db.VARCHAR(255), nullable=False)
    dep_time = db.Column(db.VARCHAR(255), nullable=False)

class Flight_2(db.Model):
    __tablename__ = 'flights_2'
    __bind_key__ = "flights_2"
    flight_id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.VARCHAR(255), nullable=False)
    flight_type = db.Column(db.VARCHAR(255), nullable=False)
    from_dest = db.Column(db.VARCHAR(255), nullable=False)
    to_dest = db.Column(db.VARCHAR(255), nullable=False)
    flight_status = db.Column(db.VARCHAR(255), nullable=False)
    arrival_time = db.Column(db.VARCHAR(255), nullable=False)
    dep_time = db.Column(db.VARCHAR(255), nullable=False)



@staticmethod
def get_bind_key(to_dest):
        # Hash function to determine the bind key based on ASCII value of to_dest
        ascii_sum = sum(ord(char) for char in to_dest)
        if ascii_sum % 2 == 0:
            return 'flights_1'
        else:
            return 'flights_2'


def get_flight_model(bind_key):
    if bind_key == 'flights_1':
        return Flight_1
    elif bind_key == 'flights_2':
        return Flight_2

#Check for Time validition.
def validate_time(time_str):
    time_regex = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
    return bool(time_regex.match(time_str))



#Flask app respective pages and methods like update,delete etc
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect('/login')

    if request.method == 'POST':
        if 'view' in request.form:
            flights = []

            '''# Retrieve flights from flights_1 database
            with db.get_engine(bind='flights_1').connect() as conn:
                flights_1 = conn.execute(db.select(Flight_1)).fetchall()

            # Retrieve flights from flights_2 database
            with db.get_engine(bind='flights_2').connect() as conn:
                flights_2 = conn.execute(db.select(Flight_2)).fetchall()'''
            #Flights from database flights_1
            engine_flights_1 = db.get_engine(bind='flights_1')
            Session_flights_1 = sessionmaker(bind=engine_flights_1)
            session_flights_1 = Session_flights_1()
            flights_1 = session_flights_1.query(Flight_1).all()
            session_flights_1.close()
            #Flights from database flights_2
            engine_flights_2 = db.get_engine(bind='flights_2')
            Session_flights_2 = sessionmaker(bind=engine_flights_2)
            session_flights_2 = Session_flights_2()
            flights_2 = session_flights_2.query(Flight_2).all()
            session_flights_2.close()

            flights = sorted(flights_1 + flights_2,key=lambda x:x.flight_id)

            return render_template('admin.html', flights=flights)
        elif 'add' in request.form:
            flight_id = request.form['flight_id']
            airline = request.form['airline']
            flight_type = request.form['flight_type']
            from_dest = request.form['from_dest']
            to_dest = request.form['to_dest']
            flight_status = request.form['flight_status']
            arrival_time = request.form['arrival_time']
            dep_time = request.form['dep_time']
            #Checking Arrival time
            if not validate_time(arrival_time) or not validate_time(dep_time):
                return "Invalid time format", 400


            bind_key = get_bind_key(to_dest)
            FlightModel = get_flight_model(bind_key)
            new_flight = FlightModel(
                flight_id=flight_id,
                airline=airline,
                flight_type=flight_type,
                from_dest=from_dest,
                to_dest=to_dest,
                flight_status=flight_status,
                arrival_time=arrival_time,
                dep_time=dep_time
            )

            engine = db.get_engine(bind=bind_key)
            Session_addq = sessionmaker(bind=engine)
            session_addq = Session_addq()
            session_addq.add(new_flight)
            session_addq.commit()
            session_addq.close()

         # update Part Start
        elif 'update' in request.form:
            flight_id = request.form.get('flight_idup')

            if not flight_id:
                return "Flight ID is required", 400

            try:
                flight_id = int(flight_id)
            except ValueError:
                return "Invalid Flight ID", 400

            flight = None
            bind_key = None

            # Search for the flight in flights_1 database
            engine_flights_1 = db.get_engine(bind='flights_1')
            Session_flights_1 = sessionmaker(bind=engine_flights_1)
            session_flights_1 = Session_flights_1()
            flight = session_flights_1.query(Flight_1).get(flight_id)

            if flight:
                bind_key = 'flights_1'
                print(f"Flight found in flights_1 database. Flight ID: {flight_id}")
            else:
                session_flights_1.close()

                # Search for the flight in flights_2 database
                engine_flights_2 = db.get_engine(bind='flights_2')
                Session_flights_2 = sessionmaker(bind=engine_flights_2)
                session_flights_2 = Session_flights_2()
                flight = session_flights_2.query(Flight_2).get(flight_id)

                if flight:
                    bind_key = 'flights_2'
                    print(f"Flight found in flights_2 database. Flight ID: {flight_id}")
                else:
                    session_flights_2.close()

            if flight:
                # Render the update form with the flight details
                return render_template('update_flight.html', flight=flight)
            else:
                return "Flight not found", 404

        elif 'update_flight' in request.form:
            flight_id = request.form.get('flight_id')
            airline = request.form.get('airline')
            flight_type = request.form.get('flight_type')
            from_dest = request.form.get('from_dest')
            to_dest = request.form.get('to_dest')
            flight_status = request.form.get('flight_status')
            arrival_time = request.form.get('arrival_time')
            dep_time = request.form.get('dep_time')

            # Check if arrival_time and dep_time are in valid format and range
            if not validate_time(arrival_time) or not validate_time(dep_time):
                return "Invalid time format", 400

            print(f"Updating flight attributes:")
            print(f"Flight ID: {flight_id}")
            print(f"Airline: {airline}")
            print(f"Flight Type: {flight_type}")
            print(f"From Destination: {from_dest}")
            print(f"To Destination: {to_dest}")
            print(f"Flight Status: {flight_status}")
            print(f"Arrival Time: {arrival_time}")
            print(f"Departure Time: {dep_time}")

            # Search for the flight in flights_1 database
            engine_flights_1 = db.get_engine(bind='flights_1')
            Session_flights_1 = sessionmaker(bind=engine_flights_1)
            session_flights_1 = Session_flights_1()
            flight = session_flights_1.query(Flight_1).get(flight_id)

            if flight:
                bind_key = 'flights_1'
                print(f"Flight found in flights_1 database. Flight ID: {flight_id}")
            else:
                session_flights_1.close()

                # Search for the flight in flights_2 database
                engine_flights_2 = db.get_engine(bind='flights_2')
                Session_flights_2 = sessionmaker(bind=engine_flights_2)
                session_flights_2 = Session_flights_2()
                flight = session_flights_2.query(Flight_2).get(flight_id)

                if flight:
                    bind_key = 'flights_2'
                    print(f"Flight found in flights_2 database. Flight ID: {flight_id}")
                else:
                    session_flights_2.close()

            if flight:
                if airline:
                    flight.airline = airline
                if flight_type:
                    flight.flight_type = flight_type
                if from_dest:
                    flight.from_dest = from_dest
                if to_dest:
                    flight.to_dest = to_dest
                if flight_status:
                    flight.flight_status = flight_status
                if arrival_time:
                    flight.arrival_time = arrival_time
                if dep_time:
                    flight.dep_time = dep_time

                if bind_key == 'flights_1':
                    session_flights_1.commit()
                    print(f"Changes committed to flights_1 database for Flight ID: {flight_id}")
                    session_flights_1.close()
                elif bind_key == 'flights_2':
                    session_flights_2.commit()
                    print(f"Changes committed to flights_2 database for Flight ID: {flight_id}")
                    session_flights_2.close()

                return "Flight updated successfully"
            else:
                return "Flight not found", 404

        #Update part Ends
        elif 'delete' in request.form:
            flight_id = request.form['flight_idd']

            try:
                # Search for the flight in flights_1 database
                engine_flights_1 = db.get_engine(bind='flights_1')
                Session_flights_1 = sessionmaker(bind=engine_flights_1)
                session_flights_1 = Session_flights_1()
                flight_1 = session_flights_1.query(Flight_1).get(flight_id)

                if flight_1:
                    session_flights_1.delete(flight_1)
                    session_flights_1.commit()

                session_flights_1.close()

                # Search for the flight in flights_2 database
                engine_flights_2 = db.get_engine(bind='flights_2')
                Session_flights_2 = sessionmaker(bind=engine_flights_2)
                session_flights_2 = Session_flights_2()
                flight_2 = session_flights_2.query(Flight_2).get(flight_id)

                if flight_2:
                    session_flights_2.delete(flight_2)
                    session_flights_2.commit()

                session_flights_2.close()

            except Exception as e:
                print(f"Error while deleting flight: {str(e)}")
                # Log the error or handle it appropriately
                return "Error while deleting flight", 500

    return render_template('admin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'dsci551':
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', error='Invalid password')

    return render_template('login.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        search_column = request.form['search_column']
        search_value = request.form['search_value']

        flights = []

        try:
            # Search in flights_1 database
            engine_flights_1 = db.get_engine(bind='flights_1')
            Session_flights_1 = sessionmaker(bind=engine_flights_1)
            session_flights_1 = Session_flights_1()

            if search_column == 'flight_id':
                flights_1 = session_flights_1.query(Flight_1).filter(Flight_1.flight_id == search_value).all()
            elif search_column == 'airline':
                flights_1 = session_flights_1.query(Flight_1).filter(Flight_1.airline.ilike(f'%{search_value}%')).all()
            elif search_column == 'flight_type':
                flights_1 = session_flights_1.query(Flight_1).filter(
                    Flight_1.flight_type.ilike(f'%{search_value}%')).all()
            elif search_column == 'from_dest':
                flights_1 = session_flights_1.query(Flight_1).filter(Flight_1.from_dest.ilike(f'%{search_value}%')).all()
            elif search_column == 'to_dest':
                flights_1 = session_flights_1.query(Flight_1).filter(Flight_1.to_dest.ilike(f'%{search_value}%')).all()
            elif search_column == 'flight_status':
                flights_1 = session_flights_1.query(Flight_1).filter(
                    Flight_1.flight_status.ilike(f'%{search_value}%')).all()
            else:
                flights_1 = []

            session_flights_1.close()

            # Search in flights_2 database
            engine_flights_2 = db.get_engine(bind='flights_2')
            Session_flights_2 = sessionmaker(bind=engine_flights_2)
            session_flights_2 = Session_flights_2()

            if search_column == 'flight_id':
                flights_2 = session_flights_2.query(Flight_2).filter(Flight_2.flight_id == search_value).all()
            elif search_column == 'airline':
                flights_2 = session_flights_2.query(Flight_2).filter(Flight_2.airline.ilike(f'%{search_value}%')).all()
            elif search_column == 'flight_type':
                flights_2 = session_flights_2.query(Flight_2).filter(
                    Flight_2.flight_type.ilike(f'%{search_value}%')).all()
            elif search_column == 'from_dest':
                flights_2 = session_flights_2.query(Flight_2).filter(Flight_2.from_dest.ilike(f'%{search_value}%')).all()
            elif search_column == 'to_dest':
                flights_2 = session_flights_2.query(Flight_2).filter(Flight_2.to_dest.ilike(f'%{search_value}%')).all()
            elif search_column == 'flight_status':
                flights_2 = session_flights_2.query(Flight_2).filter(
                    Flight_2.flight_status.ilike(f'%{search_value}%')).all()
            else:
                flights_2 = []

            session_flights_2.close()

            flights = flights_1 + flights_2

        except Exception as e:
            print(f"Error while searching flights: {str(e)}")
            # Log the error or handle it appropriately
            return "Error while searching flights", 500

        return render_template('user.html', flights=flights)

    return render_template('user.html')


if __name__ == '__main__':
    app.run()