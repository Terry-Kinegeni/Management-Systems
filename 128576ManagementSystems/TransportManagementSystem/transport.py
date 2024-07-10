from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Vehicle:
    def __init__(self, registration_number, make, model):
        self.registration_number = registration_number
        self.make = make
        self.model = model

class Car(Vehicle):
    def __init__(self, registration_number, make, model, number_of_seats):
        super().__init__(registration_number, make, model)
        self.number_of_seats = number_of_seats

class Truck(Vehicle):
    def __init__(self, registration_number, make, model, cargo_capacity):
        super().__init__(registration_number, make, model)
        self.cargo_capacity = cargo_capacity

class Motorcycle(Vehicle):
    def __init__(self, registration_number, make, model, engine_capacity):
        super().__init__(registration_number, make, model)
        self.engine_capacity = engine_capacity

class Fleet:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def display_all_vehicles(self):
        return self.vehicles

    def search_vehicle_by_registration_number(self, registration_number):
        for vehicle in self.vehicles:
            if vehicle.registration_number == registration_number:
                return vehicle
        return None

fleet = Fleet()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        vehicle_type = request.form['vehicle_type']
        registration_number = request.form['registration_number']
        make = request.form['make']
        model = request.form['model']
        
        if vehicle_type == 'car':
            number_of_seats = request.form['number_of_seats']
            vehicle = Car(registration_number, make, model, int(number_of_seats))
        elif vehicle_type == 'truck':
            cargo_capacity = request.form['cargo_capacity']
            vehicle = Truck(registration_number, make, model, int(cargo_capacity))
        elif vehicle_type == 'motorcycle':
            engine_capacity = request.form['engine_capacity']
            vehicle = Motorcycle(registration_number, make, model, int(engine_capacity))
        
        fleet.add_vehicle(vehicle)
        return redirect(url_for('home'))
    return render_template('add_vehicle.html')

@app.route('/display_vehicles')
def display_vehicles():
    vehicles = fleet.display_all_vehicles()
    return render_template('display_vehicles.html', vehicles=vehicles)

@app.route('/search_vehicle', methods=['GET', 'POST'])
def search_vehicle():
    vehicle = None
    if request.method == 'POST':
        registration_number = request.form['registration_number']
        vehicle = fleet.search_vehicle_by_registration_number(registration_number)
    return render_template('search_vehicle.html', vehicle=vehicle)

if __name__ == '__main__':
    app.run(debug=True)
