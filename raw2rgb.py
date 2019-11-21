from spectral import *
import spectral.io.envi as envi
import os


def imgLoad(file_dir):
    for files in os.listdir(file_dir):
        #当前文件夹所有文件
        if files.endswith('.hdr'):# 判断是否以.hdr结尾
            file = file_dir + '\\' + files
            imgOri = envi.open(file)
            rgb = get_rgb(imgOri, bands=(25, 13, 3), stretch=((0.02, 0.98), (0.02, 0.98), (0.02, 0.98)))
            (filename, extension) = os.path.splitext(files)
            outputway = r'E:\HE+CAM5\HE_CAM52_mono_roi1\RGB\{a}.jpg'.format(a=filename)
            save_rgb(outputway, rgb)


if __name__ == '__main__':
    imgWay = r'E:\HE+CAM5\HE_CAM52_mono_roi1\preprocess'
    img = imgLoad(imgWay)


