"""
    Lempel-Ziv算法是一种被广泛应用于数据压缩领域的算法。
    该算法利用已经出现过的模式来进行数据压缩，将输入数据划分为不重复的子串，
    并以它们第一次出现时的索引位置及其长度作为表示。
"""
from __future__ import annotations
import math
import os
import sys


def lz_compress(source_path: str) -> None:
    """ LZ压缩文件
        输入值：
            source_path: 需压缩的文件路径

        返回值：
            无（已在需压缩的文件路径生成了压缩文件）

        示例：
            # lz_compress("./README.md")
            # result:
                "./README_compressed.ziv"
    """
    # 读取源文件，对其进行压缩，并将压缩后的结果写入目标文件
    path_list = source_path.split(".")
    path_list[-2] = path_list[-2] + "_compressed"
    path_list[-1] = "ziv"
    destination_path = ".".join(path_list)
    data_bits = read_file_binary(source_path)
    compressed = compress_data(data_bits)
    compressed = add_file_length(source_path, compressed)
    write_file_binary(destination_path, compressed)
    print("压缩成功,路径:",destination_path)


def lz_decompress(source_path: str, file_format: str) -> None:
    """ LZ解压缩文件
        输入值：
            source_path: 需解压缩的文件路径

        返回值：
            无（已在需解压缩的文件路径生成了解压缩文件）

        示例：
            # lz_decompress("README_compressed.ziv", "md")
            # result:
                "./README_compressed_decompressed.md"
    """
    path_list = source_path.split(".")
    path_list[-2] = path_list[-2] + "_decompressed"
    path_list[-1] = file_format
    destination_path = ".".join(path_list)
    data_bits = read_file_binary(source_path)
    data_bits = remove_prefix(data_bits)
    decompressed = decompress_data(data_bits)
    write_file_binary(destination_path, decompressed)


def read_file_binary(file_path: str) -> str:
    # 以字节形式读取给定文件，并以长字符串形式返回
    result = ""
    try:
        with open(file_path, "rb") as binary_file:
            data = binary_file.read()
        for dat in data:
            curr_byte = f"{dat:08b}"
            result += curr_byte
        return result
    except OSError:
        print("File not accessible")
        sys.exit()


def remove_prefix(data_bits: str) -> str:
    """
    Removes size prefix, that compressed file should have
    Returns the result
    """
    counter = 0
    for letter in data_bits:
        if letter == "1":
            break
        counter += 1

    data_bits = data_bits[counter:]
    data_bits = data_bits[counter + 1 :]
    return data_bits


def decompress_data(data_bits: str) -> str:
    """
    Decompresses given data_bits using Lempel–Ziv–Welch compression algorithm
    and returns the result as a string
    """
    lexicon = {"0": "0", "1": "1"}
    result, curr_string = "", ""
    index = len(lexicon)

    for i in range(len(data_bits)):
        curr_string += data_bits[i]
        if curr_string not in lexicon:
            continue

        last_match_id = lexicon[curr_string]
        result += last_match_id
        lexicon[curr_string] = last_match_id + "0"

        if math.log2(index).is_integer():
            new_lex = {}
            for curr_key in list(lexicon):
                new_lex["0" + curr_key] = lexicon.pop(curr_key)
            lexicon = new_lex

        lexicon[bin(index)[2:]] = last_match_id + "1"
        index += 1
        curr_string = ""
    return result


def add_key_to_lexicon(
    lexicon: dict[str, str], curr_string: str, index: int, last_match_id: str
) -> None:
    # 向词典中添加新字符串（curr_string+“0”，curr_string+“1”）
    lexicon.pop(curr_string)
    lexicon[curr_string + "0"] = last_match_id

    if math.log2(index).is_integer():
        for curr_key in lexicon:
            lexicon[curr_key] = "0" + lexicon[curr_key]

    lexicon[curr_string + "1"] = bin(index)[2:]


def compress_data(data_bits: str) -> str:
    # 使用Lempel–Ziv–Welch压缩算法压缩给定的数据比特，并将结果作为字符串返回
    lexicon = {"0": "0", "1": "1"}
    result, curr_string = "", ""
    index = len(lexicon)

    for i in range(len(data_bits)):
        curr_string += data_bits[i]
        if curr_string not in lexicon:
            continue

        last_match_id = lexicon[curr_string]
        result += last_match_id
        add_key_to_lexicon(lexicon, curr_string, index, last_match_id)
        index += 1
        curr_string = ""

    while curr_string != "" and curr_string not in lexicon:
        curr_string += "0"

    if curr_string != "":
        last_match_id = lexicon[curr_string]
        result += last_match_id

    return result


def add_file_length(source_path: str, compressed: str) -> str:
    # 在压缩字符串的前面添加给定文件的长度（使用Elias gamma编码）
    file_length = os.path.getsize(source_path)
    file_length_binary = bin(file_length)[2:]
    length_length = len(file_length_binary)

    return "0" * (length_length - 1) + file_length_binary + compressed


def write_file_binary(file_path: str, to_write: str) -> None:
    # 将给定的字符串写入指定文件中
    byte_length = 8
    try:
        with open(file_path, "wb") as opened_file:
            result_byte_array = [
                to_write[i : i + byte_length]
                for i in range(0, len(to_write), byte_length)
            ]

            if len(result_byte_array[-1]) % byte_length == 0:
                result_byte_array.append("10000000")
            else:
                result_byte_array[-1] += "1" + "0" * (
                    byte_length - len(result_byte_array[-1]) - 1
                )

            for elem in result_byte_array:
                opened_file.write(int(elem, 2).to_bytes(1, byteorder="big"))
    except OSError:
        print("File not accessible")
        sys.exit()


if __name__ == "__main__":

    # 采用LZ算法压缩文件
    raw_filepath = "./README.md"
    lz_compress(raw_filepath)

    # 采用LZ算法解压缩文件
    raw_filepath = "README_compressed.ziv"
    file_format = "md"
    lz_decompress(raw_filepath, file_format)
