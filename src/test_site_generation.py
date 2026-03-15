import unittest

from site_generation import *

class TestExtractHTML(unittest.TestCase):
    def test_basic_header_extraction(self):
        md = "# header1"
        expected = 'header1'
        actual = extract_title(md)
        self.assertEqual(expected, actual)

    def test_header_extraction(self):
        md = """
# header1

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        expected = 'header1'
        actual = extract_title(md)
        self.assertEqual(expected, actual)

    def test_header2_comes_first(self):
            md = """
    ## header 2

    # header1

    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
            expected = 'header1'
            actual = extract_title(md)
            self.assertEqual(expected, actual)

    def test_header_has_space(self):
            md = """
    ## header 2

    # header 1

    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
            expected = 'header 1'
            actual = extract_title(md)
            self.assertEqual(expected, actual)

