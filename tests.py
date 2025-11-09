# tests.py

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_files_info import schema_get_file_info

from google.genai import types



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
        result = write_file("./calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertFalse(result.startswith("Error:"), msg=result)

    def test_writes_to_new_file(self):
        result = write_file("./calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)
        self.assertFalse(result.startswith("Error:"), msg=result)

    def test_writes_to_unknown_file(self):
        
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        self.assertTrue(result.startswith("Error:"))
        
class TestRunPythonFile(unittest.TestCase):
    
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
        
    class TestFunctionSchemas(unittest.TestCase):
        def test_schema_get_file_content_shape(self):
            decl, tool = schema_get_file_content(types)

            # basic declaration checks
            self.assertEqual(decl.name, "get_file_content")
            self.assertIsNotNone(decl.parameters)
            self.assertEqual(decl.parameters.type, types.Type.OBJECT)

            # properties
            props = decl.parameters.properties
            self.assertIn("file_path", props)
            self.assertEqual(props["file_path"].type, types.Type.STRING)

            # required
            req = getattr(decl.parameters, "required", [])
            self.assertIn("file_path", req)

            # optional: tool contains this declaration
            self.assertIn(decl, getattr(tool, "function_declarations", []))
            
        def test_schema_run_python_file(self):
            decl, tool = schema_run_python_file(types)

            # basic declaration checks
            self.assertEqual(decl.name, "run_python_file")
            self.assertIsNotNone(decl.parameters)
            self.assertEqual(decl.parameters.type, types.Type.OBJECT)

            # properties
            props = decl.parameters.properties
            self.assertIn("file_path", props)
            self.assertEqual(props["file_path"].type, types.Type.STRING)

            # required
            req = getattr(decl.parameters, "required", [])
            self.assertIn("file_path", req)

            # optional: tool contains this declaration
            self.assertIn(decl, getattr(tool, "function_declarations", []))
            
        def test_schema_write_file(self):
            decl, tool = schema_write_file(types)

            # basic declaration checks
            self.assertEqual(decl.name, "write_file")
            self.assertIsNotNone(decl.parameters)
            self.assertEqual(decl.parameters.type, types.Type.OBJECT)

            # properties
            props = decl.parameters.properties
            self.assertIn("file_path", props)
            self.assertEqual(props["file_path"].type, types.Type.STRING)

            # required
            req = getattr(decl.parameters, "required", [])
            self.assertIn("file_path", req)

            # optional: tool contains this declaration
            self.assertIn(decl, getattr(tool, "function_declarations", []))
        
            

if __name__ == "__main__":
    unittest.main()