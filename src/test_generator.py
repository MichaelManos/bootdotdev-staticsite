import unittest

from generator import extract_title


class TestGenerator(unittest.TestCase):
    def test_find_header(self):
        md = """THis
is

not
header

# This is!   
This isn't"""
        self.assertEqual(extract_title(md), "This is!")

    def test_no_header(self):
        md = """"This
has
no header"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_no_space(self):
        md = "#No space"
        self.assertEqual(extract_title(md), "No space")
