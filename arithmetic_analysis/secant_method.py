from math import exp
from typing import Callable


def secant_method(func: Callable[[float], float],lower_bound: float, upper_bound: float, repeats: int) -> float:
    """ 割线法解方程，形式为 f(x)=0
            输入值：
                Func：原函数
                lower_bound：搜索空间下限
                upper_bound：搜索空间上限
                repeats: 迭代次数

            返回值：
                返回方程的解，即满足要求的x值

            示例：
                secant_method(func, 1, 3, 2)
                result: 0.2139409276214589
            """

    x0 = lower_bound
    x1 = upper_bound
    for _ in range(0, repeats):
        x0, x1 = x1, x1 - (func(x1) * (x1 - x0)) / (func(x1) - func(x0))
    return x1


def func(x: float) -> float:
    """
    Func: 原函数
    """
    return 8 * x - 2 * exp(-x)


if __name__ == "__main__":
    print(secant_method(func, 1, 3, 2))
