"""
    霍夫曼（Huffman）编码是一种将字符（或符号）转换为可变长度二进制位串的无损数据压缩算法。
    它利用出现频率较高的字符使用较短的编码，而较不常用字符则使用较长的编码方式。
"""
from __future__ import annotations
from burrows_wheeler import bwt_transform, reverse_bwt


class Letter:
    def __init__(self, letter: str, freq: int):
        self.letter: str = letter
        self.freq: int = freq
        self.bitstring: dict[str, str] = {}

    def __repr__(self) -> str:
        return f"{self.letter}:{self.freq}"


class TreeNode:
    def __init__(self, freq: int, left: Letter | TreeNode, right: Letter | TreeNode):
        self.freq: int = freq
        self.left: Letter | TreeNode = left
        self.right: Letter | TreeNode = right


class HuffmanDict:
    Huf_encode: list
    Huf_letters: list


def huffman_encode(raw_file_list: list) -> HuffmanDict:
    """ 哈夫曼编码压缩文件
        输入值：
            raw_file_list: 字符串列表

        返回值：
            返回HuffmanDict类
            HuffmanDict[Huf_encode]: 经过huffman编码处理的字符串
            HuffmanDict[Huf_letters]: huffman编码表

        示例：
            # raw_file_list = ["a", "a", "a", "a", "d", "s", "s", "_", "c", "_", "_", "a", "a"]
            # Huf_encode_result = huffman_encode(raw_file_list)
            # result:
                Huf_encode_result["Huf_encode"]:
                    ['0', '0', '0', '0', '1110', '110', '110', '10', '1111', '10', '10', '0', '0']
                Huf_encode_result["Huf_letters"]:
                    {'a': '0', '_': '10', 's': '110', 'd': '1110', 'c': '1111'}
    """
    letters_list = parse_file(raw_file_list)
    root = build_tree(letters_list)
    letters = {
        k: v for letter in traverse_tree(root, "") for k, v in letter.bitstring.items()
    }
    encode_list = []
    for c in raw_file_list:
        encode_list.append(letters[c])

    response: HuffmanDict = {"Huf_encode": encode_list, "Huf_letters": letters}
    return response


def huffman_decode(huf_file: HuffmanDict) -> list:
    """ 哈夫曼编码解压缩文件
        输入值：
            huf_file: HuffmanDict类
                HuffmanDict[Huf_encode]: 经过huffman编码处理的字符串
                HuffmanDict[Huf_letters]: huffman编码表

        返回值：
            返回字符串列表

        示例：
            # Huf_decode_result = huffman_decode(Huf_encode_result)
            # result: 'aaaadss_c__aa'
    """
    result = []
    for c in huf_file["Huf_encode"]:
        result.append(return_key(huf_file["Huf_letters"], c))
    return result


def bwt_huffman_encode(raw_file_list: list) -> HuffmanDict:
    """ BWT和哈夫曼编码压缩文件
        输入值：
            raw_file_list: 字符串列表

        返回值：
            返回HuffmanDict类
            HuffmanDict[Huf_encode]: 经过huffman编码处理的字符串
            HuffmanDict[Huf_letters]: huffman编码表
            HuffmanDict[Huf_letters]: bwt列表索引表

        示例：
            # raw_file_list = ["a", "a", "a", "a", "d", "s", "s", "_", "c", "_", "_", "a", "a"]
            # Bwt_Huf_encode_result = bwt_huffman_encode(raw_file_list)
            # result:
                Bwt_Huf_encode_result["Huf_encode"]:
                    ['1110', '10', '110', '10', '0', '0', '0', '0', '0', '10', '0', '110', '1111']
                Bwt_Huf_encode_result["Huf_letters"]:
                    {'a': '0', '_': '10', 's': '110', 'c': '1110', 'd': '1111'}
                Bwt_Huf_encode_result["idx_original_string"]:
                    5
    """
    bwt_result = bwt_transform(''.join(raw_file_list))
    temp=[]
    for ch in bwt_result["bwt_string"]:
        temp.append(ch)
    bwt_huffman_result = huffman_encode(temp)
    bwt_huffman_result["idx_original_string"] = bwt_result["idx_original_string"]
    return bwt_huffman_result


