# -*- coding: utf-8 -*-
# @Time ： 2023/6/6 9:06
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有
import allure
import pyautogui
import pytest
from pywinauto import mouse, application
import time
import pywinauto
from common import common_util
@pytest.mark.run(order=5)
@allure.feature('扫描图像界面')
class Test_ScanImagePage:
    def setup_class(self):
        common_util.back_systemSettingPage()
        common_util.del_all_patients()
        time.sleep(1)
        common_util.new_patient('testID','testName',1)

    # @pytest.mark.test
    @allure.title('截屏')
    def test_clip(self):
        allure.dynamic.description('截屏')
        try:
            app = common_util.connect_application()
            common_util.back_scanImagePage()
            with allure.step('点击截屏按钮'):
                clip_btn = app['血管内断层成像系统'].child_window(auto_id="btnClipImage", control_type="Button").wait('enabled', timeout=20)
                clip_btn.click()
                time.sleep(1)
                common_util.screen_shot('截屏完成')
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
                imglist_btn = app['血管内断层成像系统'].child_window(auto_id="btnPatientImage", control_type="Button")
                rect = imglist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(2)
                img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date", control_type="List")
                num = int(img_num.texts()[0][2])
                time.sleep(1)
                common_util.screen_shot('截屏后图像数量：{}'.format(num))
                assert num == 1
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                time.sleep(2)

        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    # @pytest.mark.test
    @allure.title('患者图像')
    def test_patientImage(self):
        allure.dynamic.description('患者图像')
        try:
            app = common_util.connect_application()
            common_util.back_scanImagePage()
            with allure.step('点击患者图像按钮,返回患者图像界面'):
                imglist_btn = app['血管内断层成像系统'].child_window(auto_id="btnPatientImage", control_type="Button")
                rect = imglist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(2)
                common_util.screen_shot('返回患者图像界面')
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                time.sleep(2)
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

        # @pytest.mark.test

    @allure.title('设置')
    def test_setting(self):
        allure.dynamic.description('设置：回撤类型，图像窗宽窗位风格，图像显示范围，')
        try:
            app = common_util.connect_application()
            common_util.back_scanImagePage()
            with allure.step('回撤距离和速度'):
                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button",
                                                                     found_index=0)
                setting_btn.click_input()
                pull_len = app['血管内断层成像系统'].child_window(auto_id="comPullback", control_type="ComboBox")
                pull_len.select(0)
                content_len = pull_len.texts()
                length_speed = {}
                for i in range(len(content_len)):
                    pull_len.select(i)
                    time.sleep(0.5)
                    pull_speed = app['血管内断层成像系统'].child_window(auto_id="comPullBackSped",
                                                                        control_type="ComboBox")
                    time.sleep(0.5)
                    pull_speed.select(0)
                    length_speed['{}'.format(content_len[i])] = pull_speed.texts()
                except_length_speed = common_util.read_systemInfo()
                assert except_length_speed['length_speed'] == length_speed
            with allure.step('回撤类型'):
                pull_type = app['血管内断层成像系统'].child_window(auto_id="comTriggers", control_type="ComboBox",
                                                                   found_index=0)
                content_type = pull_type.texts()
                assert content_type == ['自动', '手动']
                for i in range(len(content_type)):
                    pull_type.select(i)
                    time.sleep(1)
            with allure.step('图像窗宽窗位风格'):
                window_type = app['血管内断层成像系统'].child_window(auto_id="comWindowType",
                                                                     control_type="ComboBox", found_index=0)
                content_type = window_type.texts()
                assert content_type == ['常规', '暗黑', '高亮', '锐利', '自定义']
                for i in range(len(content_type)):
                    window_type.select(i)
                    time.sleep(1)
                window_type.select(0)
                time.sleep(1)
            with allure.step('显示范围'):
                field_type = app['血管内断层成像系统'].child_window(auto_id="comField", control_type="ComboBox",
                                                                    found_index=0)
                content_type = field_type.texts()
                except_type = common_util.read_systemInfo()['field_type']
                assert content_type == except_type
                for i in range(len(content_type)):
                    field_type.select(i)
                    time.sleep(1)
                field_type.select(1)
                close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                close_btn.click()
                time.sleep(1)
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    # @pytest.mark.skip(1)
    # @pytest.mark.test
    @allure.title('回撤')
    def test_pullback(self):
        allure.dynamic.description('回撤')
        try:
            app = common_util.connect_application()
            common_util.back_scanImagePage()
            with allure.step('6k:不同转速和距离'):
                # 6k转
                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                setting_btn.click_input()
                play_type = app['血管内断层成像系统'].child_window(auto_id="comLoop", control_type="ComboBox", found_index=0)
                play_type.select(0)
                play_speed = app['血管内断层成像系统'].child_window(auto_id="playbackSpeed", control_type="Slider", found_index=0)
                play_speed.set_value(10)
                k6_btn = app['血管内断层成像系统'].child_window(title="6k转", auto_id="rbRotateSpeed6000",control_type="RadioButton", found_index=0)
                k6_btn.click()
                pull_len = app['血管内断层成像系统'].child_window(auto_id="comPullback", control_type="ComboBox")
                pull_len.select(0)
                pull_speed = app['血管内断层成像系统'].child_window(auto_id="comPullBackSped", control_type="ComboBox")
                pull_speed.select(0)
                content_len = pull_len.texts()
                content_speed = pull_speed.texts()
                for i in range(len(content_len)):
                    setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                    if setting_close_btn.exists() == False:
                        setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                        setting_btn.click_input()
                    pull_len.select(i)
                    for j in range(len(content_speed)):
                        setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                        if setting_close_btn.exists() == False:
                            setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                            setting_btn.click_input()
                        pull_speed.select(j)
                        time.sleep(1)
                        common_util.screen_shot('距离/速度')
                        setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                        setting_close_btn.click()
                        time.sleep(1)
                        dsa = common_util.read_systemInfo()
                        if dsa['DSA'] == True:
                            dsa_btn = app['血管内断层成像系统'].child_window(title="显示DSA", control_type="Text", found_index=0)
                            if dsa_btn.exists():
                                dsa_btn = app['血管内断层成像系统'].child_window(title="显示DSA", auto_id="btnShow",control_type="Button")
                                dsa_btn.click_input()
                        time.sleep(1)
                        scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                        scan_btn.click()
                        time.sleep(5)
                        if i == 0 and j == 0:
                            calibration_btn = app['血管内断层成像系统'].child_window(auto_id="autoCalibration",control_type="Button")
                            calibration_btn.click()
                            time.sleep(13)
                        ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                        if ok_btn.exists():
                            ok_btn.click()
                        else:
                            stop_btn = app['血管内断层成像系统'].child_window(auto_id="stopScan", control_type="Button")
                            stop_btn.click()
                        scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                        scan_btn.click()
                        time.sleep(5)
                        ready_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                        ready_btn.click()
                        time.sleep(5)
                        pullback_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                        pullback_btn.click()
                        reset_btn = app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink",control_type="Button").wait('enabled', timeout=180)
                        assert reset_btn.is_enabled()
                        mm_pos = app['血管内断层成像系统'].child_window(title="mm", control_type="Text", found_index=0)
                        rect = mm_pos.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                        rect = play_btn.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        clip_btn = app['血管内断层成像系统'].child_window(auto_id="btnClipImage", control_type="Button").wait(wait_for='enabled', timeout=12)
                        if clip_btn.is_enabled():
                            clip_btn = app['血管内断层成像系统'].child_window(auto_id="txtIndex", control_type="Text")
                            frame_truth = int(clip_btn.texts()[0].split(': ')[-1])
                            pullLen = content_len[i].split('mm')[0]
                            pullSpeed = content_speed[j].split('mm')[0]
                            frame_expect = int(int(pullLen) / int(pullSpeed) * 100)
                            error = int(frame_expect * 0.05)
                            assert abs(frame_expect - frame_truth)< error
                        time.sleep(1)
                        add_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT", control_type="Button")
                        add_btn.click()
                        time.sleep(2)
            with allure.step('12k:不同转速和距离'):
                # 12k转
                k12 = common_util.read_systemInfo()
                if k12['K12'] == True:
                    setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                    setting_btn.click_input()
                    play_type = app['血管内断层成像系统'].child_window(auto_id="comLoop", control_type="ComboBox", found_index=0)
                    play_type.select(0)
                    play_speed = app['血管内断层成像系统'].child_window(auto_id="playbackSpeed", control_type="Slider", found_index=0)
                    play_speed.set_value(10)
                    pull_len = app['血管内断层成像系统'].child_window(auto_id="comPullback", control_type="ComboBox")
                    pull_len.select(0)
                    pull_speed = app['血管内断层成像系统'].child_window(auto_id="comPullBackSped", control_type="ComboBox")
                    pull_speed.select(0)
                    k12_btn = app['血管内断层成像系统'].child_window(title="12k转", auto_id="rbRotateSpeed12000",control_type="RadioButton", found_index=0)
                    k12_btn.click()
                    content_len = pull_len.texts()
                    content_speed = pull_speed.texts()
                    for i in range(len(content_len)):
                        setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",control_type="Button")
                        if setting_close_btn.exists() == False:
                            setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                            setting_btn.click_input()
                        pull_len.select(i)
                        pull_speed = app['血管内断层成像系统'].child_window(auto_id="comPullBackSped", control_type="ComboBox",found_index=0)
                        for j in range(len(content_speed)):
                            setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",control_type="Button")
                            if setting_close_btn.exists() == False:
                                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting",control_type="Button")
                                setting_btn.click_input()
                            pull_speed.select(j)
                            time.sleep(1)
                            common_util.screen_shot('距离/速度')
                            setting_close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting",control_type="Button")
                            setting_close_btn.click()
                            dsa_btn = app['血管内断层成像系统'].child_window(title="显示DSA", control_type="Text", found_index=0)
                            if dsa_btn.exists():
                                dsa_btn = app['血管内断层成像系统'].child_window(title="显示DSA", auto_id="btnShow",control_type="Button")
                                dsa_btn.click_input()
                            scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                            scan_btn.click()
                            time.sleep(5)
                            ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                            if ok_btn.exists():
                                ok_btn.click()
                            else:
                                stop_btn = app['血管内断层成像系统'].child_window(auto_id="stopScan", control_type="Button")
                                stop_btn.click()
                            scan_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                            scan_btn.click()
                            time.sleep(5)
                            ready_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                            ready_btn.click()
                            time.sleep(5)
                            pullback_btn = app['血管内断层成像系统'].child_window(auto_id="staScan", control_type="Button")
                            pullback_btn.click()
                            reset_btn = app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink",control_type="Button").wait('enabled', timeout=180)
                            assert reset_btn.is_enabled()
                            mm_pos = app['血管内断层成像系统'].child_window(title="mm", control_type="Text", found_index=0)
                            rect = mm_pos.rectangle().mid_point()
                            mouse.click(coords=(rect.x, rect.y))
                            play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                            rect = play_btn.rectangle().mid_point()
                            mouse.click(coords=(rect.x, rect.y))
                            clip_btn = app['血管内断层成像系统'].child_window(auto_id="btnClipImage", control_type="Button").wait(wait_for='enabled', timeout=12)
                            if clip_btn.is_enabled():
                                clip_btn = app['血管内断层成像系统'].child_window(auto_id="txtIndex", control_type="Text")
                                frame_truth = int(clip_btn.texts()[0].split(': ')[-1])
                                pullLen = content_len[i].split('mm')[0]
                                pullSpeed = content_speed[j].split('mm')[0]
                                frame_expect = int(int(pullLen) / int(pullSpeed) * 200)
                                error = int(frame_expect * 0.05)
                                assert abs(frame_expect - frame_truth)< error
                                time.sleep(1)
                            add_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT", control_type="Button")
                            add_btn.click()
                            time.sleep(2)
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False


    # # @pytest.mark.test
    @allure.title('关机(取消)')
    def test_shutDown_no(self):
        allure.dynamic.description('关机，点击取消按钮，应该不会关机')
        try:
            app = common_util.connect_application()
            common_util.back_scanImagePage()
            with allure.step('点击关机按钮'):
                clsoe_btn = app['血管内断层成像系统'].child_window(auto_id="imgClose", control_type="Button",found_index=0)
                clsoe_btn.click()
                time.sleep(1)
                common_util.screen_shot('关机提示框')
                no_btn = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                no_btn.click()
                time.sleep(1)
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False