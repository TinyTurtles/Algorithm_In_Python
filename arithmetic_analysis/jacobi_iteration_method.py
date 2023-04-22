from __future__ import annotations

import numpy as np
from numpy import float64
from numpy.typing import NDArray


# 求解线性方程组的方法
def jacobi_iteration_method(coefficient_matrix: NDArray[float64], constant_matrix: NDArray[float64],
                            init_val: list[float], iterations: int) -> list[float]:
    """ Jacobi迭代法解严格对角占优的线性方程组(A*X=B)
        输入值：
            coefficient_matrix：系数矩阵A
            constant_matrix：结果矩阵B
            init_val: 迭代初始值X0
            iterations: 迭代次数

        返回值：
            返回方程的解，即满足要求的x1,x2....

        示例：
            Examples:(coefficient*X=constant)
                4x1 +  1*x2 +  1*x3 =  2
                1*x1 + 5*x2 + 2*x3 = -6
                1*x1 + 2*x2 + 4*x3 = -4

            coefficient=[[4, 1, 1],
                         [1, 5, 2],
                         [1, 2, 4]]
            constant=[[2],
                      [-6],
                      [-4]]
            init_val = [0.5, -0.5, -0.5]
            iterations = 3
            jacobi_iteration_method(coefficient, constant, init_val, iterations)
            the result：[0.909375, -1.14375, -0.7484375]
    """

    rows1, cols1 = coefficient_matrix.shape
    rows2, cols2 = constant_matrix.shape

    if rows1 != cols1:
        raise ValueError(
            f"Coefficient matrix dimensions must be nxn but received {rows1}x{cols1}"
        )

    if cols2 != 1:
        raise ValueError(f"Constant matrix must be nx1 but received {rows2}x{cols2}")

    if rows1 != rows2:
        raise ValueError(
            f"""Coefficient and constant matrices dimensions must be nxn and nx1 but
            received {rows1}x{cols1} and {rows2}x{cols2}"""
        )

    if len(init_val) != rows1:
        raise ValueError(
            f"""Number of initial values must be equal to number of rows in coefficient
            matrix but received {len(init_val)} and {rows1}"""
        )

    if iterations <= 0:
        raise ValueError("Iterations must be at least 1")

    table: NDArray[float64] = np.concatenate(
        (coefficient_matrix, constant_matrix), axis=1
    )

    rows, cols = table.shape

    strictly_diagonally_dominant(table)

    # 将整个矩阵迭代给定次数
    for _ in range(iterations):
        new_val = []
        for row in range(rows):
            temp = 0
            for col in range(cols):
                if col == row:
                    denom = table[row][col]
                elif col == cols - 1:
                    val = table[row][col]
                else:
                    temp += (-1) * table[row][col] * init_val[col]
            temp = (temp + val) / denom
            new_val.append(temp)
        init_val = new_val

    return [float(i) for i in new_val]


# 检查给定矩阵是否严格对角占优
def strictly_diagonally_dominant(table: NDArray[float64]) -> bool:
    rows, cols = table.shape

    is_diagonally_dominant = True

    for i in range(0, rows):
        total = 0
        for j in range(0, cols - 1):
            if i == j:
                continue
            else:
                total += table[i][j]

        if table[i][i] <= total:
            raise ValueError("Coefficient matrix is not strictly diagonally dominant")

    return is_diagonally_dominant


# 测试案例
if __name__ == "__main__":
    coefficient = np.array([[4, 1, 1],
                            [1, 5, 2],
                            [1, 2, 4]])
    constant = np.array([[2],
                         [-6],
                         [-4]])
    init_val = [0.5, -0.5, -0.5]
    iterations = 3
    print(jacobi_iteration_method(coefficient, constant, init_val, iterations))
