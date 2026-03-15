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

class TestTextToTextNodes(unittest.TestCase):
    def test_base_test(self):
        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)
###########
## BLOCK ##
###########
class TestMarkdownToBlocks(unittest.TestCase):
    def test_expected_split(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
                ]
        actual = markdown_to_blocks(md)
        self.assertListEqual(expected, actual)

    def test_additional_blank_lines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
                ]
        actual = markdown_to_blocks(md)
        self.assertListEqual(expected, actual)

    def test_additional_blank_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
                ]
        actual = markdown_to_blocks(md)
        self.assertListEqual(expected, actual)

block_map = {
    BlockType.PARAGRAPH: [
        "this is a paragraph block"
    ],
    BlockType.HEADING: [
        "# Heading1",
        "## Heading2",
        "### Heading3",
        "#### Heading4",
        "##### Heading5",
    ],
    BlockType.CODE: [
        "```\nthis is a code block\n```"
    ],
    BlockType.QUOTE: [
        ">this is a quote block",
        "> this is a different quote block"
    ],
    BlockType.UNORDERED_LIST: [
        "- list1\n- list2\n- list3"
    ],
    BlockType.ORDERED_LIST: [
        "1. list1\n2. list2\n3. list3"
    ]
}
invalid_block_map = {
    BlockType.PARAGRAPH: [
        "this is a paragraph block"
    ],
    BlockType.HEADING: [
        "#Heading1",
        "##Heading2",
        "###Heading3",
        "####Heading4",
        "#####Heading5",
    ],
    BlockType.CODE: [
        "``\nthis is a code block\n```"
    ],
    BlockType.QUOTE: [
        "this is a quote block",
        " this is a different quote block"
    ],
    BlockType.UNORDERED_LIST: [
        "- list1\n list2\n- list3"
    ],
    BlockType.ORDERED_LIST: [
        "1. list1\n. list2\n3. list3"
    ]
}
class TestBlockToBlockType(unittest.TestCase):
    def test_each_with_map(self):
        for case in block_map:
            for block in block_map[case]:
                result = block_to_block_type(block)
                self.assertEqual(case, result)

    def test_each_with_invalid_map(self):
        for case in invalid_block_map:
            for block in invalid_block_map[case]:
                result = block_to_block_type(block)
                self.assertEqual(BlockType.PARAGRAPH, result)

#first list is input, second is expected output from block to html, third is final expected html
block_conversion_map = {
    BlockType.PARAGRAPH: [
        ["this is a paragraph block"], 
        [("p", "this is a paragraph block")],
        ["<div><p>this is a paragraph block</p></div>"]
    ],
    BlockType.HEADING: [
    [
        "# Heading1",
        "## Heading2",
        "### Heading3",
        "#### Heading4",
        "##### Heading5",
    ], 
    [
        ("h1", "Heading1"),
        ("h2", "Heading2"),
        ("h3", "Heading3"),
        ("h4", "Heading4"),
        ("h5", "Heading5")
    ],
    [
        "<div><h1>Heading1</h1></div>",
        "<div><h2>Heading2</h2></div>",
        "<div><h3>Heading3</h3></div>",
        "<div><h4>Heading4</h4></div>",
        "<div><h5>Heading5</h5></div>",
    ]],
    BlockType.CODE: [
    [
        "```\nthis is a code block\n```"
    ],
    [
        ('pre', '<code>this is a code block\n</code>')
    ],
    [
        "<div><pre><code>this is a code block\n</code></pre></div>"
    ]],
    BlockType.QUOTE: [
    [
        ">this is a quote block",
        "> this is a different quote block"
    ],
    [
        ('blockquote', 'this is a quote block'),
        ('blockquote', 'this is a different quote block')
    ],
    [
        "<div><blockquote>this is a quote block</blockquote></div>",
        "<div><blockquote>this is a different quote block</blockquote></div>"  
    ]],
    BlockType.UNORDERED_LIST: [
    [
        "- list1\n- list2\n- list3"
    ],
    [
        ('ul','<li>list1</li><li>list2</li><li>list3</li>')
    ],
    [
        "<div><ul><li>list1</li><li>list2</li><li>list3</li></ul></div>"
    ]],
    BlockType.ORDERED_LIST: [
    [
        "1. list1\n2. list2\n3. list3"
    ],
    [
        ('ol','<li>list1</li><li>list2</li><li>list3</li>')
    ],
    [
        "<div><ol><li>list1</li><li>list2</li><li>list3</li></ol></div>"
    ]]
}
class TestBlockToHTML(unittest.TestCase):
    def test_each_with_map(self):
        for case in block_conversion_map:
            for i in range(len(block_conversion_map[case][0])):
                result = block_to_html(block_conversion_map[case][0][i])
                self.assertEqual(block_conversion_map[case][1][i], result)

class TestMarkDownToHTMLNode(unittest.TestCase):
    def test_each_with_map(self):
        for case in block_conversion_map:
            for i in range(len(block_conversion_map[case][0])):
                result = markdown_to_html_node(block_conversion_map[case][0][i])
                self.assertEqual(block_conversion_map[case][2][i], result.to_html())

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        