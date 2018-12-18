import sys

import cv2
from matplotlib import pyplot as plt


ESC = 0


def make_image_gray(cv_image):
    """Return grayscale image"""
    return cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)


def main(image_path):
    splitted = image_path.split('.')
    base_name, ext = '.'.join(splitted[:-1]), splitted[-1]
    image = cv2.imread(image_path)
    gray = make_image_gray(image)
    plt.hist(gray.ravel(),256,[0,256])
    plt.show()
    cv2.imwrite(base_name + "_gray." + ext, gray)

    cv2.imshow("Original", image)
    cv2.imshow("Gray", gray)
    cv2.waitKey(ESC)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '--help':
        print("Usage: gray.py path_to_image")
    else:
        main(sys.argv[1])
