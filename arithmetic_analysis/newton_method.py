from typing import Callable


def newton(
    function: Callable[[float], float],
    derivative: Callable[[float], float],
    starting_int: int,
) -> float:
    """ 牛顿法解方程，形式为 f(x)=0
        输入值：
            function：原函数
            derivative：函数一阶导数
            starting_int：搜索初始点

        返回值：
            返回方程的解，即满足要求的x值

        示例：
            newton(lambda x: x ** 3 - 2 * x - 5, lambda x: 3 * x ** 2 - 2, 3)
            result: 2.0945514815423474
        """

    prev_guess = float(starting_int)
    while True:
        try:
            next_guess = prev_guess - function(prev_guess) / derivative(prev_guess)
        except ZeroDivisionError:
            raise ZeroDivisionError("Could not find root") from None
        if abs(prev_guess - next_guess) < 10**-5:
            return next_guess
        prev_guess = next_guess


def function(x: float) -> float:
    """
    function: 原函数
    """
    return (x**3) - (2 * x) - 5


def derivative(x: float) -> float:
    """
    derivative: 原函数的一阶导数
    """
    return 3 * (x**2) - 2


if __name__ == "__main__":
    print(newton(function, derivative, 3))
