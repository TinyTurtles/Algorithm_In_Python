from typing import Callable


# 二分法解方程
def bisection(function: Callable[[float], float], a: float, b: float) -> float:
    """ 二分法解方程，形式为 f(x)=0
    输入值：
        function：lambda x: f(x)
        a：搜索空间的下限
        b：搜索空间的上限

    返回值：
        返回方程的解，即满足要求的x值

    示例：
        bisection(lambda x: x ** 3 - 1, -5, 5)
        result：1.0000000149011612
    """

    start: float = a
    end: float = b
    if function(a) == 0:  # 如果a或者b是方程的一个根
        return a
    elif function(b) == 0:
        return b
    elif (
            function(a) * function(b) > 0
    ):
        # 此算法寻不到根
        raise ValueError("could not find root in given interval.")
    else:
        mid: float = start + (end - start) / 2.0
        while abs(start - mid) > 10 ** -7:  # until precisely equals to 10^-7
            if function(mid) == 0:
                return mid
            elif function(mid) * function(start) < 0:
                end = mid
            else:
                start = mid
            mid = start + (end - start) / 2.0
        return mid


if __name__ == "__main__":
    # 使用bisection查找[a，b]中函数变为0的位置
    # print(bisection(lambda x: x ** 3 - 1, -5, 5))
    print(bisection(lambda x: x ** 3 - 2 * x - 5, -5, 5))
