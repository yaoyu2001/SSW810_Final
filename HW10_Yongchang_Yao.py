# Homework 10 SSW810
# Yongchang Yao 10432383

import collections
import os
from prettytable import PrettyTable


class Student:
    """Define a class as student to indicate a student"""
    PT_FIELDS = ["CWID", "Name", "Completed Courses", "Remaining Required", "Remaining Elective"]
    GRADE_PASS = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

    def __init__(self, CWID, Name, Major):
        self._CWID, self._Name, self._Major = CWID, Name, Major
        self._course_rank = collections.defaultdict(str)
        self._course_require = dict()
        self._course_elective = dict()
        self._completed_courses = set()

    def add_course(self, course, grade):
        self._course_rank[course] = grade

    def course_match(self):
        """According to grade and type to get courses list of a student"""
        for name, grade in self._course_rank.items():
            if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+','C']:
                self._completed_courses.add(name)
                if name in self._course_require.keys():
                    self._course_require.pop(name)
                if name in self._course_elective.keys():
                    self._course_elective = None

    def pt_row(self):

        if self._course_elective is not None:
            return [self._CWID, self._Name, sorted(self._completed_courses), sorted(self._course_require.keys()), sorted(self._course_elective.keys())]
        else:
            return [self._CWID, self._Name, sorted(self._completed_courses), sorted(self._course_require.keys()), "None"]


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
    PT_FIELDS = ["Dept", "Required", "Elective"]

    def __init__(self, name, _type, major):
        self._name = name
        self._type = _type
        self._major = major


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
        # Two containers to store data
        self._students = dict()
        self._instructors = dict()
        self._courses = dict()
        self._majors = set()
        # Read data from file
        self._get_students(os.path.join(path, "students.txt"))
        self._get_instructors(os.path.join(path, "instructors.txt"))
        self._get_grade(os.path.join(path, "grades.txt"))
        self._get_course(os.path.join(path, "majors.txt"))
        self._grade_match()

        if pttable:
            self._majors_prettytable()
            self._students_prettytable()
            self._instructors_prettytable()

    def _get_students(self,path):
        """Read students and populate self._students"""
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep=";",header=True):
                self._students[cwid] = Student(cwid,name,major)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_instructors(self, path):
        """Read instructors and populate self._instructors"""
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep="|", header=True):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_grade(self, path):
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path,4,sep='|',header=True):

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
        try:
            for major,type,course_name in file_reading_gen(path,3,sep='\t',header=True):
                self._courses[course_name] = Course(course_name, type, major)
                self._majors.add(major)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

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
            # print(student._Name)
            # print(student._completed_courses)
            # print(student._course_require)
            # print(student._course_elective)

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
        pt = PrettyTable(field_names=Course.PT_FIELDS)
        for major in self._majors:
            required = set()
            elective = set()
            for course in self._courses.values():
                if course._major == major:
                    if course._type == "R":
                        required.add(course._name)
                    elif course._type == "E":
                        elective.add(course._name)
            pt.add_row([major, sorted(required), sorted(elective)])

        print("Major summary")
        print(pt)


def main():
    """Get paths"""
    directory = "G:\Interview\SSW810_Final"

    stevens = Repository(directory, pttable=True)


if __name__ == '__main__':

    main()
