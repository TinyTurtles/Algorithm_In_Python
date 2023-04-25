"""
    BWT（Burrows-Wheeler Transform）算法是一种数据压缩算法，
    通过对数据进行变换，使得数据中的重复模式得到更好的压缩。
    BWT算法的基本思想是将原始数据转换为一种更易于压缩的形式，
    然后再使用其他压缩算法进行压缩。
"""
from __future__ import annotations


class BWTTransformDict:
    bwt_string: str
    idx_original_string: int


def bwt_transform(s: str) -> BWTTransformDict:
    """ 将字符串采用BWT算法进行变换
        输入值：
            s：需要变换的字符串

        返回值：
            返回BWTTransformDict类
            BWTTransformDict[bwt_string]: 经过BWT算法处理的字符串
            BWTTransformDict[idx_original_string]: 列表索引

        示例：
            bwt_transform("a_asa_da_casa")
            result: {'bwt_string': 'aaaadss_c__aa', 'idx_original_string': 3}
    """
    if not isinstance(s, str):
        raise TypeError("The parameter s type must be str.")
    if not s:
        raise ValueError("The parameter s must not be empty.")

    rotations = all_rotations(s)
    rotations.sort()  # sort the list of rotations in alphabetically order
    # make a string composed of the last char of each rotation
    response: BWTTransformDict = {
        "bwt_string": "".join([word[-1] for word in rotations]),
        "idx_original_string": rotations.index(s),
    }
    return response


def reverse_bwt(bwt_string: str, idx_original_string: int) -> str:
    """ 将经BWT算法变换的字符串还原
        输入值：
            BWTTransformDict[bwt_string]: 经过BWT算法变换的字符串
            BWTTransformDict[idx_original_string]: 列表索引

        返回值：
            返回还原后的字符串

        示例：
            reverse_bwt("aaaadss_c__aa", 3)
            result: 'a_asa_da_casa'
    """
    if not isinstance(bwt_string, str):
        raise TypeError("The parameter bwt_string type must be str.")
    if not bwt_string:
        raise ValueError("The parameter bwt_string must not be empty.")
    try:
        idx_original_string = int(idx_original_string)
    except ValueError:
        raise TypeError(
            "The parameter idx_original_string type must be int or passive"
            " of cast to int."
        )
    if idx_original_string < 0:
        raise ValueError("The parameter idx_original_string must not be lower than 0.")
    if idx_original_string >= len(bwt_string):
        raise ValueError(
            "The parameter idx_original_string must be lower than" " len(bwt_string)."
        )

    ordered_rotations = [""] * len(bwt_string)
    for _ in range(len(bwt_string)):
        for i in range(len(bwt_string)):
            ordered_rotations[i] = bwt_string[i] + ordered_rotations[i]
        ordered_rotations.sort()
    return ordered_rotations[idx_original_string]


def all_rotations(s: str) -> list[str]:
    if not isinstance(s, str):
        raise TypeError("The parameter s type must be str.")

    return [s[i:] + s[:i] for i in range(len(s))]


if __name__ == "__main__":
    entry_msg = "a_asa_da_casa"
    s = entry_msg.strip()
    bwt_result = bwt_transform(s)
    print(bwt_result)
    original_string = reverse_bwt(bwt_result["bwt_string"], bwt_result["idx_original_string"])
    print(original_string)
