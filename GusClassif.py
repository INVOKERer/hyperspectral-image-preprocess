from spectral import *
import cv2
import numpy as np
import os


def classify():
    img = open_image(r'E:\HE+CAM5\PreproEasy\HE_CAM52_mono_E_roi1_prePro.hdr').load()
    gt1 = cv2.imread(r'E:\HE+CAM5\PreproEasy\rgb-down\roi1_SVM.jpg')
    gt = np.asarray(gt1[:, :, 0])
    (m, n) = gt.shape
    for i in range(m):
        for j in range(n):
            if gt[i, j] < 127:
                gt[i, j] = 10
            else:
                gt[i, j] = 255

    classes = create_training_classes(img, gt)
    gmlc = GaussianClassifier(classes)
    return gmlc


def imgClass(file_dir):
    gmlc = classify()
    for files in os.listdir(file_dir):
        # 当前文件夹所有文件
        if files.endswith('.hdr'):  # 判断是否以.hdr结尾
            file = file_dir + '\\' + files
            img2 = open_image(file).load()
            clmap = gmlc.classify_image(img2)
            (filename, extension) = os.path.splitext(files)
            outputway = r'E:\HE+CAM5\PreproEasy\rgb-down\testa\{a}.jpg'.format(a=filename)
            save_rgb(outputway, clmap)


if __name__ == '__main__':
    imgWay = r'E:\HE+CAM5\PreproEasy'
    img = imgClass(imgWay)

