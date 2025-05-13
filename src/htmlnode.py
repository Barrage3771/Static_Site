

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        new_string = ""
        if self.props is None:
            return ""
        for key, value in self.props.items():
            new_string += " " + key + "=" + '"' + value + '"'
        return new_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if self.value is None or self.value == '':
            raise ValueError("LeafNode must have value")
        elif self.tag is None:
            return f"{self.value}"

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"


