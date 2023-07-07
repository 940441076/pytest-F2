import os
import smtplib
import time
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import allure
import pyautogui
import glob
import yaml
from pywinauto import application,mouse,keyboard
import psutil
import shutil
import string
import win32api
import json
import re
from uiautomation import WindowControl
from dingtalkchatbot.chatbot import DingtalkChatbot
def connect_application():

    #。。。。。。。。。。
    '''启动软件'''
    try:
        process = []
        processID = []
        for proc in psutil.process_iter():
            process.append(proc.name())
            processID.append(proc.pid)
        if 'OCTViewer.exe' in process:
            pid_index = process.index('OCTViewer.exe')
            pid = int(processID[pid_index])
            app = application.Application(backend='uia').connect(process=pid)
            time.sleep(2)
        else:
            app = application.Application(backend='uia').start(r'D:\OCTViewer-VM1\bin\OCTViewer.exe')
            # app['提示'].wait('exists', timeout=50)
            # ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
            # if ok_btn.exists():
            #     ok_btn.click()
            app['血管内断层成像系统'].wait('exists', timeout=150)
            time.sleep(2)
        return app
    except:
        time.sleep(1)
        screen_shot('异常：connect_application')

def kill_app():
    '''结束程序'''
    for proc in psutil.process_iter():
        if proc.name() == 'OCTViewer.exe':
            proc.kill()
        if proc.name() == 'OctLogServer.exe':
            proc.kill()
def kill_allure_serve():
    '''结束程序'''
    for proc in psutil.process_iter():
        if proc.name() == 'cmd.exe':
            proc.kill()
def screen_shot(title):
    '''截图提交到报告中'''
    try:
        pyautogui.screenshot('result/screen.jpg')
        allure.attach.file('result/screen.jpg', title, allure.attachment_type.JPG)
    except:
        time.sleep(1)
        screen_shot('异常：screen_shot')
def add_text(content):
    '''添加结果描述到报告中'''
    allure.attach('', content, allure.attachment_type.TEXT)


def new_patient(hospitalId='id',patientName='name',age=1):
    app = connect_application()
    back_homePage()
    regist_btn = app['血管内断层成像系统'].child_window(title="新增患者", auto_id="btnRegist",
                                                        control_type="Button")
    rect = regist_btn.rectangle().mid_point()
    mouse.click(coords=(rect.x, rect.y))
    time.sleep(1)
    hospitalId1 = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
    hospitalId1.type_keys(hospitalId)
    time.sleep(0.5)
    name = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
    name.type_keys(patientName)
    time.sleep(0.5)
    age1 = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
    age1.type_keys(age)
    time.sleep(0.5)
    newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
    newOCT_btn.click()
    time.sleep(3)
def del_all_patients():
    try:
        app = connect_application()
        back_patientListPage()
        patient_list = app['血管内断层成像系统']['ListView']
        time.sleep(1)
        if len(patient_list.texts()) > 0:
            patient_list = app['血管内断层成像系统']['ListView'].child_window(title="F_2.Models.PatientInfo",
                                                                                  control_type="DataItem", found_index=0)
            patient_list.click_input()
            time.sleep(1)
            keyboard.send_keys('^a')
            del_patient = app['血管内断层成像系统'].child_window(title="删除患者", control_type="Text", found_index=1)
            rect = del_patient.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            time.sleep(1)
            is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
            is_btn.click()
            time.sleep(1)
            is_btn2 = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
            is_btn2.click()
            time.sleep(2)
    except:
        time.sleep(1)
        screen_shot('异常：del_all_patients')

def del_devices_file():
    '''删除U盘和本地数据'''
    try:
        disk_list = []
        usb_adress = []
        for c in string.ascii_uppercase:
            disk = c + ':'
            if os.path.isdir(disk):
                disk_list.append(disk)
        for i in range(len(disk_list)):
            disk_info = win32api.GetVolumeInformation(disk_list[i] + '/')
            if disk_info[0] == 'TesterXu':
                usb_adress = disk_list[i] + '/*'
                files = glob.glob(usb_adress)
                for i in range(len(files)):
                    if os.path.isdir(files[i]) and files[i].split(r'/')[-1] != 'data' and files[i].split(r'/')[-1] != 'System Volume Information':
                        shutil.rmtree(files[i])
                    elif os.path.isfile(files[i]):
                        os.remove(files[i])
        if os.path.exists(r'D:/Export'):
            shutil.rmtree(r'D:/Export')

        files = glob.glob(usb_adress)
        for i in range(len(files)):
            if os.path.isdir(files[i]) and files[i].split(r'/')[-1] != 'data' and files[i].split(r'/')[-1] != 'System Volume Information':
                shutil.rmtree(files[i])
            elif os.path.isfile(files[i]):
                os.remove(files[i])
        return usb_adress
    except:
        time.sleep(1)
        screen_shot('异常：del_devices_file')

