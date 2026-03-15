import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "Link", props={"href": "index.html"})
        node2 = HTMLNode("a", "Link", props={"href": "index.html"})
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = HTMLNode("a", "Link", props={"href": "index.html"})
        node2 = HTMLNode("p", "paragraph")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(
            "a", "Link", props={"href": "https://www.google.com", "target": "_blank"}
        )
        target_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), target_output)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_no_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("a", "home", props={"href": "/index.html"})
        parent_node = ParentNode("div", [child_node], props={"id": "link"})
        self.assertEqual(
            parent_node.to_html(), '<div id="link"><a href="/index.html">home</a></div>'
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child1</span><p>child2</p></div>"
        )

    def test_parent_no_children_error(self):
        node = ParentNode("p", children=None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
