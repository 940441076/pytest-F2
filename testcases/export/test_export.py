# -*- coding: utf-8 -*-
# @Time ： 2023/6/6 9:06
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有
import random

import allure
import pyautogui
import pytest
from pywinauto import mouse,keyboard
import time
from common import common_util
import string
import os
import win32api
import glob
# @pytest.mark.skip('忽略')
@allure.feature('导出')
@allure.title('导出')
class TestExport:
    @pytest.mark.test
    def test_export(self):
        allure.dynamic.description('测试导出')
        try:
            app = common_util.connect_application()
            common_util.del_devices_file()
            common_util.del_all_patients()
            for m in range(2):
                common_util.new_patient(hospitalId='id{}'.format(m+1),patientName='name{}'.format(m+1))
                with allure.step('6k:不同转速和距离'):
                    # 6k转
                    setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                    setting_btn.click_input()
                    k6_btn = app['血管内断层成像系统'].child_window(title="6k转", auto_id="rbRotateSpeed6000",
                                                                    control_type="RadioButton", found_index=0)
                    k6_btn.click()
                    pull_len = app['血管内断层成像系统'].child_window(auto_id="comPullback", control_type="ComboBox")
                    pull_len.select(0)
                    content_len = pull_len.texts()
                    for i in range(len(content_len)):
                        setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",
                                                                                   control_type="Button")
                        if setting_close_btn.exists() == False:
                            setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting",
                                                                                 control_type="Button")
                            setting_btn.click_input()
                        pull_len.select(i)
                        pull_speed = app['血管内断层成像系统'].child_window(auto_id="comPullBackSped",
                                                                            control_type="ComboBox")
                        pull_speed.select(0)
                        content_speed = pull_speed.texts()
                        for j in range(len(content_speed)):
                            setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",
                                                                                       control_type="Button")
                            if setting_close_btn.exists() == False:
                                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting",
                                                                                     control_type="Button",
                                                                                 found_index=0)
                                setting_btn.click_input()
                            pull_speed.select(j)
                            time.sleep(1)
                            common_util.screen_shot('距离/速度:{}-{}'.format(content_len[i], content_speed[j]))
                            setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",
                                                                                       control_type="Button")
                            setting_close_btn.click()
                            time.sleep(1)
                            scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                            scan_btn.click()
                            time.sleep(5)
                            ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                            if ok_btn.exists():
                                ok_btn.click()
                            else:
                                stop_btn = app['血管内断层成像系统'].child_window(auto_id="stopScan",
                                                                                  control_type="Button")
                                stop_btn.click()
                            scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                            scan_btn.click()
                            time.sleep(5)
                            ready_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                            ready_btn.click()
                            time.sleep(5)
                            pullback_btn = app['血管内断层成像系统'].child_window(auto_id="staScan",
                                                                                  control_type="Button")
                            pullback_btn.click()
                            time.sleep(10)
                            for k in range(15):
                                export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutPut",control_type="Button")
                                time.sleep(6)
                                if export_btn.is_enabled():
                                    time.sleep(1)
                                    break
                            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutPut",control_type="Button")
                            if export_btn.is_enabled():

                                random_num = random.randint(1, 31)
                                if random_num % 2 == 0:
                                    with allure.step('开始导出'):
                                        export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutPut",control_type="Button")
                                        export_btn.click()
                                        time.sleep(1)
                                        out_btn = app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                                                         control_type="Button").wait('enabled',timeout=5)
                                        out_btn.click()
                                        for k in range(100):
                                            if k%2==0:
                                                pyautogui.click(500,500)
                                            else:
                                                pyautogui.click(600, 600)
                                        time.sleep(1)
                                        common_util.screen_shot('截图')
                                        ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                                          control_type="Button").wait(wait_for='exists',
                                                                                                      timeout=100)
                                        ok_btn.click()
                                        time.sleep(1)
                                        end_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT",control_type="Button")
                                        end_btn.click()
                                        time.sleep(2)
                                elif random_num % 3 == 0 or random_num % 5 == 0:
                                    with allure.step('结束查看'):
                                        end_btn = app['血管内断层成像系统'].child_window(auto_id="close",
                                                                                         control_type="Button")
                                        end_btn.click()

                                        time.sleep(3)
                                    with allure.step('选中数据后，点击导出按钮'):
                                        img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date",
                                                                                         control_type="List")
                                        img_num = int(img_num.texts()[0][2])-1
                                        if img_num > 5:
                                            for k in range(70):
                                                mouse.scroll(coords=(500, 500), wheel_dist=-10)
                                        check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox",control_type="CheckBox",found_index=img_num)
                                        rect = check_mark.rectangle().mid_point()
                                        mouse.click(coords=(rect.x, rect.y))
                                        time.sleep(1)
                                        export_btn = app['血管内断层成像系统'].child_window(title="导出",control_type="Text",found_index=0)
                                        rect = export_btn.rectangle().mid_point()
                                        mouse.click(coords=(rect.x, rect.y))
                                        time.sleep(1)
                                        next_btn = app['血管内断层成像系统'].child_window(title="下一步",auto_id="btnOutput",control_type="Button")
                                        next_btn.click()
                                        time.sleep(1)
                                        app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                                               control_type="Button").wait(
                                            wait_for='enabled', timeout=100)
                                        time.sleep(1)
                                        out_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                         auto_id="btnOutput",
                                                                                         control_type="Button").wait('enabled',timeout=5)
                                        out_btn.click()
                                        for k in range(100):
                                            if k % 2 == 0:
                                                pyautogui.click(500, 500)
                                            else:
                                                pyautogui.click(600, 600)
                                        time.sleep(1)
                                        common_util.screen_shot('截图')
                                        ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                                          control_type="Button").wait(wait_for='exists', timeout=100)
                                        ok_btn.click()
                                        time.sleep(1)
                                        cancel_btn = app['血管内断层成像系统'].child_window(title="取消",
                                                                                            auto_id="btnCancel",
                                                                                            control_type="Button")
                                        cancel_btn.click()
                                        time.sleep(1)
                                        newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                                        newOCT_btn.click()
                                        time.sleep(2)
                                else:
                                    end_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT",
                                                                                     control_type="Button")
                                    end_btn.click()
                                    time.sleep(2)
                            else:
                                with allure.step('lumen计算失败'):
                                    end_btn = app['血管内断层成像系统'].child_window(auto_id="close",
                                                                                     control_type="Button")
                                    end_btn.click()

                                    time.sleep(3)
                                with allure.step('选中数据后，点击导出按钮'):
                                    img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date",
                                                                                     control_type="List")
                                    img_num = int(img_num.texts()[0][2]) - 1
                                    if img_num > 5:
                                        for k in range(70):
                                            mouse.scroll(coords=(500, 500), wheel_dist=-10)
                                    check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox",
                                                                                        control_type="CheckBox",
                                                                                        found_index=img_num)
                                    rect = check_mark.rectangle().mid_point()
                                    mouse.click(coords=(rect.x, rect.y))
                                    time.sleep(1)
                                    export_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                        control_type="Text",
                                                                                        found_index=0)
                                    rect = export_btn.rectangle().mid_point()
                                    mouse.click(coords=(rect.x, rect.y))
                                    time.sleep(1)
                                    next_btn = app['血管内断层成像系统'].child_window(title="下一步",
                                                                                      auto_id="btnOutput",
                                                                                      control_type="Button")
                                    next_btn.click()
                                    time.sleep(1)
                                    app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                                           control_type="Button").wait(
                                        wait_for='enabled', timeout=100)
                                    time.sleep(1)
                                    out_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                     auto_id="btnOutput",
                                                                                     control_type="Button").wait(
                                        'enabled', timeout=5)
                                    out_btn.click()
                                    for k in range(100):
                                        if k % 2 == 0:
                                            pyautogui.click(500, 500)
                                        else:
                                            pyautogui.click(600, 600)
                                    time.sleep(1)
                                    common_util.screen_shot('截图')
                                    ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                                      control_type="Button").wait(wait_for='exists', timeout=100)
                                    ok_btn.click()
                                    time.sleep(1)
                                    cancel_btn = app['血管内断层成像系统'].child_window(title="取消",
                                                                                        auto_id="btnCancel",
                                                                                        control_type="Button")
                                    cancel_btn.click()
                                    time.sleep(1)
                                    newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT",
                                                                                        control_type="Button")
                                    newOCT_btn.click()
                                    time.sleep(2)
                            time.sleep(3)
                with allure.step('12k:不同转速和距离'):
                    k12 = common_util.read_systemInfo()
                    if k12['K12'] == True:
                        setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                        setting_btn.click_input()
                        pull_len = app['血管内断层成像系统'].child_window(auto_id="comPullback",control_type="ComboBox")
                        pull_len.select(0)
                        k12_btn = app['血管内断层成像系统'].child_window(title="12k转", auto_id="rbRotateSpeed12000",
                                                                         control_type="RadioButton", found_index=0)
                        k12_btn.click()
                        content_len = pull_len.texts()
                        for i in range(len(content_len)):
                            setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",
                                                                                       control_type="Button")
                            if setting_close_btn.exists() == False:
                                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting",
                                                                                     control_type="Button")
                                setting_btn.click_input()
                            pull_len.select(i)
                            time.sleep(1)

                            setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",
                                                                                       control_type="Button")
                            if setting_close_btn.exists() == False:
                                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting",
                                                                                     control_type="Button")
                                setting_btn.click_input()
                            pull_len.select(i)
                            pull_speed = app['血管内断层成像系统'].child_window(auto_id="comPullBackSped",
                                                                                control_type="ComboBox")
                            pull_speed.select(0)
                            content_speed = pull_speed.texts()
                            for j in range(len(content_speed)):
                                setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",
                                                                                           control_type="Button")
                                if setting_close_btn.exists() == False:
                                    setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting",
                                                                                         control_type="Button",
                                                                         found_index=0)
                                    setting_btn.click_input()
                                pull_speed.select(j)
                                time.sleep(1)
                                common_util.screen_shot('距离/速度:{}-{}'.format(content_len[i], content_speed[j]))
                                setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",
                                                                                           control_type="Button")
                                setting_close_btn.click()
                                scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan",
                                                                                  control_type="Button")
                                scan_btn.click()
                                time.sleep(5)
                                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                                  control_type="Button")
                                if ok_btn.exists():
                                    ok_btn.click()
                                else:
                                    stop_btn = app['血管内断层成像系统'].child_window(auto_id="stopScan",
                                                                                      control_type="Button")
                                    stop_btn.click()
                                scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan",
                                                                                  control_type="Button")
                                scan_btn.click()
                                time.sleep(4)
                                ready_btn = app['血管内断层成像系统'].child_window(auto_id="staScan",
                                                                                   control_type="Button")
                                ready_btn.click()
                                time.sleep(5)
                                pullback_btn = app['血管内断层成像系统'].child_window(auto_id="staScan",
                                                                                      control_type="Button")
                                pullback_btn.click()

                                if content_len[i]=='54mm' and content_speed[j]=='10mm/s':
                                    time.sleep(30)
                                else:
                                    time.sleep(15)
                                for k in range(15):
                                    export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutPut",
                                                                                        control_type="Button")
                                    time.sleep(6)
                                    if export_btn.is_enabled():
                                        time.sleep(1)
                                        break
                                export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutPut",
                                                                                    control_type="Button")
                                if export_btn.is_enabled():

                                    random_num = random.randint(1, 31)
                                    if random_num % 2 == 0:
                                        with allure.step('开始导出'):
                                            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutPut",
                                                                                                control_type="Button")
                                            export_btn.click()
                                            time.sleep(1)
                                            out_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                             auto_id="btnOutput",
                                                                                             control_type="Button").wait(
                                                'enabled', timeout=5)
                                            out_btn.click()
                                            for k in range(100):
                                                if k % 2 == 0:
                                                    pyautogui.click(500, 500)
                                                else:
                                                    pyautogui.click(600, 600)
                                            time.sleep(1)
                                            common_util.screen_shot('截图')
                                            ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                                              control_type="Button").wait(
                                                wait_for='exists',
                                                timeout=100)
                                            ok_btn.click()
                                            time.sleep(1)
                                            end_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT",
                                                                                             control_type="Button")
                                            end_btn.click()
                                            time.sleep(2)
                                    elif random_num % 3 == 0 or random_num % 5 == 0:
                                        with allure.step('结束查看'):
                                            end_btn = app['血管内断层成像系统'].child_window(auto_id="close",
                                                                                             control_type="Button")
                                            end_btn.click()

                                            time.sleep(3)
                                        with allure.step('选中数据后，点击导出按钮'):
                                            img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date",
                                                                                             control_type="List")
                                            img_num = int(img_num.texts()[0][2]) - 1
                                            if img_num > 5:
                                                for k in range(70):
                                                    mouse.scroll(coords=(500, 500), wheel_dist=-10)
                                            check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox",
                                                                                                control_type="CheckBox",
                                                                                                found_index=img_num)
                                            rect = check_mark.rectangle().mid_point()
                                            mouse.click(coords=(rect.x, rect.y))
                                            time.sleep(1)
                                            export_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                                control_type="Text",
                                                                                                found_index=0)
                                            rect = export_btn.rectangle().mid_point()
                                            mouse.click(coords=(rect.x, rect.y))
                                            time.sleep(1)
                                            next_btn = app['血管内断层成像系统'].child_window(title="下一步",
                                                                                              auto_id="btnOutput",
                                                                                              control_type="Button")
                                            next_btn.click()
                                            time.sleep(1)
                                            app['血管内断层成像系统'].child_window(title="导出",
                                                                                   auto_id="btnOutput",
                                                                                   control_type="Button").wait(
                                                wait_for='enabled', timeout=100)
                                            time.sleep(1)
                                            out_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                             auto_id="btnOutput",
                                                                                             control_type="Button").wait(
                                                'enabled', timeout=5)
                                            out_btn.click()
                                            for k in range(100):
                                                if k % 2 == 0:
                                                    pyautogui.click(500, 500)
                                                else:
                                                    pyautogui.click(600, 600)
                                            time.sleep(1)
                                            common_util.screen_shot('截图')
                                            ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                                              control_type="Button").wait(wait_for='exists', timeout=100)
                                            ok_btn.click()
                                            time.sleep(1)
                                            cancel_btn = app['血管内断层成像系统'].child_window(title="取消",
                                                                                                auto_id="btnCancel",
                                                                                                control_type="Button")
                                            cancel_btn.click()
                                            time.sleep(1)
                                            newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT",
                                                                                                control_type="Button")
                                            newOCT_btn.click()
                                            time.sleep(2)
                                    else:
                                        end_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT",
                                                                                         control_type="Button")
                                        end_btn.click()
                                        time.sleep(2)
                                else:
                                    with allure.step('lumen计算失败'):
                                        end_btn = app['血管内断层成像系统'].child_window(auto_id="close",
                                                                                         control_type="Button")
                                        end_btn.click()

                                        time.sleep(3)
                                    with allure.step('选中数据后，点击导出按钮'):
                                        img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date",
                                                                                         control_type="List")
                                        img_num = int(img_num.texts()[0][2]) - 1
                                        if img_num > 5:
                                            for k in range(70):
                                                mouse.scroll(coords=(500, 500), wheel_dist=-10)
                                        check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox",
                                                                                            control_type="CheckBox",
                                                                                            found_index=img_num)
                                        rect = check_mark.rectangle().mid_point()
                                        mouse.click(coords=(rect.x, rect.y))
                                        time.sleep(1)
                                        export_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                            control_type="Text",
                                                                                            found_index=0)
                                        rect = export_btn.rectangle().mid_point()
                                        mouse.click(coords=(rect.x, rect.y))
                                        time.sleep(1)
                                        next_btn = app['血管内断层成像系统'].child_window(title="下一步",
                                                                                          auto_id="btnOutput",
                                                                                          control_type="Button")
                                        next_btn.click()
                                        time.sleep(1)
                                        app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                                               control_type="Button").wait(
                                            wait_for='enabled', timeout=100)
                                        time.sleep(1)
                                        out_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                                         auto_id="btnOutput",
                                                                                         control_type="Button").wait(
                                            'enabled', timeout=5)
                                        out_btn.click()
                                        for k in range(100):
                                            if k % 2 == 0:
                                                pyautogui.click(500, 500)
                                            else:
                                                pyautogui.click(600, 600)
                                        time.sleep(1)
                                        common_util.screen_shot('截图')
                                        ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                                          control_type="Button").wait(wait_for='exists', timeout=100)
                                        ok_btn.click()
                                        time.sleep(1)
                                        cancel_btn = app['血管内断层成像系统'].child_window(title="取消",
                                                                                            auto_id="btnCancel",
                                                                                            control_type="Button")
                                        cancel_btn.click()
                                        time.sleep(1)
                                        newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT",
                                                                                            control_type="Button")
                                        newOCT_btn.click()
                                        time.sleep(2)
                                time.sleep(3)
                common_util.back_patientListPage()
                patient_list = app['血管内断层成像系统'].child_window(title="F_2.Models.PatientInfo",
                                                                      control_type="DataItem", found_index=0)
                patient_list.click_input()
                time.sleep(2)
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk", control_type="Button")
                ok_btn.click()
                time.sleep(2)
                with allure.step('选中最后一个数据后，点击导出按钮'):
                    img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date", control_type="List")
                    img_num = int(img_num.texts()[0][2])-1
                    if img_num>5:
                        for i in range(70):
                            mouse.scroll(coords=(500, 500), wheel_dist=-10)
                    check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox",
                                                                        control_type="CheckBox",
                                                                        found_index=img_num)

                    rect = check_mark.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    time.sleep(1)
                    export_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                        control_type="Text",
                                                                        found_index=0)
                    rect = export_btn.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    time.sleep(1)
                    next_btn = app['血管内断层成像系统'].child_window(title="下一步",
                                                                      auto_id="btnOutput",
                                                                      control_type="Button")
                    next_btn.click()
                    time.sleep(1)
                    app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                           control_type="Button").wait(
                        wait_for='enabled', timeout=100)
                    time.sleep(1)
                    out_btn = app['血管内断层成像系统'].child_window(title="导出",
                                                                     auto_id="btnOutput",
                                                                     control_type="Button").wait('enabled',timeout=5)
                    out_btn.click()
                    for k in range(100):
                        if k % 2 == 0:
                            pyautogui.click(500, 500)
                        else:
                            pyautogui.click(600, 600)
                    time.sleep(1)
                    common_util.screen_shot('截图')
                    ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton",
                                                      control_type="Button").wait(wait_for='exists', timeout=100)
                    ok_btn.click()
                    time.sleep(1)
                    cancel_btn = app['血管内断层成像系统'].child_window(title="取消",
                                                                        auto_id="btnCancel",
                                                                        control_type="Button")
                    cancel_btn.click()
                    time.sleep(1)

            disk_list = []
            for c in string.ascii_uppercase:
                disk = c + ':'
                if os.path.isdir(disk):
                    disk_list.append(disk)
            for i in range(len(disk_list)):
                disk_info = win32api.GetVolumeInformation(disk_list[i] + '/')
                if disk_info[0] == 'BossXU':
                    usb_adress = disk_list[i] + '/*'
                    files = glob.glob(usb_adress)
            export_file = []
            for i in range(len(files)):
                if 'FSM_202' in files[i]:
                    export_file.append(i)
            with allure.step('导出次数{}'.format(len(export_file))):
                common_util.add_text('导出次数：{}'.format(len(export_file)))
        except Exception as e:
            common_util.add_text(str(e))
            assert False

