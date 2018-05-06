import glob
import os
import pickle
import shutil
import time
from config import config
import model
import util

# 清空并创建临时文件夹
if os.path.exists("screenshot"):
    shutil.rmtree("screenshot")
if os.path.exists("singlechar"):
    shutil.rmtree("singlechar")
os.mkdir("screenshot")
os.mkdir("singlechar")

# 输出程序标题
print("-" * 72)
print("{0}   _____  _____  _______  ____   _____    ____   _       _\n{0}  / ____||_   _||__   __|/ __ \\ |  __ \\  / __ \\ | |     | |\n{0} | |  __   | |     | |  | |  | || |  | || |  | || |     | |\n{0} | | |_ |  | |     | |  | |  | || |  | || |  | || |     | |\n{0} | |__| | _| |_    | |  | |__| || |__| || |__| || |____ | |____ \n{0}  \\_____||_____|   |_|   \\____/ |_____/  \\____/ |______||______|\n".format(" " * 4))
print("{}加减小游戏抓娃娃助手".format(" " * 26))
print("{}1.1.0.20180506".format(" " * 29))
print("-" * 72)
# 训练逻辑回归模型
if not os.path.exists("lr.pickle"):
    model.dumpModel()
# 加载逻辑回归模型
with open("lr.pickle", "rb") as fr:
    lr = pickle.load(fr)
print("请确保游戏画面位于[{}, {}]，大小 {}×{}\n".format(config["projection_x"], config["projection_y"], config["projection_width"], config["projection_height"]))

while True:
    debug = input("准备好后按回车键开始游戏 (共{}题)：".format(config["question_count"]))
    preRes = "" # 保存上次表达式，防止无效点击
    count = 1 # 有效迭代轮数
    time_start = time.time()
    while count <= config["question_count"]:
        time_end = time.time()
        if time_end - time_start < 3:
            time.sleep(0.1)
            for i in glob.glob(os.path.join("singlechar", str(count).zfill(2) + "_*.png")):
                os.remove(i)
            img = util.shotScreen("screenshot/%s.png" %str(count).zfill(2))
            res = util.getResult(lr, img, "%s.png" %str(count).zfill(2))
            if res != preRes and res != "":
                time_start = time.time()
                try:
                    print("第{}题: {} ({})".format(str(count).zfill(2), res.replace("==", "="), eval(res)))
                except:
                    print("第{}题: {} (Error)".format(str(count).zfill(2), res.replace("==", "=")))
                else:
                    if debug == "":
                        if eval(res):
                            util.tapScreen(config["tap_true_x"], config["tap_y"])
                        else:
                            util.tapScreen(config["tap_false_x"], config["tap_y"])
                preRes = res
                count += 1
            if count > config["question_count"]:
                print("\n游戏成功完成，去领取娃娃吧！\n")
        else:
            print("\n游戏失败了，祝下次好运！\n")
            break
