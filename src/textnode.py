from enum import Enum

class TextType(Enum):
    text = 'plaintext'
    bold = 'boldtext'
    italic = 'italictext'
    code = 'code'
    link = 'link'
    image = 'img'

class TextNode():
    def __init__(self, text: str, text_type:TextType, url:str):
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