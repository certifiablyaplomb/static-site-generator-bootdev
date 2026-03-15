from textnode import *
from helpers import split_nodes_delimiter, split_nodes_image, split_nodes_link

delimiters_map ={
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`"
}
def text_to_textnodes(text):
    father_node = TextNode(text, TextType.TEXT)
    new_nodes = [father_node]
    for delimiter in delimiters_map:
        new_nodes = split_nodes_delimiter(new_nodes, delimiters_map[delimiter], delimiter)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

##takes a markdown string and converts it to text ##strips each individual line of independant whitespace chars
def markdown_to_blocks(document_as_string):
    blocks = document_as_string.split("\n\n") ##list of strings including '\n' chars
    return list(filter(lambda x: x !='', map(lambda x: x.strip(), blocks)))

