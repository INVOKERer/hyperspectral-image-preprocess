import cv2

img_way = r'E:\HE+CAM5\PreproEasy\rgb-down\roi1_SVMcvt.jpg'
out_way = r'E:\HE+CAM5\PreproEasy\rgb-down\roi1_SVMcvtnot.jpg'
img = cv2.imread(img_way)

res = cv2.bitwise_not(img)
cv2.imwrite(out_way, res)
