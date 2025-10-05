# tests.py

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from functions.get_file_content import get_file_content
from calculator.pkg.calculator import Calculator
from functions.write_file import write_file
from functions.run_python_file import run_python_file

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")


class TestGetFileContent(unittest.TestCase):
    def test_reads_calculator_main(self):
        result = get_file_content("calculator", "main.py")
        self.assertFalse(result.startswith("Error:"), msg=result)
        self.assertIn('from pkg.calculator import Calculator', result)

    def test_reads_calculator_pkg_calculator(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        self.assertFalse(result.startswith("Error:"), msg=result)
        self.assertIn('class Calculator', result)

    def test_rejects_outside_path(self):
        result = get_file_content("calculator", "/bin/cat")
        self.assertTrue(result.startswith("Error:"))

    def test_rejects_missing_file(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertTrue(result.startswith("Error:"))
        
class TestWriteFile(unittest.TestCase):
    
    def test_not_lorem_ipsum(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertFalse(result.startswith("Error:"), msg=result)

    def test_writes_to_new_file(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)
        self.assertFalse(result.startswith("Error:"), msg=result)

    def test_writes_to_unknown_file(self):
        
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        self.assertTrue(result.startswith("Error:"))
        
class testRunPythonFile(unittest.TestCase):
    
    def test_usage_instructions(self):
        result = run_python_file("calculator", "main.py")
        print(result)
        
    def test_run_calculator(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)
        
    def test_run_tests(self):
        result = run_python_file("calculator", "tests.py")
        print(result)
        
    def test_run_main(self):
        result = run_python_file("calculator", "../main.py")
        print(result)
        self.assertTrue(result.startswith("Error:"), msg=result)
        
    def test_run_non_existent(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertTrue(result.startswith("Error:"), msg=result)
    
if __name__ == "__main__":
    unittest.main()