from __future__ import annotations


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other: HTMLNode) -> bool:
        for attribute in ["tag", "value", "children", "props"]:
            if getattr(self, attribute) != getattr(other, attribute):
                return False
        return True

    def __repr__(self) -> str:
        print(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        prop_list = [f' {key}="{self.props[key]}"' for key in self.props]
        return "".join(prop_list)


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __repr__(self) -> str:
        print(f"LeafNode({self.tag}, {self.value}, {self.props})")

    def to_html(self) -> str:
        if self.value is None or self.value == "":
            raise ValueError("Leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        prop_str = self.props_to_html()
        return f"<{self.tag}{prop_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __repr__(self) -> str:
        print(f"ParentNode({self.tag}, {self.children}, {self.props})")

    def to_html(self) -> str:
        if self.tag is None or self.tag == "":
            raise ValueError("Parent nodes must have a tag.")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent nodes must have children.")
        prop_str = self.props_to_html()
        children_str = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{prop_str}>{children_str}</{self.tag}>"
