import cv2
import numpy as np
import os
from pymouse import PyMouse
import random
import win32gui, win32ui, win32con
from config import config

def cropImg(img):
    """裁剪原始截图"""
    height = img.shape[0]
    return img[int(config["exp_area_top_rate"] * height):int(config["exp_area_bottom_rate"] * height), :]

def binaryImg(img):
    """二值化图片"""
    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    return img

def cropAgain(img):
    """再次裁剪"""
    height = img.shape[0]
    img1 = img[0:int(0.5 * height), :]
    img2 = img[int(0.5 * height):height, :]
    return img1, img2

def cutImg(img, filename):
    """水平分割图片"""
    sum_list = np.array(img).sum(axis=0)
    start_index = -1
    res = []
    names = []
    index = 0
    for sum in sum_list:
        if sum > 255 * 4:
            if start_index == -1:
                start_index = index
        else:
            if start_index != -1:
                sigleCharWidth = config["single_char_width"]
                # 防止分割错误，判断字符宽度
                if index - start_index > sigleCharWidth * 2:
                    res.append((start_index, start_index + (index - start_index) // 2))
                    res.append((start_index + (index - start_index) // 2, index))
                else:
                    res.append((start_index, index))
                start_index = -1
        index += 1
    count = 0
    for single_char in res:
        start = single_char[0]
        end = single_char[1]
        sub_img = img[:, start:end]
        sub_img = cv2.resize(
            sub_img, (120, 240), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("singlechar/%s_%d.png" % (filename, count), sub_img)
        names.append("%s_%d.png" % (filename, count))
        count += 1
    return names

def vcutImg(img, filename):
    """竖直方向切割图片"""
    sum_list = np.array(img).sum(axis=1)
    start_index = -1
    end = -1
    index = 0
    for sum in sum_list:
        if sum > 255 * 2:
            start_index = index
            break
        index += 1
    for i in range(1, len(sum_list) + 1):
        if sum_list[-i] > 255 * 2:
            end = len(sum_list) + 1 - i
            break
    img = img[start_index:end, :]
    img = cv2.resize(img, (30, 60), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("singlechar/%s" % filename, img)
    return img

def getAll(img, filename):
    """封装对图片的全部操作"""
    img1, img2 = cropAgain(binaryImg(cropImg(img)))
    names = cutImg(img1, filename.split(".")[0] + "_1") + cutImg(img2, filename.split(".")[0] + "_2")
    return names

def getResult(lr, img, filename):
    """识别图片数据并获取表达式"""
    res = []
    filenames = getAll(img, filename)
    for filename in filenames:
        img = np.array(vcutImg(cv2.imread(os.path.join("singlechar", filename), 0), filename)).reshape(1, -1)
        img[img == 255] = 1
        y_hat = lr.predict(img)[0]
        if y_hat == 10:
            res.append("+")
        elif y_hat == 11:
            res.append("-")
        elif y_hat == 12:
            res.append("==")
        else:
            res.append(str(y_hat))
    res = "".join(res)
    return res

def shotScreen(filename):
    """使用windows原生API截屏"""
    width = config["projection_width"]
    height = config["projection_height"]
    mfcDC = win32ui.CreateDCFromHandle(win32gui.GetWindowDC(0))
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (config["projection_x"], config["projection_y"]), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    return cv2.imread(filename, 0)

def tapScreen(x, y):
    """模拟鼠标点击"""
    PyMouse().click(int(x) + random.randint(-10, 10), int(y) + random.randint(-10, 10), 1)
