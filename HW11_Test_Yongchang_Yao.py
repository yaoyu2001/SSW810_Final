# Homework 11 Test
# Yongchang Yao
import unittest
import os
from datetime import datetime, timedelta
from HW11_Yongchang_Yao import Repository


class TestHomework11(unittest.TestCase):

    def test_Hw11(self):
        """Test Homework11"""

        path = os.getcwd()
        """Create a class to store all data"""
        stevens = Repository(path)
        """Test student"""
        student_test = list()
        for student in stevens._students.values():
            student_test.append(student.pt_row())
        self.assertEqual(student_test, [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], {'SSW 555', 'SSW 540'}, 'None'], ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], {'SSW 555', 'SSW 540'}, {'CS 546', 'CS 501'}], ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], {'SSW 540'}, {'CS 546', 'CS 501'}], ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], 'None', 'None']])

        """Test instructor"""
        instructor_test = list()
        for instructor in stevens._instructors.values():
            if instructor._CWID == 98760:
                self.assertEqual(instructor._Name, "Darwin, C")
                self.assertEqual(instructor._Department, "SYEN")
                self.assertEqual(instructor._course_students["SYS 800"], 1)
            if instructor._CWID == 98765:
                self.assertEqual(instructor._Name, "Einstein, A")
                self.assertEqual(instructor._Department, "SFEN")
                self.assertEqual(instructor._course_students["SSW 567"], 4)

        """Test a student's courses, completed and remaining """
        for student in stevens._students.values():
            if student._CWID == 10103:
                self.assertEqual(student._completed_courses, {'CS 501', 'SSW 564', 'SSW 567', 'SSW 687'})
                self.assertEqual(student._course_require.keys(), {'SSW 555'})
                self.assertEqual(student._course_elective.keys(), None)
            elif student._CWID == 10115:
                self.assertEqual(student._completed_courses, {'CS 545', 'SSW 564', 'SSW 567', 'SSW 687'})
                self.assertEqual(student._course_require.keys(), {'SSW 555'})
                self.assertEqual(student._course_elective.keys(), None)
            elif student._CWID == 10172:
                self.assertEqual(student._completed_courses, {'SSW 555', 'SSW 567'})
                self.assertEqual(student._course_require.keys(), {'SSW 564'})
                self.assertEqual(student._course_elective.keys(), {'CS 501', 'CS 513', 'CS 545'})
            elif student._CWID == 10175:
                self.assertEqual(student._completed_courses, {'SSW 564', 'SSW 567', 'SSW 687'})
                self.assertEqual(student._course_require.keys(), {'SSW 555'})
                self.assertEqual(student._course_elective.keys(), {'CS 501', 'CS 513', 'CS 545'})
            elif student._CWID == 11658:
                self.assertEqual(student._completed_courses, {})
                self.assertEqual(student._course_require.keys(), {'SYS 612', 'SYS 671', 'SYS 800'})
                self.assertEqual(student._course_elective.keys(), {'SSW 540', 'SSW 565', 'SSW 810'})
        """Test a major's courses"""
        for major in stevens._majors.values():
            if major._dept == "SYEN":
                self.assertEqual(major._required, {'CS 546', 'CS 570'})
                self.assertEqual(major._elective, {'SSW 565', 'SSW 810'})
            if major._dept == "SFEN":
                self.assertEqual(major._required, {'SSW 540', 'SSW 555', 'SSW 810'})
                self.assertEqual(major._elective, {'CS 501', 'CS 546'})
        """Test instructor summary from database"""
        DB_FILE = "G:\Interview\Data\810_startup_Yongchang_Yao.db"
        instructor_list = stevens.instructor_table_db(DB_FILE)
        self.assertEqual(instructor_list, [['98764', 'Cohen, R', 'SFEN', 'CS 546', '1'], ['98763', 'Rowland, J', 'SFEN', 'SSW 810', '4'], ['98763', 'Rowland, J', 'SFEN', 'SSW 555', '1'], ['98762', 'Hawking, S', 'CS', 'CS 501', '1'], ['98762', 'Hawking, S', 'CS', 'CS 546', '1'], ['98762', 'Hawking, S', 'CS', 'CS 570', '1']])

if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)
