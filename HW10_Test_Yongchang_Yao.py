# Homework 10 Test
# Yongchang Yao
import unittest
import os
from datetime import datetime, timedelta
from HW10_Yongchang_Yao import Repository


class TestHomework10(unittest.TestCase):

    def test_Hw10(self):
        """Test Homework10"""

        path = os.getcwd()
        """Create a class to store all data"""
        stevens = Repository(path)
        """Test student"""

        for student in stevens._students.values():
            if student._CWID == 10103:
                self.assertEqual(student._Name, "Baldwin, C")
                self.assertEqual(student._Major, "SYEN")
                self.assertEqual(student._course_rank, {'SSW 567': 'A', 'SSW 564': 'A-', 'SSW 687': 'B', 'CS 501': 'B'})
                self.assertEqual(student._course_rank['SSW 567'], 'A')
            elif student._CWID == 10183:
                self.assertEqual(student._Name, "Chapman, O")
                self.assertEqual(student._Major, "SYEN")
                self.assertEqual(student._course_rank, {'SSW 689': 'A'})
                self.assertEqual(student._course_rank['SSW 689'], 'A')

        """Test instructor"""
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
        # for major in stevens._majors_class:
        #     if major._name == "SYEN":
        #         self.assertEqual(major.required.keys(), {'SYS 612', 'SYS 671', 'SYS 800'})
        #         self.assertEqual(major.elective.keys(), {'SSW 540', 'SSW 565', 'SSW 810'})
        #     if major._name == "SFEN":
        #         self.assertEqual(major.required.keys(), {'SSW 555', 'SSW 564', 'SSW 567'})
        #         self.assertEqual(major.elective.keys(), {'CS 501', 'CS 513', 'CS 545'})


if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)