def import_testdata(index=0):
    '''U盘导入测试数据'''
    try:
        app = connect_application()
        back_homePage()
        # exit_engineerMode()
        import_btn = app['血管内断层成像系统'].child_window(title="导入", control_type="Text", found_index=1)
        rect = import_btn.rectangle().mid_point()
        mouse.click(coords=(rect.x, rect.y))
        time.sleep(1)
        item = app['血管内断层成像系统'].child_window(auto_id="cmbFilePath", control_type="ComboBox").wait(wait_for='visible', timeout=50)
        if index != 0:
            item.select(1)
        time.sleep(2)
        import_btn2 = app['血管内断层成像系统'].child_window(title="导入", control_type="Button")
        import_btn2.click()
        time.sleep(1)
        ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button").wait(
            wait_for='exists', timeout=800)
        ok_btn.click()
        time.sleep(2)
    except:
        time.sleep(1)
        screen_shot('异常：import_testdata')

def back_homePage():
    '''返回首页'''
    try:
        app = connect_application()
        select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist", control_type="Button")

        if not select_btn.exists():
            imglist_btn = app['血管内断层成像系统'].child_window(auto_id="btnPatientImage", control_type="Button")
            if imglist_btn.exists():
                rect = imglist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
            end_btn = app['血管内断层成像系统'].child_window(auto_id="close", control_type="Button")
            if end_btn.exists():
                end_btn.click()
            stent_conf_btn = app['血管内断层成像系统'].child_window(title="支架配置", control_type="TabItem")
            if stent_conf_btn.exists():
                ok_btn = app['血管内断层成像系统'].child_window(title="确认", control_type="Text")
                rect = ok_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
            home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
            if home_btn.exists():
                home_btn.click()
            time.sleep(1)
    except:
        time.sleep(1)
        screen_shot('异常：back_homePage')

def back_patientListPage():
    '''返回患者列表界面'''
    try:
        app = connect_application()
        select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist", control_type="Button")
        imglist_btn = app['血管内断层成像系统'].child_window(title="患者图像", control_type="Text", found_index=0)
        end_btn = app['血管内断层成像系统'].child_window(auto_id="close", control_type="Button")
        home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
        edit_btn = app['血管内断层成像系统'].child_window(auto_id="btnEditPatient", control_type="Button")
        stent_conf_btn = app['血管内断层成像系统'].child_window(title="支架配置", control_type="TabItem")
        if stent_conf_btn.exists():
            ok_btn = app['血管内断层成像系统'].child_window(title="确认", control_type="Text")
            rect = ok_btn.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            time.sleep(1)
            if imglist_btn.exists():
                rect = imglist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(2)
                home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
                home_btn.click()
                time.sleep(1)
                select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist",control_type="Button")
                select_btn.click()
        elif select_btn.exists():
            select_btn.click()
        elif imglist_btn.exists():
            rect = imglist_btn.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            time.sleep(2)
            home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
            home_btn.click()
            time.sleep(1)
            select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist",
                                                                control_type="Button")
            select_btn.click()
        elif end_btn.exists():
            end_btn.click()
            time.sleep(2)
            home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
            home_btn.click()
            time.sleep(1)
            select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist",
                                                                control_type="Button")
            select_btn.click()
        elif home_btn.exists() and edit_btn.exists():
            home_btn.click()
            time.sleep(1)
            select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist",
                                                                control_type="Button")
            select_btn.click()
        time.sleep(2)
    except:
        time.sleep(1)
        screen_shot('异常：back_patientListPage')
def back_patientImgPage():
    '''返回患者图像列表界面'''
    try:
        app = connect_application()
        edit_btn = app['血管内断层成像系统'].child_window(auto_id="btnEditPatient", control_type="Button")
        if not edit_btn.exists():
            back_patientListPage()
            patient_list = app['血管内断层成像系统'].child_window(title="F_2.Models.PatientInfo",control_type="DataItem", found_index=0)
            patient_list.click_input()
            time.sleep(2)
            ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk", control_type="Button")
            ok_btn.click()
            time.sleep(2)
    except:
        time.sleep(1)
        screen_shot('异常：back_patientImgPage')


def back_imageViewPage():
    '''返回图像查看界面'''
    try:
        app = connect_application()
        end_btn = app['血管内断层成像系统'].child_window(auto_id="close", control_type="Button")
        if not end_btn.exists():
            back_patientImgPage()
            look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=1)
            rect = look_btn.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            time.sleep(2)
    except:
        time.sleep(1)
        screen_shot('异常：back_imageViewPage')

def back_scanImagePage():
    '''返回扫描界面'''
    try:
        app = connect_application()
        imglist_btn = app['血管内断层成像系统'].child_window(title="患者图像", control_type="Text", found_index=0)
        if not imglist_btn.exists():
            back_patientImgPage()
            newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
            newOCT_btn.click()
            time.sleep(2)
    except:
        time.sleep(1)
        screen_shot('异常：back_scanImagePage')

