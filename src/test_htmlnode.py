import unittest

from htmlnode import HTMLNode


test_props = {
                "href": "https://www.google.com",
                "target": "_blank"
            }

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        expected = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(tag="a", 
                        value="a dog", 
                        children=None, 
                        props=test_props)
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

    def test_props_to_html1(self):
        expected = ''
        node = HTMLNode(tag="a", 
                        value="a dog", 
                        children=None)
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

    def test_repr(self):
        node = HTMLNode(tag="a", 
                        value="a dog", 
                        children=None, 
                        props=test_props)
        expected = "HTMLNode(a, a dog, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        actual = repr(node)
        self.assertEqual(actual, expected)