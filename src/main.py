from collections import Counter, defaultdict
from graphviz import Digraph


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None


def huffman_encoding(text):
    freq_count = Counter(text)
    nodes = [HuffmanNode(char, freq) for char, freq in freq_count.items()]

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)
        left_node = nodes.pop(0)
        right_node = nodes.pop(0)
        merged = HuffmanNode(None, left_node.freq + right_node.freq)
        merged.left = left_node
        merged.right = right_node
        nodes.append(merged)

    root = nodes[0]
    codes = defaultdict(str)
    assign_codes(root, " ", codes)

    encoded_text = "".join(codes[char] for char in text)
    return encoded_text, dict(codes), root


def assign_codes(node, code, codes):
    if node:
        if node.char:
            codes[node.char] = code
        assign_codes(node.left, code + "0", codes)
        assign_codes(node.right, code + "1", codes)


def create_dot(node, dot=None):
    if dot is None:
        dot = Digraph()
    if node:
        label = f"{node.char}\n{node.freq}" if node.char is not None else f"{node.freq}"
        dot.node(str(id(node)), label=label)
        if node.left:
            left_label = f"{node.left.char}\n{node.left.freq}" if node.left.char is not None else f"{node.left.freq}"
            dot.node(str(id(node.left)), label=left_label)
            dot.edge(str(id(node)), str(id(node.left)))
            create_dot(node.left, dot)
        if node.right:
            right_label = f"{node.right.char}\n{node.right.freq}" if node.right.char is not None else f"{node.right.freq}"
            dot.node(str(id(node.right)), label=right_label)
            dot.edge(str(id(node)), str(id(node.right)))
            create_dot(node.right, dot)
    return dot


def is_valid_input(text):
    return any(c.isalpha() for c in text)


text_input = input("Enter the text you want to encode: ").replace(' ', '_')

while not is_valid_input(text_input):
    print("Invalid input! Please enter a text")
    text_input = input("Enter the text you want to encode: ")

encoded_text, codes, root = huffman_encoding(text_input)

print("Encoded text:", encoded_text)
print("Codes:", codes)

tree_dot = create_dot(root)
tree_dot.render('huffman_tree', format='png', cleanup=True)
print("Huffman Tree has been drawn and saved as 'huffman_tree.png'")
