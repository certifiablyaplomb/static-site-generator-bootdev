from enum import Enum

class TextType(Enum):
    TEXT = 'plaintext'
    BOLD = 'boldtext'
    ITALIC = 'italictext'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'img'

class TextNode():
    def __init__(self, text: str, text_type:TextType, url:str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, rhs):
        if (self.text == rhs.text 
            and self.text_type == rhs.text_type 
            and self.url == rhs.url):
            return True
        return False
    
    def __repr__(self):
        return (f'TextNode({self.text}, {self.text_type.value}, {self.url})')