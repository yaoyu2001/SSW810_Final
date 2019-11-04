# Homework 9 Test
# Yongchang Yao
import unittest
from datetime import datetime, timedelta
from HW09_Yongchang_Yao import main,Student,Instructor,file_reading_gen,Repository


class TestHomework09(unittest.TestCase):

    def test_Hw09(self):
        """Test Homework09"""
        student_data = {'10103': '[]'}
        path = "G:\Interview\Data"
        """Create a class to store all data"""
        stevens = Repository(path)
        """Test student"""

        for student in stevens._students.keys():
            if student == 10103:
                self.assertEqual(student._Name, "Baldwin, C")
                self.assertEqual(student._Major, "SYEN")
                self.assertEqual(student._course_rank, {'SSW 567': 'A', 'SSW 564': 'A-', 'SSW 687': 'B', 'CS 501': 'B'})
                self.assertEqual(student._course_rank['SSW 567'], 'A')
            elif student == 10183:
                self.assertEqual(student._Name, "Chapman, O")
                self.assertEqual(student._Major, "SYEN")
                self.assertEqual(student._course_rank, {'SSW 689': 'A'})
                self.assertEqual(student._course_rank['SSW 689'], 'A')

        """Test instructor"""
        for instructor in stevens._instructors.keys():
            if instructor == 98760:
                self.assertEqual(instructor._Name, "Darwin, C")
                self.assertEqual(instructor._Department, "SYEN")
                self.assertEqual(instructor._course_students["SYS 800"], 1)
            if instructor == 98765:
                self.assertEqual(instructor._Name, "Einstein, A")
                self.assertEqual(instructor._Department, "SFEN")
                self.assertEqual(instructor._course_students["SSW 567"], 4)


if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)
