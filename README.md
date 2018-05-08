# 加减小游戏抓娃娃助手
使用 `Python` 开发的抓娃娃助手，兼容微信小游戏加减大师、加减王者，更多同类游戏可以自行修改配置文件适配。

## 运行效果截图
![](https://github.com/iflycn/doll/blob/master/ScreenGif.gif)

## 如何工作
1. 将手机屏幕映射到电脑
2. 首次运行时自动训练逻辑回归模型
3. 裁切出截图中的问题部分，使用机器学习数据识别问题
4. 判断出对错后自动点击对应回答

## 如何使用（Windows 系统）
### 安装 Vysor
1. `Vysor` 可以将手机屏幕实时映射到电脑，速度一流，很好的解决了该项目需要的速度问题。
2. 推荐安装 `Google Chrome` 应用版本，你可以在 Chrome 应用中搜索并安装 [Vysor](https://chrome.google.com/webstore/detail/vysorcom/kdphpklacmlhmooodiekhpbepcdlaghl)
### 设置你的手机
3. 开启开发者选项，打开 USB 调试，小米手机一并打开 USB 调试（安全设置）
4. 使用数据线连接手机，等待系统自动安装驱动完成
### 下载程序
5. 下载[加减小游戏抓娃娃助手压缩包](https://github.com/iflycn/doll/archive/master.zip)，解压到硬盘目录，例如 `D:\doll-master`
6. 修改文件 `config.py` 中的配置项以适应你的使用环境。你也可以尝试使用默认项，但你需要：将 `Vysor` 窗口置于桌面左上角，并调整窗口宽度为 310 PX
### 安装 Python
7. 从 [Python 官网](https://www.python.org/downloads)下载安装 `python3.6.5`
8. 电脑运行 `CMD`，输入命令 `pip3 install -r D:\doll-master\requirements.txt`，等待下载依赖包并安装完成
9. 如果下载依赖包过程中出错，重新输入命令 `pip3 install -r D:\doll-master\requirements.txt` 直到下载成功
### 开始使用
10. 手机进入微信小游戏加减大师界面
11. 电脑运行 `CMD`，依次输入命令 `D:`、`cd doll-master`、`python main.py`，根据程序提示操作即可

## 训练逻辑回归模型
* 因游戏字体不同的原因，你有可能需要重新训练逻辑回归模型，遵循以下训练步骤：
1. 在程序提示按回车键开始游戏时，输入 `debug` 并回车进入测试模式，这时程序仍将保存截图但不会自动答题，请手动完成尽可能多的答题
2. 在游戏结束后关闭程序，进入 `D:\doll-master\singlechar` 目录，正确的话，你会看到一些拆分好的单个字符样本，这些字符可能是 `+`、`-`、`=` 或者 `0-9` （如果截图不正确，一般是 `config.py` 中的配置项设置问题）
3. `D:\doll-master\trainchar` 目录下有 `+`、`-`、`=` 和 `0-9` 共 13 个文件夹，清空每个文件夹下的训练图片，但不要删除文件夹本身
4. 将步骤 2 中得到的单个字符样本放入对应的文件夹下，为保证训练效果，每个类型的字符最好超过 3 个（如果样本不够，重复步骤 2）
5. 删除 `D:\doll-master\lr.pickle` 文件，重新运行程序，程序将自动训练新的逻辑回归模型

## TODO
- [ ] 优化磁盘性能，禁止多余的读写操作
- [x] 完善 README

## 参考项目
- [1033020837/WechatGameScript](https://github.com/1033020837/WechatGameScript)