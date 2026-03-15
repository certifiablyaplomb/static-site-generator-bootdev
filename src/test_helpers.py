import unittest

from textnode import *
from helpers import *

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

    def test_multiple_nodes(self):
        expected = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word, and this is another ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(", followed by additional text for testing", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word, and this is another ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(", followed by additional text for testing", TextType.TEXT)
            ]
        node = TextNode(f"This is text with a `code block` word, and this is another **bold block**, followed by additional text for testing", TextType.TEXT)
        new_nodes = [node, node]
        for delimiter in delimiters_map:
            new_nodes = split_nodes_delimiter(new_nodes, delimiters_map[delimiter], delimiter)
        self.assertEqual(new_nodes, expected)

class TestMarkdownImageExtractor(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images(self):
        text= "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ![duplicate image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), 
                              ("duplicate image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_not_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

class TestMarkdownLinkExtractor(unittest.TestCase):
    def test_extract_link(self):
        text= "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
        
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),
                              ("to youtube","https://www.youtube.com/@bootdotdev")], matches)

    def test_not_extract_image(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

class TestSplitNodeImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and follow-up text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and follow-up text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )

    def test_not_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_not_split_links1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_no_trailing_empty_strings(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes
        )
    
    def test_multiple_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )

class TestSplitNodeLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and follow-up text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and follow-up text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )

    def test_not_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_not_split_images1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, url="https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )

    def test_no_trailing_empty_strings(self):
        node = TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes
        )
    
    def test_multiple_nodes(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node, node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, url="https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, url="https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, url="https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, url="https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )


