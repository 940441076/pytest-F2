import os
import glob
# 1.需要提前安装好python环境
# 2.需要提前准备好allure安装包和java安装包

# 判断是否安装allure
folder_alure = glob.glob(r'D:\workspace\allure-2.22.1\bin')
if folder_alure == []:
    os.system(r'D:\测试所需\allure-2.22.1.exe')
# 判断是否安装java
folder_java = glob.glob(r'C:\Program Files\Java\jdk-17\bin')
if folder_java == []:
    os.system(r'D:\测试所需\jdk-17_windows-x64_bin.exe')
# 添加临时变量
path = os.environ.get('PATH')
path = r'D:\workspace\allure-2.22.1\bin;C:\Program Files\Java\jdk-17\bin;'+path
os.environ['PATH'] = path
os.system('allure open report/')


