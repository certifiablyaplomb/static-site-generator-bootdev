from enum import Enum
import re


from htmlnode import LeafNode, ParentNode # tag:str|None, value:str, props:dict=None
from textnode import *


##converts a text node to an html Leaf Node
def text_node_to_html_node(text_node):
    match text_node.text_type.name:
        case "TEXT":
            return LeafNode(tag=None, value=text_node.text)
        case "BOLD":
            return LeafNode(tag="b", value=text_node.text)
        case "ITALIC":
            return LeafNode(tag="i", value=text_node.text)
        case "CODE":
            return LeafNode(tag="code", value=text_node.text)
        case "LINK":
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case "IMAGE":
            return LeafNode(tag="img", value='', props={
                "src":text_node.url,
                "alt":text_node.text
                })
        case _:
            raise Exception(f"An Unknown Error Occured, texttype = {text_node.text_type.name}")

##returns new list of updated textnodes representing one inline element
def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType):
    new_nodes = [] #list of lists
    for node in old_nodes:
        if node.text_type!= TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        try:
            former, value, latter = node.text.split(delimiter, 2)
        except ValueError:
            raise Exception(f'expected closing delimiter: {delimiter}')
        
        if former.strip() != '':
            new_nodes_list = [
                TextNode(former, TextType.TEXT),
                TextNode(value, text_type)
            ]
        else:
            new_nodes_list = [
                TextNode(value, text_type)
            ]
        if latter.strip() != '':
            new_nodes_list.extend(split_nodes_delimiter( [TextNode(latter, TextType.TEXT)], delimiter, text_type) )
        new_nodes.extend(new_nodes_list)

    return new_nodes

#extracts markdown images
def extract_markdown_images(text): #![linkname](url)
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

#extracts markdown links
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(nodes):
    final_list=[]
    for node in nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images == None:
            final_list.append(node)
            continue
        text = node.text
        for image in images:
            former, latter = text.split(f'![{image[0]}]({image[1]})')
            if former != '':
                final_list.append(TextNode(former, TextType.TEXT))
                final_list.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            else:
                final_list.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            ##cut the chain and start from next point
            text = latter
        if text != '':
            final_list.append(TextNode(text, TextType.TEXT))
    return final_list

def split_nodes_link(nodes):
    final_list=[]
    for node in nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue

        links = extract_markdown_links(node.text)
        if links == None:
            final_list.append(node)
            continue
        text = node.text
        for link in links:
            former, latter = text.split(f'[{link[0]}]({link[1]})')
            if former != '':
                final_list.append(TextNode(former, TextType.TEXT))
                final_list.append(TextNode(link[0], TextType.LINK, url=link[1]))
            else:
                final_list.append(TextNode(link[0], TextType.LINK, url=link[1]))
            ##cut the chain and start from next point
            text = latter
        if text != '':
            final_list.append(TextNode(text, TextType.TEXT))
    return final_list

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

##############################
######## BLOCK TYPE ##########
##############################
class BlockType(Enum):
    PARAGRAPH = 'p', #p
    HEADING = 'h', #h1
    CODE = 'code', #code
    QUOTE = 'blockquote', #blockquoute
    UNORDERED_LIST = 'ul', #ul
    ORDERED_LIST = 'ol' #ol

##takes a markdown string and converts it to text ##strips each individual line of independant whitespace chars
def markdown_to_blocks(document_as_string):
    blocks = document_as_string.split("\n\n") ##list of strings including '\n' chars
    return list(filter(lambda x: x !='', map(lambda x: x.strip(), blocks)))

def block_to_block_type(block):
    
    if re.fullmatch(r"#{1,6} .+", block):
        return BlockType.HEADING

    elif block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    
    elif all(map(lambda x: x.startswith(">")
                 , block.split('\n'))):
        return BlockType.QUOTE

    elif all(map(lambda x: x.startswith("- "), block.split('\n'))):
        return BlockType.UNORDERED_LIST
    
    elif all(map(lambda x: x[1].startswith(f'{x[0] + 1}. '), enumerate(block.split('\n')))):
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH

#get blocks
#determine their type
#instantiate as parent
def markdown_to_html_node(document_as_string):
    blocks = markdown_to_blocks(document_as_string)
    all_blocks = []
    for block in blocks:
        html_text = block_to_html(block)
        if html_text[0] != 'pre':
            child_text_nodes = text_to_textnodes(html_text[1])
        else:
            child_text_nodes = [TextNode(html_text[1], TextType.TEXT)]
        child_nodes = list(map(text_node_to_html_node, child_text_nodes)) 
        all_blocks.append(ParentNode(html_text[0], child_nodes))
    return ParentNode('div', all_blocks)

def block_to_html(block): #returns tuple of tag and text
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return ("p", block.replace('\n', ' ').strip())
        
        case BlockType.HEADING:
            i = 0
            while block[i] == '#':
                i += 1
            altered_block = block.replace('#', '', i)
            return (f'h{i}', altered_block.strip()) 
        
        case BlockType.CODE:
            block_lines = block.split('\n')
            snipped = '\n'.join(block_lines[1:-1])
            return ('pre', f'<code>{snipped}\n</code>')

        case BlockType.QUOTE:
            altered_block = block.replace('>', '', 1)
            return ('blockquote', altered_block.replace('\n', ' ').strip())
        
        case BlockType.UNORDERED_LIST:
            block_lines = block.split('\n')
            altered_lines = map(lambda x: x[1].replace('- ', '<li>') + '</li>', 
                                enumerate(block_lines))
            new_block = ''.join(altered_lines)
            return ('ul', new_block)
        case BlockType.ORDERED_LIST:
            block_lines = block.split('\n')
            altered_lines = map(lambda x: x[1].replace(f'{x[0] + 1}. ', '<li>') + '</li>', 
                                enumerate(block_lines))
            new_block = ''.join(altered_lines)
            return ('ol', new_block)
        
