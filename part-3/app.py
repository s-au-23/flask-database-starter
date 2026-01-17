from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# ======================
# DATABASE CONFIG
# ======================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# MODELS
# ======================

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    courses = db.relationship('Course', backref='teacher', lazy=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref='students')



# ======================
# ROUTES
# ======================

@app.route('/')
def index():
    students = Student.query.order_by(Student.name).all()
    return render_template('index.html', students=students)


@app.route('/courses')
def courses():
    all_courses = Course.query.limit(10).all()
    return render_template('courses.html', courses=all_courses)


@app.route('/teachers')
def teachers():
    all_teachers = Teacher.query.filter(Teacher.name.like('%John%')).all()
    return render_template('teachers.html', teachers=all_teachers)
from sqlalchemy.exc import IntegrityError

from sqlalchemy.exc import IntegrityError

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        course_id = request.form['course_id']

        # ---------- VALIDATION ----------
        if not name or not email or not course_id:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_student'))

        if '@' not in email:
            flash('Invalid email format!', 'danger')
            return redirect(url_for('add_student'))

        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            flash('Email already exists!', 'danger')
            return redirect(url_for('add_student'))
        # --------------------------------

        student = Student(name=name, email=email, course_id=course_id)

        db.session.add(student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('add.html', courses=courses)


@app.route('/edit-student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course_id = request.form['course_id']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('edit_student.html', student=student, courses=courses)
@app.route('/delete-student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))




@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course = Course(
            name=request.form['name'],
            description=request.form.get('description'),
            teacher_id=request.form['teacher_id']
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses'))

    teachers = Teacher.query.all()
    return render_template('add_course.html', teachers=teachers)

# ======================
# INIT DB (RUN ONCE)
# ======================

def init_db():
    with app.app_context():
        db.create_all()

        if not Teacher.query.first():
            t1 = Teacher(name='John Smith', email='john@example.com')
            t2 = Teacher(name='Alice Johnson', email='alice@example.com')
            db.session.add_all([t1, t2])
            db.session.commit()

            c1 = Course(name='Python Basics', description='Learn Python', teacher_id=t1.id)
            c2 = Course(name='Web Development', description='Flask & Frontend', teacher_id=t2.id)
            db.session.add_all([c1, c2])
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    def __repr__(self):
        return f'<Teacher {self.name}>'