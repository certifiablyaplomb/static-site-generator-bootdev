import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node1 = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(node, node1)
    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node1 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node1)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT, "standard text")
        node1 = TextNode("This is a text node", TextType.TEXT, "nonstandard text")
        self.assertNotEqual(node, node1)
    def test_not_eq1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node1 = TextNode("This is a bold node", TextType.BOLD)
        self.assertNotEqual(node, node1)

    
if __name__ == "__main__":
    unittest.main()
