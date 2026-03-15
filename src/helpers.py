import re

from htmlnode import LeafNode # tag:str|None, value:str, props:dict=None
from textnode import TextType, TextNode

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




