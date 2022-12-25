import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db = SQLAlchemy(app)


class Employer(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20))
    employees = db.Column(db.Integer)
    emp_info = db.relationship('Employee', backref='company')


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    designation = db.Column(db.String(15))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


with app.app_context():
    db.create_all()
    Migrate(app, db, render_as_batch=True)


@app.route('/')
def add_company():
    target = Employer(company_name='target', employees=2000)
    anz = Employer(company_name='anz', employees=50000)
    dell = Employer(company_name='dell', employees=96000)
    microsoft = Employer(company_name='microsoft', employees=1200)
    db.session.add_all([target, anz, dell, microsoft])
    db.session.commit()
    return "Data added"


@app.route('/e')
def add_employee():
    ram = Employee(name='ram', age=35, designation='engineer', company='target')
    rupal = Employee(name='rupal', age=23, designation='Lead engineer', company='anz')
    chaman = Employee(name='chaman', age=35, designation='Manager', company='dell')
    abhishek = Employee(name='abhishek', age=35, designation='Director', company='microsoft')
    db.session.add_all([ram, rupal, chaman, abhishek])
    db.session.commit()
    return "Data added"


if __name__ == "__main__":
    app.run()