def back_systemSettingPage():
    '''进入系统设置界面'''
    try:
        app = connect_application()
        stent_conf_btn = app['血管内断层成像系统'].child_window(title="支架配置", control_type="TabItem")
        if not stent_conf_btn.exists():
            back_patientListPage()
            menu = app['血管内断层成像系统'].child_window(title="菜单", control_type="Text", found_index=0)
            rect = menu.rectangle().mid_point()
            mouse.move(coords=(rect.x, rect.y))
            time.sleep(0.5)
            dispose_btn = app['血管内断层成像系统'].child_window(title="系统配置", control_type="Text", found_index=0)
            rect = dispose_btn.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            time.sleep(1)
    except:
        time.sleep(1)
        screen_shot('异常：back_systemSettingPage')

def select_device_import(num):
    '''选择外接设备，导出成功后判断并截图'''
    try:
        deviceType = [['CD/DVD','cdRadio'],['USB','usbRadio'],['本地文件夹','folderRadio']]
        app = connect_application()
        usb_btn = app['血管内断层成像系统'].child_window(title=deviceType[num][0], auto_id=deviceType[num][1],
                                                         control_type="RadioButton")
        rect = usb_btn.rectangle().mid_point()
        mouse.click(coords=(rect.x, rect.y))
        time.sleep(1)
        out_btn = app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                         control_type="Button")
        out_btn.click()
        app['提示'].wait(wait_for='exists', timeout=1000)
        time.sleep(1)
        screen_shot('成功提示')
        success_pane = app['提示']['Static3']
        num = int(success_pane.texts()[0].split(':')[-1])
        assert num == 2
        ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
        ok_btn.click()
    except:
        time.sleep(1)
        screen_shot('异常：select_device_import')

def open_engineerMode():
    '''打开工程师模式'''
    try:
        app = connect_application()
        back_systemSettingPage()
        show_test = app['血管内断层成像系统'].child_window(title="显示工程师模式", auto_id="btnEngineerMode",control_type="Button")
        if show_test.exists():
            rect = show_test.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            pwd_edit = app['血管内断层成像系统'].child_window(auto_id="pwd", control_type="Edit")
            pwd_edit.type_keys('14606c66')
            ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk", control_type="Button",found_index=0)
            rect = ok_btn.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
        time.sleep(1)
    except:
        time.sleep(1)
        screen_shot('异常：open_engineerMode')

def exit_engineerMode():
    '''退出工程师模式'''
    try:
        app = connect_application()
        back_systemSettingPage()
        exit_test = app['血管内断层成像系统'].child_window(title="退出工程师模式", auto_id="btnEngineerMode",control_type="Button")
        if exit_test.exists():
            rect = exit_test.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
    except:
        time.sleep(1)
        screen_shot('异常：exit_engineerMode')

def read_yaml(path):
    try:
        with open(os.getcwd()+path,encoding='utf-8') as f:
            value = yaml.load(stream=f,Loader=yaml.FullLoader)
            return value
    except:
        time.sleep(1)
        screen_shot('异常：read_yaml')

 # 设置报告窗口的标题
def set_windows_title():
    """
    通过修改allure-html目录下的index.html文件，设置打开的 Allure 报告的浏览器窗口标题文案
    @param allure_html_path: allure生成的html测试报告根目录
    @param new_title:  需要更改的标题文案 【 原文案为：Allure Report 】
    @return:
    """
    report_title_filepath = r"result/report/index.html"
    # 定义为只读模型，并定义名称为: f
    with open(report_title_filepath, 'r+', encoding="utf-8") as f:
        # 读取当前文件的所有内容
        all_the_lines = f.readlines()
        f.seek(0)
        f.truncate()
        # 循环遍历每一行的内容，将 "Allure Report" 全部替换为 → new_title(新文案)
        for line in all_the_lines:
            f.write(line.replace("Allure Report", 'VM1自动化测试报告(xuky)'))
        # 关闭文件
        f.close()

 # 设置报告内容的标题
def set_report_name():
    """
    通过修改allure-html目录下的widgets/summary.json, 修改Allure报告Overview的标题文案
    @param allure_html_path: allure生成的html测试报告根目录
    @param new_name:  需要更改的标题文案 【 原文案为：ALLURE REPORT 】
    @return:
    """
    deviceType = read_yaml('/extract.yaml')['systemInfo']['deviceType']


    title_filepath = r"result/report/widgets/summary.json"
    # 读取summary.json中的json数据，并改写reportName
    with open(title_filepath, 'rb') as f:
        # 加载json文件中的内容给params
        params = json.load(f)
        # 修改内容
        params['reportName'] = '{}自动化测试报告'.format(deviceType)
        # 将修改后的内容保存在dict中
        new_params = params
    # 往summary.json中，覆盖写入新的json数据
    with open(title_filepath, 'w', encoding="utf-8") as f:
        json.dump(new_params, f, ensure_ascii=False, indent=4)