def bwt_huffman_decode(huf_file: HuffmanDict) -> str:
    """ BWT和哈夫曼编码解压缩文件
        输入值：
            返回HuffmanDict类
                HuffmanDict[Huf_encode]: 经过huffman编码处理的字符串
                HuffmanDict[Huf_letters]: huffman编码表
                HuffmanDict[Huf_letters]: bwt列表索引表

        返回值：
            返回字符串

        示例：
            # Bwt_Huf_decode_result = bwt_huffman_decode(Bwt_Huf_encode_result)
            # result: 'aaaadss_c__aa'
    """
    huf_decode = huffman_decode(huf_file)
    bwt_huffman_result = reverse_bwt("".join(huf_decode), huf_file["idx_original_string"])

    return bwt_huffman_result


def return_key(huf_letters, item):
    for key, value in huf_letters.items():
        if value == item:
            return key
    return "Key Not Found"


def parse_file(raw_file_list: list) -> list[Letter]:
    # 阅读文件，构建一个包含所有字母及其频率的dict，然后将dict转换为字母列表。
    chars: dict[str, int] = {}
    for c in raw_file_list:
        chars[c] = chars[c] + 1 if c in chars else 1
    return sorted((Letter(c, f) for c, f in chars.items()), key=lambda x: x.freq)


def build_tree(letters: list[Letter]) -> Letter | TreeNode:
    # 运行字母列表，并为霍夫曼树构建最小堆。
    response: list[Letter | TreeNode] = letters  # type: ignore
    while len(response) > 1:
        left = response.pop(0)
        right = response.pop(0)
        total_freq = left.freq + right.freq
        node = TreeNode(total_freq, left, right)
        response.append(node)
        response.sort(key=lambda x: x.freq)
    return response[0]


def traverse_tree(root: Letter | TreeNode, bitstring: str) -> list[Letter]:
    # 递归遍历霍夫曼树以设置每个字母的位串字典，并返回字母列表
    if isinstance(root, Letter):
        root.bitstring[root.letter] = bitstring
        return [root]
    treenode: TreeNode = root  # type: ignore
    letters = []
    letters += traverse_tree(treenode.left, bitstring + "0")
    letters += traverse_tree(treenode.right, bitstring + "1")
    return letters


if __name__ == "__main__":
    file_path = "./README.md"
    raw_file_list = []
    with open(file_path) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            raw_file_list.append(c)

    raw_file_list = ["a", "a", "a", "a", "d", "s", "s", "_", "c", "_", "_", "a", "a"]
    # Huffman编码压缩
    Huf_encode_result = huffman_encode(raw_file_list)
    print("huffman编码后: \n", Huf_encode_result["Huf_encode"])
    print("huffman编码索引表: \n", Huf_encode_result["Huf_letters"])

    # Huffman编码解压缩
    Huf_decode_result = huffman_decode(Huf_encode_result)
    print("huffman解码后: \n", "".join(Huf_decode_result))

    # BWT和Huffman编码后压缩
    Bwt_Huf_encode_result = bwt_huffman_encode(raw_file_list)
    print("bwt_huffman编码后: \n", Bwt_Huf_encode_result["Huf_encode"])
    print("bwt_huffman编码索引表: \n", Bwt_Huf_encode_result["Huf_letters"])
    print("bwt_列表索引表: \n", Bwt_Huf_encode_result["idx_original_string"])

    # BWT和Huffman编码后解压缩
    Bwt_Huf_decode_result = bwt_huffman_decode(Bwt_Huf_encode_result)
    print("bwt_huffman解码后: \n", Bwt_Huf_decode_result)
