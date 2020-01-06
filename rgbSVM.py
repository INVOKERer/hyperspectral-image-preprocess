# done
from sklearn import svm
import cv2
import numpy as np
import os
# import spectral.io.envi as envi
# import time


def classify(file_dir, hdr_dir, roi_dir1, roi_dir2, out_dir):
    # time_start = time.time()
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    img = cv2.imread(hdr_dir)
    m, n, l = img.shape
    k = m * n
    img_reshape = img.reshape((k, l))
    gt1 = cv2.imread(roi_dir1)
    gt = np.asarray(gt1[:, :, 0])
    gt1_flatten = gt.flatten()
    gt2 = cv2.imread(roi_dir2)
    gt2 = np.asarray(gt2[:, :, 0])
    gt2_flatten = gt2.flatten()
    label1 = 255
    label2 = 0
    count = 0
    for i in range(k):
        if gt1_flatten[i] > 127:
            if count == 0:
                label = np.array([label1])
                data = img_reshape[i, :]
                count = count + 1
            else:
                label = np.append(label, label1)
                data = np.vstack((data, img_reshape[i, :]))
                # data = np.concatenate((data, img_reshape[i, :]), axis=0)
                count = count + 1
            # print(count)
        elif gt2_flatten[i] > 127:
            if count == 0:
                label = np.array([label2])
                data = img_reshape[i, :]
                count = count + 1
            else:
                label = np.append(label, label2)
                data = np.vstack((data, img_reshape[i, :]))
                # data = np.concatenate((data, img_reshape[i, :]), axis=0)
                count = count + 1
    print('collect samples: ' + str(count))
    clf = svm.SVC(C=1, kernel='rbf', gamma='auto', decision_function_shape='ovr')
    clf.fit(data, label)
    # time_end = time.time()
    # print('totally cost', time_end-time_start)

    for files in os.listdir(file_dir):
        # 当前文件夹所有文件
        if files.endswith('.jpg'):  # 判断是否以结尾
            file = file_dir + '\\' + files
            img2 = cv2.imread(file)
            print('doing' + files)
            m, n, l = img2.shape
            k = m * n
            img2_reshape = img2.reshape((k, l))
            clmap = clf.predict(img2_reshape)
            res = clmap.reshape((m, n))
            (filename, extension) = os.path.splitext(files)
            outputway = out_dir + r'\{a}.jpg'.format(a=filename)
            cv2.imwrite(outputway, res)


if __name__ == '__main__':
    imgWay = r'E:\HE+CAM5\20191231\test'                                  # 需要分类的图像路径
    hdrWay = r'E:\HE+CAM5\20191231\roix.jpg'                 # 用于分类的图像路径
    roiWay1 = r'E:\HE+CAM5\test\1.jpg'                     # 用于分类的图像掩膜路径
    roiWay2 = r'E:\HE+CAM5\test\2.jpg'
    outWay = r'E:\HE+CAM5\test\testd'                   # 分类后的输出路径
    classify(imgWay, hdrWay, roiWay1, roiWay2, outWay)