# 新增环境配置
def set_report_env_on_html():
    """
     在allure-html报告中往widgets/environment.json中写入环境信息,
        格式参考如下：[{"values":["Auto Test Report"],"name":"report_title"},{"values":["autotestreport_"]]
    """
    systemInfo = read_yaml('/extract.yaml')['systemInfo']
    env_info = {'系统': 'WIN10 / V07',
                '内存': '12G',
                '显卡': 'GTX1080 / 8G',
                '软件版本': '{} / {} / {}'.format(systemInfo['SWV'],systemInfo['MC'],systemInfo['MDL']),
                }
    envs = []
    for k, v in env_info.items():
        envs.append({
            "name": k,
            "values": [v]
        })
    with open(r"result/report/widgets/environment.json", 'w', encoding="utf-8") as f:
        json.dump(envs, f, ensure_ascii=False, indent=4)


def send_mail():
    '''发送邮件'''
    try:
        dviceType = read_yaml('/extract.yaml')['systemInfo']['deviceType']
        # 登录 （QQ邮箱）
        # sender = '940441076@qq.com'
        # smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # smtp_obj.login(sender, 'liucswnixyrybcge')

        # 登录 （三五互联邮箱）
        sender = 'keyong.xu@forssmann.cn'
        smtp_obj = smtplib.SMTP_SSL('w.cn4e.com', 465)
        smtp_obj.login(sender, 'Gto1BXJkCHO7Asoo')

        # receiver = ['keyong.xu@forssmann.cn']
        receiver = ['keyong.xu@forssmann.cn', 'desheng.yuan@forssmann.cn', 'xiachi.liu@forssmann.cn', 'yanwen.wang@forssmann.cn']
        str_receiver = str(receiver).replace("[", '').replace("]", '').replace("'", '')
        # 设置内容
        title = '{}自动化测试结果'.format(dviceType)
        msg = MIMEMultipart()
        msg['From'] = formataddr(('徐克永', sender))
        msg['To'] = formataddr(('', str_receiver))
        msg['Subject'] = Header(title, 'utf-8')  # 主题
        try:
            window = WindowControl(searchDepth=1, Name='C:\Windows\py.exe')

            textContent = window.DocumentControl(searchDepth=1).GetTextPattern().DocumentRange.GetText()

            content = re.compile('at <(.*?)/>.', re.S)
            http_address = re.findall(content, textContent)[0]
            content = f'<p><h2>{title}截图:</h2><br><h4>报告临时链接(内网)：{http_address}</h4></br><br><img src="cid:resultImg"></br></p>'
        except:
            content = f'<p><h2>{title}截图:</h2><br><img src="cid:resultImg"></br></p>'
        # 正文带图片
        f = open(r"result/result.jpg", 'rb')  # 打开图片
        msgimage = MIMEImage(f.read())
        f.close()
        msgimage.add_header('Content-ID', '<resultImg>')  # 设置图片
        msg.attach(msgimage)
        msg.attach(MIMEText(content, 'html', 'utf-8'))  # 添加到邮件正
        # 发邮件
        smtp_obj.sendmail(sender, receiver, msg.as_string())
        smtp_obj.quit()
    except Exception as e:
        print(e)


def send_dingtalk():
    '''发送钉钉消息'''
    systemInfo = read_yaml('/extract.yaml')['systemInfo']
    try:
        webhook = 'https://oapi.dingtalk.com/robot/send?access_token=034ef99dce9cc9bcb08ce8ed887c8c06ce17a03989cee023098338a06957f419'
        secret = 'SECfc4c756e21efaf7ffdbef4fb2d732195f177d8d90847956274ea6c887287502c'
        ding = DingtalkChatbot(webhook, secret)
        try:
            window = WindowControl(searchDepth=1, Name='C:\Windows\py.exe')
            textContent = window.DocumentControl(searchDepth=1).GetTextPattern().DocumentRange.GetText()
            content = re.compile('at <(.*?)/>.', re.S)
            http_address = re.findall(content, textContent)[0]
        except:
            http_address = '地址错误'
        ding.send_text('{}自动化测试完成，\n测试报告临时链接(内网)：\n{}'.format(systemInfo['deviceType'],http_address))
    except Exception as e:
        print(e)
def open_report():
    '''本地文件打开'''
    os.system('allure_open_report.bat')
    # os.system('allure_serve_report.bat')

def read_systemInfo():
    '''从文件获取系统参数信息'''
    systemInfo = read_yaml('/extract.yaml')['systemInfo']
    return systemInfo