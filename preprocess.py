from spectral import *
from spectral import BIP
import spectral.io.envi as envi
import os
import numpy as np
import time


def imgprocess(file_dir):   # hdr中data type = 5 interleave = bip

    for files in os.listdir(file_dir):
        # 当前文件夹所有文件
        if files.endswith('blank-10358-4349.hdr'):   # 判断是否以.hdr结尾
            file = file_dir + '\\' + files
            blank = open_image(file)
            blank = blank[:, :, :]
            imgblank = np.asarray(blank, dtype=float)

    for files in os.listdir(file_dir):
        if files.endswith('.hdr'):  # 判断是否以.hdr结尾
            file = file_dir + '\\' + files
            ori = open_image(file)
            img = ori[:, :, :]
            img = np.asarray(img, dtype=float)
            (filename, extension) = os.path.splitext(files)
            pcdata = img / imgblank
            rawfile = file_dir + '\\pre\\' + filename + '.raw'
            pcdata.tofile(rawfile)


def generateHDR(file_dir):
    t = 0.05
    for files in os.listdir(file_dir):
        portion = os.path.splitext(files)
        # 如果后缀是.dat
        if portion[1] == ".hdr":
            # 重新组合文件名和后缀名
            file = file_dir + '\\' + files
            newname = file_dir + '\\' + portion[0] + ".txt"
            os.rename(file, newname)
        time.sleep(t)
        f = open(newname, "r+")   # 设置文件对象
        new_stus = ''
        for i in f:
            if i == 'data type = 12\n':
                i = 'data type = 5\n'
                # new_stus.append(i)
                new_stus = new_stus + i
            elif i == 'interleave = bsq\n':
                i = 'interleave = bip\n'
                # new_stus.append(i)
                new_stus = new_stus + i
            else:
                # new_stus.append(i)
                new_stus = new_stus + i
        f.truncate()
        f.close()
        full_path = file_dir + '\\pre\\' + portion[0] + '.txt'
        file = open(full_path, 'w')
        file.write(new_stus)
        file.close()
        new_file_dir = file_dir + '\\pre'
    time.sleep(t)
    for files in os.listdir(new_file_dir):
        portion = os.path.splitext(files)
        if portion[1] == ".txt":
            # 重新组合文件名和后缀名
            file = new_file_dir + '\\' + files
            newname = new_file_dir + '\\' + portion[0] + ".hdr"
            os.rename(file, newname)


if __name__ == '__main__':
    imgWay = r'E:\HE+CAM5\HE_CAM52_mono_roi1'
    imgprocess(imgWay)
    generateHDR(imgWay)
