import unittest

from textnode import TextNode, TextType
from helpers import text_node_to_html_node, split_nodes_delimiter

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

delimiters_map ={
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`"
}
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimiter(self):
        for delimiter in delimiters_map:
            expected = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", delimiter),
                TextNode(" word", TextType.TEXT),
            ]
            node = TextNode(f"This is text with a {delimiters_map[delimiter]}code block{delimiters_map[delimiter]} word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], delimiters_map[delimiter], delimiter)
            self.assertEqual(new_nodes, expected)

    def test_multiple_same_delimiters(self):
        for delimiter in delimiters_map:
            expected = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", delimiter),
                TextNode(" word, and this is another ", TextType.TEXT),
                TextNode("code block", delimiter),
                TextNode(" aswell", TextType.TEXT)
            ]
            node = TextNode(f"This is text with a {delimiters_map[delimiter]}code block{delimiters_map[delimiter]} word, and this is another {delimiters_map[delimiter]}code block{delimiters_map[delimiter]} aswell", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], delimiters_map[delimiter], delimiter)
            self.assertEqual(new_nodes, expected)
            
    def test_multiple_diff_delimiters(self):
        expected = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word, and this is another ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(", followed by additional text for testing", TextType.TEXT)
            ]
        node = TextNode(f"This is text with a `code block` word, and this is another **bold block**, followed by additional text for testing", TextType.TEXT)
        new_nodes = [node]
        for delimiter in delimiters_map:
            new_nodes = split_nodes_delimiter(new_nodes, delimiters_map[delimiter], delimiter)
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter_count(self):
        for delimiter in delimiters_map:
            node = TextNode(f"This is text with a {delimiters_map[delimiter]}code block word", TextType.TEXT)
            self.assertRaises(Exception, split_nodes_delimiter, [node], delimiters_map[delimiter], delimiter)