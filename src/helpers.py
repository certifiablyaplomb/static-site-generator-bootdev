from htmlnode import LeafNode # tag:str|None, value:str, props:dict=None
from textnode import TextType, TextNode

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


