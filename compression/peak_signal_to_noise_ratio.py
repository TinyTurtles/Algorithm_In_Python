"""
    PSNR全称是Peak Signal-to-Noise Ratio，峰值信噪比。
    它是一种用于衡量压缩图像质量的方法，通常用于评估被压缩和解压缩后的图像与原始图像之间的差别。
"""
import math
import cv2
import numpy as np


def peak_signal_to_noise_ratio(original: float, contrast: float) -> float:
    """ 采用PSNR计算图像的压缩质量
        输入值：
            original：通过cv2.imread()读取的原始图像
            contrast: 通过cv2.imread()读取的压缩后图像

        返回值：
            返回PSNR值 （值越高压缩越无损）

        示例：
            # original2 = cv2.imread("./image_data/PSNR-example-base.png")
            # contrast2 = cv2.imread("./image_data/PSNR-example-comp-10.jpg")
            # PSNR_value = peak_signal_to_noise_ratio(original2, contrast2)
            # result: "31.53 dB"
    """
    pixel_max = 255.0
    mse = np.mean((original - contrast) ** 2)
    if mse == 0:
        return 100
    return 20 * math.log10(pixel_max / math.sqrt(mse))


if __name__ == "__main__":
    original2 = cv2.imread("./image_data/PSNR-example-base.png")
    contrast2 = cv2.imread("./image_data/PSNR-example-comp-10.jpg")
    PSNR_value = peak_signal_to_noise_ratio(original2, contrast2)
    print(f"PSNR: { PSNR_value } dB")