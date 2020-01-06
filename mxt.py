from spectral import *
import os
import numpy as np
import cv2


def classifier_generate(img, gt, choice):
    img = open_image(img).load()
    gt1 = cv2.imread(gt)
    gt = np.asarray(gt1[:, :, 0])
    (m, n) = gt.shape
    for i in range(m):
        for j in range(n):
            if gt[i, j] < 127:
                gt[i, j] = 10
            else:
                gt[i, j] = 255

    classes = create_training_classes(img, gt)
    if choice == 0:
        gmlc = GaussianClassifier(classes)
    else:
        gmlc = MahalanobisDistanceClassifier(classes)
    return gmlc


def imgClass(imgxway, gtxway, file_dir, out_dir=None, k=0):  # k = 0:GaussianClassifier 1:MahalanobisDistanceClassifier
    if out_dir is None:
        out_dir = file_dir
    gmlc = classifier_generate(imgxway, gtxway, k)
    for files in os.listdir(file_dir):
        # 当前文件夹所有文件
        if files.endswith('.hdr'):  # 判断是否以.hdr结尾
            file = file_dir + '\\' + files
            img2 = open_image(file).load()
            clmap = gmlc.classify_image(img2)
            (filename, extension) = os.path.splitext(files)
            outputway = out_dir + '\\{a}.jpg'.format(a=filename)
            save_rgb(outputway, clmap)


def math(s1, s2):
    s = s1/s2
    return s


def imgprocess(file_dir, out_dir, blankend):       # hdr中data type = 5 interleave = bip
    for files in os.listdir(file_dir):
        # 当前文件夹所有文件
        if files.endswith(blankend):   # 判断是否以.hdr结尾
            file = file_dir + '\\' + files
            blank = open_image(file)
            blank = blank[:, :, :]
            imgblank = np.asarray(blank, dtype=float)

    count = 1
    for files in os.listdir(file_dir):
        if files.endswith('.hdr'):  # 判断是否以.hdr结尾
            file = file_dir + '\\' + files
            ori = open_image(file)
            img = ori[:, :, :]
            img = np.asarray(img, dtype=float)
            (filename, extension) = os.path.splitext(files)
            pcdata = math(img, imgblank)
            rawfile = out_dir + '\\' + filename + '.raw'
            pcdata.tofile(rawfile)
            print('pre image ' + str(count))
            count = count + 1


def generateHDR(file_dir, out_dir):
    rename_file(file_dir, '.hdr', '.txt')
    for files in os.listdir(file_dir):
        if files.endswith('.txt'):
            file = file_dir + '\\' + files
            f = open(file, "r+")   # 设置文件对象
            new_stus = ''
            for i in f:
                if i == 'data type = 12\n':
                    i = 'data type = 5\n'
                    new_stus = new_stus + i
                elif i == 'interleave = bsq\n':
                    i = 'interleave = bip\n'
                    new_stus = new_stus + i
                elif i == 'wavelength units = Unknown\n':
                    i = 'wavelength units = Nanometers\n'
                    new_stus = new_stus + i
                else:
                    new_stus = new_stus + i
            f.close()
            full_path = out_dir + '\\' + files
            file = open(full_path, 'w')
            file.write(new_stus)
            file.close()
    rename_file(out_dir, ".txt", ".hdr")
    rename_file(file_dir, ".txt", ".hdr")


def rename_file(file_dir, x, y):   # change x to y
    for files in os.listdir(file_dir):
        portion = os.path.splitext(files)
        # 如果后缀是x
        if portion[1] == x:
            # 重新组合文件名和后缀名
            file = file_dir + '\\' + files
            newname = file_dir + '\\' + portion[0] + y
            os.rename(file, newname)


def imgResize(file_dir, out_dir):
    for files in os.listdir(file_dir):
        # 当前文件夹所有文件
        if files.endswith('.jpg'):  # 判断是否以.jpg结尾
            file = file_dir + '\\' + files
            imgOri = cv2.imread(file)
            size = (1024, 1024)
            result = cv2.resize(imgOri, size, interpolation=cv2.INTER_AREA)
            (filename, extension) = os.path.splitext(files)
            outputway = out_dir + '//' + filename + '.jpg'
            cv2.imwrite(outputway, result)