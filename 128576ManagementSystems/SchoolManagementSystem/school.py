from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades

    def get_average_grade(self):
        return sum(self.grades.values()) / len(self.grades)

class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def get_student_average(self, student_name):
        for student in self.students:
            if student.name == student_name:
                return student.get_average_grade()
        return None

    def get_class_average(self, subject):
        total, count = 0, 0
        for student in self.students:
            if subject in student.grades:
                total += student.grades[subject]
                count += 1
        return total / count if count > 0 else None

classroom = Classroom()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        grades = {subject: int(grade) for subject, grade in request.form.items() if subject != 'name'}
        student = Student(name, grades)
        classroom.add_student(student)
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/display_students')
def display_students():
    return render_template('display_students.html', students=classroom.students)

@app.route('/student_average', methods=['GET', 'POST'])
def student_average():
    if request.method == 'POST':
        student_name = request.form['name']
        average = classroom.get_student_average(student_name)
        return render_template('result.html', result=average, student_name=student_name)
    return render_template('student_average.html')

@app.route('/class_average', methods=['GET', 'POST'])
def class_average():
    if request.method == 'POST':
        subject = request.form['subject']
        average = classroom.get_class_average(subject)
        return render_template('result.html', result=average, subject=subject)
    return render_template('class_average.html')

if __name__ == '__main__':
    app.run(debug=True)
