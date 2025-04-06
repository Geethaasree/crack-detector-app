import cv2
import math
import numpy as np
import scipy.ndimage

def orientated_non_max_suppression(mag, ang):
    ang_quant = np.round(ang / (np.pi/4)) % 4
    winE = np.array([[0, 0, 0],[1, 1, 1], [0, 0, 0]])
    winSE = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    winS = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    winSW = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

    magE = non_max_suppression(mag, winE)
    magSE = non_max_suppression(mag, winSE)
    magS = non_max_suppression(mag, winS)
    magSW = non_max_suppression(mag, winSW)

    mag[ang_quant == 0] = magE[ang_quant == 0]
    mag[ang_quant == 1] = magSE[ang_quant == 1]
    mag[ang_quant == 2] = magS[ang_quant == 2]
    mag[ang_quant == 3] = magSW[ang_quant == 3]
    return mag

def non_max_suppression(data, win):
    data_max = scipy.ndimage.maximum_filter(data, footprint=win, mode='constant')
    data_max[data != data_max] = 0
    return data_max

def process_image(input_path, output_path):
    gray_image = cv2.imread(input_path, 0)

    with_nmsup = True
    fudgefactor = 1.3
    sigma = 21
    kernel = 2 * math.ceil(2 * sigma) + 1

    gray_image = gray_image / 255.0
    blur = cv2.GaussianBlur(gray_image, (kernel, kernel), sigma)
    gray_image = cv2.subtract(gray_image, blur)

    sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.hypot(sobelx, sobely)
    ang = np.arctan2(sobely, sobelx)

    threshold = 4 * fudgefactor * np.mean(mag)
    mag[mag < threshold] = 0

    if with_nmsup:
        mag = orientated_non_max_suppression(mag, ang)
        mag[mag > 0] = 255
        mag = mag.astype(np.uint8)

    kernel = np.ones((5,5), np.uint8)
    result = cv2.morphologyEx(mag, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(output_path, result)
