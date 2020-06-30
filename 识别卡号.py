import cv2
import matplotlib.pyplot as plt

# 信用卡的位置
# predict_card = "data/card.png"
predict_card = "data/huifengzhongg.png"
# 模板的位置
template = "data/tmp.png"


# 定义cv2展示函数
def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 对框进行排序
def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]  # 用一个最小的矩形，把找到的形状包起来x,y,h,w
    # (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
    #                                     key=lambda b: b[1][i], reverse=reverse))
    a = zip(cnts, boundingBoxes)
    (cnts, boundingBoxes) = zip(*sorted(a, key=lambda b: b[1][i], reverse=reverse))

    return cnts, boundingBoxes


img = cv2.imread(template)
ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, refCnts, -1, (0, 255, 0), 3)
refCnts = sort_contours(refCnts, method="left-to-right")[0]
