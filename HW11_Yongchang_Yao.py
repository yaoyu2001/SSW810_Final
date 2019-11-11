# Homework 11 SSW810
# Yongchang Yao 10432383

import collections
import os
from prettytable import PrettyTable
import sqlite3




class Student:
    """Define a class as student to indicate a student"""
    PT_FIELDS = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Elective"]

    def __init__(self, CWID, Name, Major):
        self._CWID, self._Name, self._Major = CWID, Name, Major
        self._course_rank = collections.defaultdict(str)
        self._course_require = dict()
        self._course_elective = dict()
        self._completed_courses = set()

    def add_course(self, course, grade):
        self._course_rank[course] = grade

    # def course_match(self):
    #     """According to grade and type to get courses list of a student"""
    #     for name, grade in self._course_rank.items():
    #         if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+','C']:
    #             self._completed_courses.add(name)
    #             if name in self._course_require.keys():
    #                 self._course_require.pop(name)
    #             if name in self._course_elective.keys():
    #                 self._course_elective = None

    def pt_row(self):
        """Give one line in table of a student"""
        major, passed, rem_required, rem_electives = self._Major.remaining(self._course_rank)
        if rem_electives is not None:
            return [self._CWID, self._Name, major, sorted(passed), rem_required, rem_electives]
        else:
            return [self._CWID, self._Name, major, sorted(passed), rem_required, "None"]


class Instructor:
    """Define a class as student to indicate a Instructor"""
    PT_FIELDS = ["CWID", "Name", "Dept", "Courses", "Students"]

    def __init__(self, CWID, Name, Department):
        self._CWID, self._Name, self._Department = CWID, Name, Department
        self._course_students = collections.defaultdict(int)

    def add_course(self, course):
        self._course_students[course] += 1

    def pt_row(self):
        for course, student_num in self._course_students.items():
            yield [self._CWID, self._Name, self._Department, course, student_num]


class Course:

    """Define a class to show courses"""
    def __init__(self, name, _type, major):
        self._name = name
        self._type = _type
        self._major = major


class Major:
    PT_FIELDS = ["Dept", "Required", "Elective"]
    PASSING_GRADES = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
    """Define a class to show major"""
    def __init__(self, dept):
        self._dept = dept
        self._required = set()
        self._elective = set()

    def add_course(self, course, type):
        """Add a new course to major"""
        if type == 'R':
            self._required.add(course)
        elif type == 'E':
            self._elective.add(course)
        else:
            raise ValueError(f"Major.add_course : expected 'R' or 'E' but found '{type}'")

    def remaining(self, completed):
        """By a list of completed course, get remaining required courses and elective courses"""
        passed = {course for course, grade in completed.items() if grade in Major.PASSING_GRADES}

        rem_required = self._required - passed
        if self._elective.intersection(passed):
            rem_elective = None
        else:
            rem_elective = self._elective
        return self._dept, passed, rem_required, rem_elective

    def pt_row(self):
        """Give one line in table of a Major"""
        return [self._dept, sorted(self._required), sorted(self._elective)]


def file_reading_gen(path, fields=3, sep='\t', header=False):
    """file_reading function"""
    fp = open(path, 'r')
    with fp:
        lines = fp.readlines()
        start = 1 if header else 0
        for i in range(start, len(lines)):
            line = lines[i].strip("\n").split(sep)
            if len(line) != fields:
                raise ValueError(f"‘{os.path.basename(path)}’ has {len(line)} fields "
                                 f"on line {i if header == True else i + 1} but expected {fields}")
            else:

                yield tuple(line)


# A class to store all students instructors and grades
class Repository:
    def __init__(self, path, pttable=False):
        # Connect to database
        DB_FILE = "G:\Interview\Data\810_startup.db"
        db = sqlite3.connect(DB_FILE)
        # Containers to store data
        self._students = dict()
        self._instructors = dict()
        self._courses = dict()
        self._majors = dict()
        # self._majors = set()
        # self._majors_class = set()
        # Read data from file
        try:
            self._get_majors(os.path.join(path, "majors.txt"))
            self._get_students(os.path.join(path, "students.txt"))
            self._get_instructors(os.path.join(path, "instructors.txt"))
            self._get_grade(os.path.join(path, "grades.txt"))
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)
        # self._grade_match()
        # self._get_majors()

        # Upload Instructors_summary to database
        # query = """insert into Instructors_summary (CWID,Name,Dept,Courses,Students)
        #     values(?,?,?,?,?) """
        # for instructor in self._instructors.values():
        #     for row in instructor.pt_row():
        #         db.execute(query, tuple(row))
        #         db.commit()

        if pttable:
            self._majors_prettytable()
            self._students_prettytable()
            self._instructors_prettytable()

    def _get_students(self,path):
        """Read students and populate self._students"""
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep=";",header=True):
                if major not in self._majors:
                    print(f"Student {CWID}'{name}' has unknown major '{major}'")
                else:
                    self._students[cwid] = Student(cwid, name, self._majors[major])
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_instructors(self, path):
        """Read instructors and populate self._instructors"""
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep="\t", header=True):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_grade(self, path):
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path,4,sep='\t',header=True):

                try:
                    self._students[student_cwid].add_course(course, grade)
                except KeyError:
                    print(f"Found grade for unknow student {student_cwid}")

                try:
                    self._instructors[instructor_cwid].add_course(course)
                except KeyError:
                    print(f"Found grade for unknow student {instructor_cwid}")

        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_course(self, path):
        """Get course and major info from data file"""
        try:
            for major,type,course_name in file_reading_gen(path,3,sep='\t',header=True):
                self._courses[course_name] = Course(course_name, type, major)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_majors(self,path):
        """Add courses in major"""
        for major, flag, course in file_reading_gen(path, 3,sep='\t',header=True):
            if major not in self._majors:
                self._majors[major] = Major(major)
            self._majors[major].add_course(course, flag)

    def _grade_match(self):
        """March grade for all students"""
        for student in self._students.values():
            for course in self._courses.values():
                if student._Major == course._major:
                    if course._type == "R":
                        student._course_require[course._name] = course
                    elif course._type == "E":
                        student._course_elective[course._name] = course
            student.course_match()

    def _students_prettytable(self):
        """Print student table"""
        pt = PrettyTable(field_names=Student.PT_FIELDS)

        for student in self._students.values():
            pt.add_row(student.pt_row())

        print("Student summary")
        print(pt)

    def _instructors_prettytable(self):
        """Print instructors table"""
        pt = PrettyTable(field_names=Instructor.PT_FIELDS)
        for instructor in self._instructors.values():
            for row in instructor.pt_row():
                pt.add_row(row)

        print("Instructor summary")
        print(pt)

    def _majors_prettytable(self):
        """Print major summary"""
        pt = PrettyTable(field_names=Major.PT_FIELDS)
        for major in self._majors.values():
            pt.add_row(major.pt_row())

        print("Major summary")
        print(pt)


def main():
    """Get paths"""
    directory = os.getcwd()

    stevens = Repository(directory, pttable=True)


if __name__ == '__main__':
    main()

