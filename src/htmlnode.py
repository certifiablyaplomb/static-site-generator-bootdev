class HTMLNode(): ##parent
    def __init__(self, 
                tag:str=None, 
                value:str=None, 
                children:list=None, 
                props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ''

        converted = ''
        for prop in self.props.items():
            converted += f' {prop[0]}="{prop[1]}"'
        return converted
    
    def __repr__(self):
        return f'HTMLNode("{self.tag}", "{self.value}", children={self.children}, props={self.props})'
###################  
class LeafNode(HTMLNode):
    def __init__(self, tag:str|None, value:str, props:dict=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        if self.value==None:
            raise ValueError("leaf nodes require value element")
        if self.tag == None:
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
    
    def __repr__(self):
        return f'LeafNode({f'\"{self.tag}\"' if self.tag else None}, "{self.value}", props={self.props})'
    
####################
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError('parent nodes require a tag')
        if not self.children:
            raise ValueError('parent nodes require children')
        # if self.tag != 'pre':
        final_product=f'<{self.tag}{self.props_to_html()}>'
        for element in self.children:
            final_product += element.to_html()
        return f'{final_product}</{self.tag}>'

    def __repr__(self):
        return f'ParentNode(\"{self.tag}\", {list(map(lambda x: repr(x), self.children))}, props={self.props})'
