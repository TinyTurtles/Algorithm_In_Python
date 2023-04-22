import numpy as np
from numpy import float64
from numpy.typing import NDArray


def gaussian_elimination(coefficients: NDArray[float], vector: NDArray[float]) -> NDArray[float]:
    """ 高斯消元法解线性方程组(A*X=B)
    输入值：
        coefficients：系数矩阵A
        vector：结果矩阵B

    返回值：
        返回方程的解，即满足要求的x1,x2....

    示例：
        Examples:(A*X=B)
            2*x1 + 2*x2 - 1*x3 = 5
            0*x1 - 2*x2 - 1*x3 = -7
            0*x1 + 0*x2 + 5*x3 = 15

        A=[[1, -4, -2],
           [5, 2, -2],
           [1, -1, 0]]
        B=[[-2],
           [-3],
           [4]]
        gaussian_elimination(A, B)
        the result：[[ 2.3 ]
                    [-1.7 ]
                    [ 5.55]]
    """

    # 检查系数是否为一个平方矩阵
    rows, columns = np.shape(coefficients)
    if rows != columns:
        return np.array((), dtype=float)

    # 增广矩阵
    augmented_mat: NDArray[float64] = np.concatenate((coefficients, vector), axis=1)
    augmented_mat = augmented_mat.astype("float64")

    # 缩放矩阵，使其保持三角形式
    for row in range(rows - 1):
        pivot = augmented_mat[row, row]
        for col in range(row + 1, columns):
            factor = augmented_mat[col, row] / pivot
            augmented_mat[col, :] -= factor * augmented_mat[row, :]

    x = retroactive_resolution(
        augmented_mat[:, 0:columns], augmented_mat[:, columns: columns + 1]
    )

    return x


def retroactive_resolution(coefficients: NDArray[float64], vector: NDArray[float64]) -> NDArray[float64]:
    rows, columns = np.shape(coefficients)

    x: NDArray[float64] = np.zeros((rows, 1), dtype=float)
    for row in reversed(range(rows)):
        total = 0
        for col in range(row + 1, columns):
            total += coefficients[row, col] * x[col]

        x[row, 0] = (vector[row] - total) / coefficients[row, row]

    return x


if __name__ == "__main__":
    """
    Examples:(A*X=B)
        2*x1 + 2*x2 - 1*x3 = 5        
        0*x1 - 2*x2 - 1*x3 = -7        
        0*x1 + 0*x2 + 5*x3 = 15
    """
    A=[[1, -4, -2],
       [5, 2, -2],
       [1, -1, 0]]
    B=[[-2],
       [-3],
       [4]]
    print(gaussian_elimination(A, B))
