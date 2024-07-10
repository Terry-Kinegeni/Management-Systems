from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Patient management data
patients = []

# Route to display all patients
@app.route('/')
def index():
    return render_template('index.html', patients=patients)

# Route to add a new patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        illness = request.form['illness']
        patient = {"name": name, "age": age, "illness": illness}
        patients.append(patient)
        return redirect(url_for('index'))
    return render_template('add_patient.html')

# Route to search for a patient by name
@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        name = request.form['name']
        for patient in patients:
            if patient['name'].lower() == name.lower():
                return render_template('search_result.html', patient=patient)
        return render_template('search_result.html', patient=None)
    return render_template('search_patient.html')

# Route to remove a patient by name
@app.route('/remove', methods=['GET', 'POST'])
def remove_patient():
    if request.method == 'POST':
        name = request.form['name']
        for patient in patients:
            if patient['name'].lower() == name.lower():
                patients.remove(patient)
                return redirect(url_for('index'))
        return render_template('remove_patient.html', not_found=True)
    return render_template('remove_patient.html', not_found=False)

if __name__ == '__main__':
    app.run(debug=True)
