from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/instructors')
def template_demo():
    path = os.getcwd()
    # Get data from Database
    # db_path = "G:\Interview\Data\810_startup_Yongchang_Yao.db"
    db_path = os.path.join(path, "810_startup_Yongchang_Yao.db")
    try:
        db = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        print(f"Error: Unable to open database at {db_path}")
    else:
       query ="""select i.CWID,i.Name,i.Dept,g.Course,count(*) as Students from grades g join instructors i on g.InstructorCWID=i.CWID
                                        group by i.CWID,i.Name,i.Dept,g.Course"""
    data = [{'cwid': cwid, 'name': name, 'dept': dept, "courses": courses, "students": students}
                for cwid, name, dept, courses, students in db.execute(query)]
    db.close()
    # render HTML
    return render_template('instructors_summary.html', title='Stevens Repository',
                           table_title="Number of student by courses and instructor",students = data)


if __name__ == "__main__":
    app.run(debug=True)
