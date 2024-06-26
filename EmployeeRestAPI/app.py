from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///james.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Department(db.Model):
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100))
    dept_location = db.Column(db.String(200))

    def to_dict(self):
        return {
            'dept_id': self.dept_id,
            'dept_name': self.dept_name,
            'dept_location': self.dept_location
        }

class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(200))
    emp_salary = db.Column(db.Float)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))

    def to_dict(self):
        return {
            'emp_id': self.emp_id,
            'emp_name': self.emp_name,
            'emp_salary': self.emp_salary,
            'dept_id': self.dept_id
        }

@app.route("/get_departments", methods=['GET'])
def get_departments():
    try:
        dept_details = Department.query.all()
        return jsonify([dept.to_dict() for dept in dept_details])
    except Exception as msg:
        return {"error": str(msg)}, 500

@app.route("/add_department", methods=['POST'])
def add_department():
    try:
        dept_details = request.get_json()
        new_department = Department(
            dept_id=dept_details["dept_id"],
            dept_name=dept_details["dept_name"],
            dept_location=dept_details["dept_location"]
        )
        db.session.add(new_department)
        db.session.commit()
        return {"Message": "New department details added successfully"}
    except Exception as msg:
        return {"error": str(msg)}, 500

@app.route('/dept_id/<int:dept_id>', methods=['GET'])
def get_employees_by_dept_id(dept_id):
    try:
        emp_data = Employee.query.filter_by(dept_id=dept_id).all()
        dept_data = Department.query.filter_by(dept_id=dept_id).first()
        format_employee_data = [emp.to_dict() for emp in emp_data]
        format_dept_data = dept_data.to_dict() if dept_data else {}
        return jsonify({"employees": format_employee_data, "department": format_dept_data})
    except Exception as msg:
        return {"error": str(msg)}, 500

@app.route("/insert_data", methods=['POST'])
def insert_data():
    try:
        new_data = request.get_json()
        new_department = Department(
            dept_id=new_data["dept_id"],
            dept_name=new_data["dept_name"],
            dept_location=new_data["dept_location"]
        )
        new_employee = Employee(
            emp_id=new_data['emp_id'],
            emp_name=new_data['emp_name'],
            emp_salary=new_data['emp_salary'],
            dept_id=new_data['dept_id']
        )
        db.session.add(new_department)
        db.session.add(new_employee)
        db.session.commit()
        return {"Message": "Data inserted successfully"}
    except Exception as msg:
        return {"error": str(msg)}, 500

@app.before_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
