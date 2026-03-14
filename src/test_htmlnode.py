import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        expected = "HTMLNode(\"a\", \"a dog\", children=None, props={'href': 'https://www.google.com', 'target': '_blank'})"
        actual = repr(node)
        self.assertEqual(actual, expected)

#############################################

class TestLeafNode(unittest.TestCase):
    def test_props_to_html(self):
        expected = ' href="https://www.google.com" target="_blank"'
        node = LeafNode(tag="a", 
                        value="a dog", 
                        props=test_props)
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

    def test_valueless_to_html(self):
            node = LeafNode(tag="a", 
                            value=None)
            self.assertRaises(ValueError, node.to_html)

    def test_tagless_to_html(self):
        expected = 'a dog'
        node = LeafNode(tag=None, 
                        value="a dog")
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_to_html_no_props(self):
        expected = '<p>a dog</p>'
        node = LeafNode(tag='p', 
                        value="a dog")
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_to_html_with_props(self):
        expected = '<a href="https://www.google.com" target="_blank">a dog</a>'
        node = LeafNode(tag='a', 
                        value="a dog",
                        props=test_props)
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_repr(self):
        node = LeafNode(tag="a", 
                        value="a dog", 
                        props=test_props)
        expected = "LeafNode(\"a\", \"a dog\", props={'href': 'https://www.google.com', 'target': '_blank'})"
        actual = repr(node)
        self.assertEqual(actual, expected)

class TestParentNode(unittest.TestCase):
    def test_to_html_non_tree(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_to_html_tree(self):
        node = ParentNode(
            "p",
            [
                ParentNode("div", [
                    LeafNode("i", "layered italic text"),
                    LeafNode("p", "layered paragraph text"),
                    ]),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        expected = "<p><div><i>layered italic text</i><p>layered paragraph text</p></div>Normal text<i>italic text</i>Normal text</p>"
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_repr(self):
        node = ParentNode(tag="a", 
                        children=[
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                        ],
                        props=test_props)
        expected = 'ParentNode("a", [\'LeafNode("b", "Bold text", props=None)\', \'LeafNode(None, "Normal text", props=None)\', \'LeafNode("i", "italic text", props=None)\', \'LeafNode(None, "Normal text", props=None)\'], props={\'href\': \'https://www.google.com\', \'target\': \'_blank\'})'
        actual = repr(node)
        self.maxDiff = None
        self.assertEqual(actual, expected)