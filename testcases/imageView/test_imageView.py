# -*- coding: utf-8 -*-
# @Time ： 2023/6/6 9:06
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有

import allure
import pyautogui
import pytest
from pywinauto import mouse, keyboard
import time
import pywinauto
import re
from common import common_util

@pytest.mark.run(order=4)
@allure.feature('图像查看界面')
class Test_ImageViewPage:

    def setup_class(self):
        common_util.del_all_patients()
        common_util.import_testdata()

    # @pytest.mark.test
    @allure.title('打印到U盘')
    def test_print_usb(self):
        allure.dynamic.description('打印到U盘')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('点击打印按钮'):
                play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                rect = play_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                print_btn = app['血管内断层成像系统'].child_window(auto_id="btnPrint", control_type="Button").wait('enabled',timeout=20)
                print_btn.click()
                time.sleep(1)
                no_btn = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                no_btn.click()
                time.sleep(1)
                pane = app['提示']
                if pane.exists():
                    content = app['提示']['Pane'].texts()[0]
                    assert '未找到打印机' in content
                    time.sleep(1)
                    common_util.screen_shot('未找到打印机')
                    ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                    ok_btn.click()
                else:
                    app1 = pywinauto.Desktop()
                    nvdia = app1.window(title_re='Print preview')
                    time.sleep(1)
                    common_util.screen_shot('windows打印弹窗')
                    nvdia.close()
                time.sleep(1)
                print_btn = app['血管内断层成像系统'].child_window(auto_id="btnPrint", control_type="Button")
                print_btn.click()
                time.sleep(1)
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                content = app['提示']['Pane'].texts()[0]
                time.sleep(1)
                common_util.screen_shot('打印完成')
                assert '已成功打印到外插设备' in content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
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

    # @pytest.mark.test
    @allure.title('截屏')
    def test_clip(self):
        allure.dynamic.description('截屏')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('点击截屏按钮'):
                end_btn = app['血管内断层成像系统'].child_window(auto_id="close", control_type="Button")
                end_btn.click()
                time.sleep(1)
                img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date", control_type="List")
                num1 = int(img_num.texts()[0][2])
                time.sleep(1)
                common_util.screen_shot('截屏前图像数量：{}'.format(num1))
                look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=1)
                rect = look_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(3)
                play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                rect = play_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                clip_btn = app['血管内断层成像系统'].child_window(auto_id="btnClipImage", control_type="Button").wait('enabled',timeout=20)
                clip_btn.click()
                time.sleep(1)
                common_util.screen_shot('截屏完成')
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
                end_btn = app['血管内断层成像系统'].child_window(auto_id="close", control_type="Button")
                end_btn.click()
                img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date", control_type="List")
                num2 = int(img_num.texts()[0][2])
                time.sleep(1)
                common_util.screen_shot('截屏后图像数量：{}'.format(num2))
                assert num2==num1+1

                look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=1)
                rect = look_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
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

    # @pytest.mark.test
    @allure.title('导出')
    def test_export(self):
        allure.dynamic.description('导出')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('开始导出'):
                point1 = app['血管内断层成像系统'].child_window(title="30", control_type="Text", found_index=0)
                rect = point1.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutPut", control_type="Button").wait(wait_for='enabled', timeout=20)
                export_btn.click()
                time.sleep(1)
                usb_btn = app['血管内断层成像系统'].child_window(title="USB", auto_id="usbRadio", control_type="RadioButton")
                usb_btn.click()
                time.sleep(1)
                out_btn = app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput", control_type="Button")
                out_btn.click()
                app['提示'].wait(wait_for='exists', timeout=120)
                success_pane = app['提示']['Static3']
                time.sleep(1)
                common_util.screen_shot('导出完成')
                assert '导出结束，文件数量为:1'== success_pane.texts()[0]
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
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

    # @pytest.mark.test
    @allure.title('显示纵切面')
    def test_showZong(self):
        allure.dynamic.description('显示纵切面')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('显示纵切面'):

                checkbox_zong = app['血管内断层成像系统'].child_window(title="纵切面", auto_id="ckbzong",
                                                                       control_type="CheckBox")
                rect = checkbox_zong.rectangle()
                rect = re.sub('[a-zA-Z() ]', '', str(rect)).split(',')
                pos = (int(rect[2]) - 3, int(rect[1]))
                mouse.move(coords=pos)
                checkbox_zong2 = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                        found_index=0)
                rect = checkbox_zong2.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('不显示纵切面')
                app['血管内断层成像系统'].child_window(auto_id="imageMprOper", control_type="Custom").wait_not(
                    wait_for_not='visible', timeout=2)
                time.sleep(1)
                common_util.screen_shot('显示纵切面')
                checkbox_zong3 = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                        found_index=0)
                rect = checkbox_zong3.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                app['血管内断层成像系统'].child_window(auto_id="imageMprOper", control_type="Custom").wait(
                    wait_for='visible', timeout=2)
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

    # @pytest.mark.test
    @allure.title('显示官腔分析')
    def test_showLumen(self):
        allure.dynamic.description('显示官腔分析')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('显示官腔分析'):
                time.sleep(1)
                checkbox_gq = app['血管内断层成像系统'].child_window(title="管腔分析", auto_id="ckblumen",
                                                                     control_type="CheckBox")
                rect = checkbox_gq.rectangle()
                rect = re.sub('[a-zA-Z() ]', '', str(rect)).split(',')
                pos = (int(rect[2]) - 3, int(rect[1]))
                mouse.move(coords=pos)

                checkbox_gq3 = app['血管内断层成像系统'].child_window(title="管腔分析", control_type="Text",
                                                                      found_index=0)
                rect = checkbox_gq3.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('不显示官腔分析')
                app['血管内断层成像系统'].child_window(auto_id="thbNarrow", control_type="Thumb").wait_not(
                    wait_for_not='visible', timeout=5)
                time.sleep(1)
                checkbox_gq2 = app['血管内断层成像系统'].child_window(title="管腔分析", control_type="Text",
                                                                      found_index=0)
                rect = checkbox_gq2.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                app['血管内断层成像系统'].child_window(auto_id="thbNarrow", control_type="Thumb").wait(
                    wait_for='visible', timeout=2)
                time.sleep(1)
                common_util.screen_shot('显示官腔分析')
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

    # @pytest.mark.test
    @allure.title('图像后校准')
    def test_reset(self):
        allure.dynamic.description('图像后校准')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('开始校准'):
                point1 = app['血管内断层成像系统'].child_window(title="30", control_type="Text", found_index=0)
                rect = point1.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                reset_btn = app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink", control_type="Button")
                reset_btn.click()
                time.sleep(1)
                check_btn = app['血管内断层成像系统'].child_window(title="应用到全部帧", auto_id="cbApplyAll", control_type="CheckBox")
                state = check_btn.get_toggle_state()
                time.sleep(1)
                common_util.screen_shot('默认勾选应用到全部帧')
                assert state==1
                reset_btn2 = app['血管内断层成像系统'].child_window(auto_id="btnReset", control_type="Button", found_index=0)
                reset_btn2.click()
                time.sleep(1)
                common_util.screen_shot('校准 ing')
                reset_btn = app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink", control_type="Button").wait('enabled', timeout=120)
                time.sleep(1)
                reset_num = app['血管内断层成像系统'].child_window(title="0", auto_id="lbShrinkRatio", control_type="Text")
                assert reset_btn.is_enabled()
                assert reset_num.exists()
                time.sleep(1)
                if reset_btn.is_enabled():
                    reset_btn = app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink", control_type="Button")
                    reset_btn.click()
                    time.sleep(1)
                    check_btn = app['血管内断层成像系统'].child_window(title="应用到全部帧", auto_id="cbApplyAll", control_type="CheckBox")
                    rect = check_btn.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    state = check_btn.get_toggle_state()
                    time.sleep(1)
                    common_util.screen_shot('不勾选应用到全部帧')
                    assert state==0
                    set_btn = app['血管内断层成像系统'].child_window(auto_id="btnOk", control_type="Button", found_index=0)
                    set_btn.click()
                    time.sleep(1)
                    common_util.screen_shot('校准ing')
                    set_btn = app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink", control_type="Button").wait('enabled', timeout=120)
                    assert set_btn.is_enabled()
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

    # @pytest.mark.test
    @allure.title('设置血管类型和手术过程')
    def test_vessel_procedure(self):
        allure.dynamic.description('血管类型和手术过程')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('对比软件中的项与实际需求项vessel'):
                vessel_type = app['血管内断层成像系统'].child_window(auto_id="cmbVessel", control_type="ComboBox")
                vessel_list = ['Not Selected', 'RCA Prox', 'RCA Mid', 'RCA Distal', 'PDA', 'Left Main', 'LAD Prox', 'LAD Mid', 'LAD Distal', 'Diagonal 1', 'Diagonal 2', 'LCX Prox', 'LCX OM1',
                                      'LCX Mid', 'LCX OM2', 'LCX Distal', 'Other']
                assert vessel_type.texts()== vessel_list
            with allure.step('新增项：add_vessel'):
                rect = vessel_type.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                select_one = app['血管内断层成像系统'].child_window(title="Left Main", control_type="ListItem", found_index=0)
                rect = select_one.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                vessel_type = app['血管内断层成像系统'].child_window(auto_id="cmbVessel", control_type="ComboBox")
                rect = vessel_type.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                show_add_pane = app['血管内断层成像系统'].child_window(title="Other", control_type="ListItem", found_index=0)
                rect = show_add_pane.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                add_pane = app['血管内断层成像系统'].child_window(auto_id="txtInputItem1", control_type="Edit")
                add_pane.type_keys('add_vessel')
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOK", control_type="Button", found_index=0)
                ok_btn.click()
                time.sleep(1)
                rect = vessel_type.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('新增add_vessel类型')
                assert 'add_vessel'in vessel_type.texts()
            with allure.step('对比软件中的项与实际需求项procedure'):
                procedure_type = app['血管内断层成像系统'].child_window(auto_id="cmbProcedure", control_type="ComboBox")
                procedure_list = ['Not Selected', 'Pre-PCI', 'Post-PCI', 'Follow-Up', 'Other']
                assert procedure_type.texts()== procedure_list
            with allure.step('新增项：add_procedure'):
                rect = procedure_type.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                mouse.click(coords=(rect.x, rect.y))
                select_one = app['血管内断层成像系统'].child_window(title="Pre-PCI", control_type="ListItem", found_index=0)
                rect = select_one.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                procedure_type = app['血管内断层成像系统'].child_window(auto_id="cmbProcedure", control_type="ComboBox")
                rect = procedure_type.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                show_add_pane = app['血管内断层成像系统'].child_window(title="Other", control_type="ListItem", found_index=0)
                rect = show_add_pane.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                add_pane = app['血管内断层成像系统'].child_window(auto_id="txtInputItem1", control_type="Edit")
                add_pane.type_keys('add_procedure')
                time.sleep(1)
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOK", control_type="Button", found_index=0)
                ok_btn.click()
                time.sleep(1)
                rect = procedure_type.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('新增procedure类型')
                assert 'add_procedure'in procedure_type.texts()
                time.sleep(1)
            with allure.step('返回系统设置界面，对比vessel和procedure'):
                common_util.back_systemSettingPage()
                vessel_list = app['血管内断层成像系统'].child_window(auto_id="listBoxVessel", control_type="List")
                rect = vessel_list.rectangle().mid_point()
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                vessel_type = vessel_list.texts()
                assert ['add_vessel'] in vessel_type
                procedure_list = app['血管内断层成像系统'].child_window(auto_id="listBoxProcedure",control_type="List")
                procedure_type = procedure_list.texts()
                time.sleep(1)
                common_util.screen_shot('包含：add_vessel和add_procedure')
                assert ['add_procedure'] in procedure_type
            with allure.step('初始化：恢复vessel和procedure'):
                initial_btn = app['血管内断层成像系统'].child_window(title="初始化", control_type="Text",
                                                                     found_index=0)
                rect = initial_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                time.sleep(1)
                initial_btn = app['血管内断层成像系统'].child_window(title="初始化", control_type="Text",
                                                                     found_index=1)
                rect = initial_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
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

    # @pytest.mark.test
    @allure.title('右侧悬浮栏相关功能')
    def test_rightToolBar(self):
        allure.dynamic.description('左侧悬浮栏相关功能')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('获取屏幕的尺寸，固定悬浮框'):
                point = app['血管内断层成像系统'].child_window(title="10", control_type="Text", found_index=0)
                rect = point.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                screenWidth, screenHeight = pyautogui.size()
                mouse.move(coords=(screenWidth - 5, int(screenHeight / 2)))
                fix_btn = app['血管内断层成像系统'].child_window(auto_id="btnGd1", control_type="Button")
                rect = fix_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
            with allure.step('曲线'):
                curve_btn = app['血管内断层成像系统'].child_window(auto_id="btnCurve", control_type="Button")
                rect = curve_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                mouse.click(coords=(int(screenWidth / 2 - 100), int(screenHeight / 2) - 100))
                mouse.click(coords=(int(screenWidth / 2 + 60), int(screenHeight / 2) - 80))
                mouse.click(coords=(int(screenWidth / 2 + 50), int(screenHeight / 2) + 50))
                mouse.click(coords=(int(screenWidth / 2), int(screenHeight / 2) + 80))
                mouse.click(coords=(int(screenWidth / 2 - 90), int(screenHeight / 2) + 10))
                mouse.click(coords=(int(screenWidth / 2 - 100), int(screenHeight / 2) - 100))
                time.sleep(1)
            with allure.step('直线'):
                line_btn = app['血管内断层成像系统'].child_window(auto_id="btnLine", control_type="Button")
                rect = line_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                mouse.click(coords=(int(screenWidth / 2 + 90), int(screenHeight / 2) - 90))
                mouse.click(coords=(int(screenWidth / 2 - 90), int(screenHeight / 2) + 90))
                time.sleep(1)
            with allure.step('角度'):
                angle_btn = app['血管内断层成像系统'].child_window(auto_id="btnAngle", control_type="Button")
                rect = angle_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                mouse.click(coords=(int(screenWidth / 2 - 80), int(screenHeight / 2) - 80))
                mouse.click(coords=(int(screenWidth / 2 + 80), int(screenHeight / 2) + 80))
                mouse.click(coords=(int(screenWidth / 2 - 80), int(screenHeight / 2) + 80))
                time.sleep(1)
            with allure.step('文字备注'):
                word_btn = app['血管内断层成像系统'].child_window(auto_id="btnWord", control_type="Button")
                rect = word_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                mouse.click(coords=(int(screenWidth / 2), int(screenHeight / 2)))
                time.sleep(1)
                text_pane = app['文字'].child_window(auto_id="txtInputItem1", control_type="Edit")
                text_pane.type_keys('这是文字备注呀')
                ok_btn = app['文字'].child_window(title="确定", auto_id="btnOK", control_type="Button", found_index=0)
                ok_btn.click()
                time.sleep(1)
            with allure.step('狭窄率'):
                as_btn = app['血管内断层成像系统'].child_window(auto_id="btnAS", control_type="Button")
                rect = as_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                as_pane1 = app['血管内断层成像系统'].child_window(auto_id="lstBox_fenzi", control_type="List")
                res = as_pane1.texts()
                item_fenzi = app['血管内断层成像系统'].child_window(auto_id="lstBox_fenzi", control_type="List").child_window(title="{}".format(res[0][0]), control_type="Text")
                rect = item_fenzi.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                as_pane2 = app['血管内断层成像系统'].child_window(auto_id="lstBox_fenmu", control_type="List")
                res = as_pane2.texts()
                item_fenmu = app['血管内断层成像系统'].child_window(auto_id="lstBox_fenmu", control_type="List").child_window(title="{}".format(res[-1][0]), control_type="Text")
                rect = item_fenmu.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                ok_btn = app['血管内断层成像系统'].child_window(title="确 定", auto_id="btnNarrowRate", control_type="Button")
                ok_btn.click()
                time.sleep(1)
            with allure.step('厚度'):
                thickness_btn = app['血管内断层成像系统'].child_window(auto_id="btnThickness", control_type="Button")
                rect = thickness_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                mouse.click(coords=(int(screenWidth / 2 - 80), int(screenHeight / 2)))
                mouse.click(coords=(int(screenWidth / 2 + 80), int(screenHeight / 2)))
                time.sleep(1)
            with allure.step('支架膨胀率'):
                swell_btn = app['血管内断层成像系统'].child_window(auto_id="btnSwell", control_type="Button")
                rect = swell_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                swell_pane = app['血管内断层成像系统'].child_window(auto_id="lstBox_fenzi", control_type="List")
                res = swell_pane.texts()
                item_fenzi = app['血管内断层成像系统'].child_window(title="{}".format(res[-1][0]), control_type="Text", found_index=0)
                rect = item_fenzi.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                item_fenmu = app['血管内断层成像系统'].child_window(auto_id="txtDiameter", control_type="Edit")
                rect = item_fenmu.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                item_fenmu.type_keys('2')
                ok_btn = app['血管内断层成像系统'].child_window(title="确 定", auto_id="btnNarrowRate", control_type="Button")
                ok_btn.click()
                time.sleep(1)
            with allure.step('查看做过的全部标记'):
                time.sleep(1)
                common_util.screen_shot('查看做过的全部标记')
            with allure.step('删除当前帧标记:有关联项'):
                swell_btn = app['血管内断层成像系统'].child_window(auto_id="btnDelChose", control_type="Button")
                rect = swell_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                tip_pane = app['提示']['pane']
                content = tip_pane.texts()[0]
                assert '是否删除当前帧标记' == content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
                tip_pane = app['提示']['pane']
                content = tip_pane.texts()[0]
                assert '请删除关联的狭窄率/膨胀率' == content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
            with allure.step('删除全部标记'):
                swell_btn = app['血管内断层成像系统'].child_window(auto_id="btnDelAll", control_type="Button")
                rect = swell_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                tip_pane = app['提示']['pane']
                content = tip_pane.texts()[0]
                assert '是否删除全部标记'== content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
            with allure.step('删除当前帧标记:无关联项'):
                swell_btn = app['血管内断层成像系统'].child_window(auto_id="btnDelChose", control_type="Button")
                rect = swell_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                tip_pane = app['提示']['pane']
                content = tip_pane.texts()[0]
                assert '是否删除当前帧标记'== content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
            with allure.step('删除后没有标记'):
                time.sleep(1)
                common_util.screen_shot('删除后没有标记')
            with allure.step('取消固定悬浮框'):
                fix_btn = app['血管内断层成像系统'].child_window(auto_id="btnGd1", control_type="Button")
                rect = fix_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
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

    # @pytest.mark.test
    @allure.title('左侧悬浮栏相关功能')
    def test_leftToolBar(self):
        allure.dynamic.description('左侧悬浮栏相关功能')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('固定左侧标记栏'):
                screenWidth, screenHeight = pyautogui.size()
                mouse.move(coords=(5, int(screenHeight / 2)))
                fix_btn = app['血管内断层成像系统'].child_window(auto_id="btnGd", control_type="Button")
                rect = fix_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
            with allure.step('做两帧测试标记'):
                frame = [["20",'这是上一帧'],["40",'这是下一帧']]
                for i in range(2):
                    frame1 = app['血管内断层成像系统'].child_window(title="{}".format(frame[i][0]), control_type="Text",found_index=0)
                    rect = frame1.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    mouse.move(coords=(screenWidth - 5, int(screenHeight / 2)))
                    word_btn = app['血管内断层成像系统'].child_window(auto_id="btnWord", control_type="Button")
                    rect = word_btn.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    mouse.click(coords=(int(screenWidth / 2), int(screenHeight / 2-200)))
                    text_pane = app['文字'].child_window(auto_id="txtInputItem1", control_type="Edit")
                    text_pane.type_keys('{}'.format(frame[i][1]))
                    ok_btn = app['文字'].child_window(title="确定", auto_id="btnOK", control_type="Button", found_index=0)
                    ok_btn.click()
                    time.sleep(1)
            with allure.step('上一帧、下一帧'):
                pre_btn = app['血管内断层成像系统'].child_window(auto_id="btnPreFrame", control_type="Button")
                rect = pre_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('上一帧')
                next_btn = app['血管内断层成像系统'].child_window(auto_id="btnNextFrame", control_type="Button")
                rect = next_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('下一帧')
            with allure.step('隐藏：标记、支架、Lumen'):
                hide_mark = app['血管内断层成像系统'].child_window(title="隐藏标记", control_type="Text", found_index=0)
                rect = hide_mark.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                hide_stent = app['血管内断层成像系统'].child_window(title="隐藏支架", control_type="Text", found_index=0)
                rect = hide_stent.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text", found_index=0)
                rect = hide_lumen.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('隐藏：标记、支架、Lumen')
            with allure.step('重置'):
                reset_btn = app['血管内断层成像系统'].child_window(title="重置", control_type="Text", found_index=0)
                rect = reset_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('重置')
            with allure.step('取消固定'):
                time.sleep(1)
                fix_btn = app['血管内断层成像系统'].child_window(auto_id="btnGd", control_type="Button")
                rect = fix_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
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

    # @pytest.mark.test
    @allure.title('纵切面做标记')
    def test_zong(self):
        allure.dynamic.description('纵切面做标记：直线、角度，书签')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            clip_btn = app['血管内断层成像系统'].child_window(auto_id="btnClipImage", control_type="Button")
            time.sleep(4)
            if not clip_btn.is_enabled():
                play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                rect = play_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
            screenWidth, screenHeight = pyautogui.size()
            with allure.step('新增：直线和角度'):
                mouse.move(coords=(screenWidth - 5, int(screenHeight / 2)))
                line_btn = app['血管内断层成像系统'].child_window(auto_id="btnLine", control_type="Button")
                rect = line_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                point1 = app['血管内断层成像系统'].child_window(title="10", control_type="Text", found_index=0)
                rect = point1.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                point2 = app['血管内断层成像系统'].child_window(title="20", control_type="Text", found_index=0)
                rect = point2.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                mouse.move(coords=(screenWidth - 5, int(screenHeight / 2)))
                angle_btn = app['血管内断层成像系统'].child_window(auto_id="btnAngle", control_type="Button")
                rect = angle_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                point1 = app['血管内断层成像系统'].child_window(title="10", control_type="Text", found_index=0)
                rect = point1.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y+10))
                mouse.click(coords=(rect.x, rect.y+100))
                mouse.click(coords=(rect.x + 100, rect.y+100))
                time.sleep(1)
                common_util.screen_shot('新增：直线和角度')
            with allure.step('删除：直线和角度'):
                point = app['血管内断层成像系统'].child_window(title="20", control_type="Text", found_index=0)
                rect = point.rectangle().mid_point()
                mouse.click(coords=(rect.x-10, rect.y))
                mouse.click(coords=(rect.x+5, rect.y-5))
                point1 = app['血管内断层成像系统'].child_window(title="10", control_type="Text", found_index=0)
                rect = point1.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y+10))
                mouse.click(coords=(rect.x+102, rect.y+8))
                time.sleep(1)
                common_util.screen_shot('删除：直线和角度')

            with allure.step('新增书签'):
                frame = ["20", '40']
                for i in range(2):
                    frame1 = app['血管内断层成像系统'].child_window(title="{}".format(frame[i]), control_type="Text", found_index=0)
                    rect = frame1.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    add_btn = app['血管内断层成像系统'].child_window(auto_id="addSign", control_type="Image")
                    rect = add_btn.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('新增书签')
            with allure.step('上一个、下一个书签'):
                pre_btn = app['血管内断层成像系统'].child_window(auto_id="preSign", control_type="Image")
                rect = pre_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('上一个')
                next_btn = app['血管内断层成像系统'].child_window(auto_id="nextSign", control_type="Image")
                rect = next_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('下一个')
            with allure.step('删除所有书签'):
                del_btn = app['血管内断层成像系统'].child_window(auto_id="delSign", control_type="Image")
                rect = del_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                no_btn = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                no_btn.click()
                time.sleep(1)
                common_util.screen_shot('删除所有：否')
                del_btn = app['血管内断层成像系统'].child_window(auto_id="delSign", control_type="Image")
                rect = del_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                time.sleep(1)
                common_util.screen_shot('删除所有：是')
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
    @allure.title('播放设置')
    def test_play(self):
        allure.dynamic.description('播放设置：单次、循环')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('设置播放速度'):
                mm_pos = app['血管内断层成像系统'].child_window(title="mm", control_type="Text", found_index=0)
                rect = mm_pos.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                setting_btn.click_input()
                time.sleep(1)
                play_speed = app['血管内断层成像系统'].child_window(auto_id="Thumb", control_type="Thumb", found_index=0)
                rect = play_speed.rectangle().mid_point()
                mouse.press(coords=(rect.x, rect.y))
                mouse.move(coords=(rect.x - 500, rect.y))
                mouse.release(coords=(rect.x - 500, rect.y))
                speed_text1 = app['血管内断层成像系统'].child_window(title="1", control_type="Text", found_index=0)
                assert speed_text1.exists()
                time.sleep(1)
                play_speed = app['血管内断层成像系统'].child_window(auto_id="Thumb", control_type="Thumb", found_index=0)
                rect = play_speed.rectangle().mid_point()
                mouse.press(coords=(rect.x, rect.y))
                mouse.move(coords=(rect.x + 800, rect.y))
                mouse.release(coords=(rect.x + 800, rect.y))
                speed_text2 = app['血管内断层成像系统'].child_window(title="10", control_type="Text", found_index=0)
                assert speed_text2.exists()
            with allure.step('设置单次'):
                play_type = app['血管内断层成像系统'].child_window(auto_id="comLoop", control_type="ComboBox", found_index=0)
                content_type = play_type.texts()
                assert content_type==['单次', '循环']
                play_type.select(0)
                close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                close_btn.click()
                time.sleep(1)
                play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                rect = play_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                clip_btn = app['血管内断层成像系统'].child_window(auto_id="btnClipImage", control_type="Button").wait(wait_for='enabled', timeout=10)
                time.sleep(1)
                assert clip_btn.is_enabled() ==True

            with allure.step('设置循环'):
                mm_pos = app['血管内断层成像系统'].child_window(title="mm", control_type="Text", found_index=0)
                rect = mm_pos.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                setting_btn.click_input()
                time.sleep(1)
                play_type = app['血管内断层成像系统'].child_window(auto_id="comLoop", control_type="ComboBox", found_index=0)
                content_type = play_type.texts()
                assert content_type==['单次', '循环']
                play_type.select(1)
                close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                close_btn.click()
                time.sleep(1)
                play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                rect = play_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(5)
                assert clip_btn.is_enabled() == False
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
    @allure.title('前进、后退')
    def test_left_right(self):
        allure.dynamic.description('前进、后退')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            point1 = app['血管内断层成像系统'].child_window(title="30", control_type="Text", found_index=0)
            rect = point1.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            current_frame = app['血管内断层成像系统']['当前帧数:'].texts()
            current_frame = int(current_frame[0].split(':')[-1])
            with allure.step('设置播步长:1'):
                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                setting_btn.click_input()
                step_page = app['血管内断层成像系统']['快进步长Edit']
                step_page.set_focus()
                keyboard.send_keys('^a')
                step_page.type_keys(0)
                close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                close_btn.click()
                time.sleep(1)
            with allure.step('前进步长1'):
                left_btn = app['血管内断层成像系统'].child_window(auto_id="leftBtn", control_type="Button")
                rect = left_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                left_frame = app['血管内断层成像系统']['当前帧数:'].texts()
                left_frame = int(left_frame[0].split(':')[-1])
                assert current_frame == left_frame+1
            with allure.step('后退步长1'):
                right_btn = app['血管内断层成像系统'].child_window(auto_id="rightBtn", control_type="Button")
                rect = right_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                right_frame = app['血管内断层成像系统']['当前帧数:'].texts()
                right_frame = int(right_frame[0].split(':')[-1])
                assert current_frame == right_frame

            with allure.step('设置播步长:30'):
                setting_btn = app['血管内断层成像系统'].child_window(auto_id="btnSetting", control_type="Button")
                setting_btn.click_input()
                step_page = app['血管内断层成像系统']['快进步长Edit']
                step_page.set_focus()
                keyboard.send_keys('^a')
                step_page.type_keys(31)
                close_btn = app['血管内断层成像系统'].child_window(auto_id="closeSetting", control_type="Button")
                close_btn.click()
                time.sleep(1)
            with allure.step('前进步长30'):
                left_btn = app['血管内断层成像系统'].child_window(auto_id="leftBtn", control_type="Button")
                rect = left_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                left_frame = app['血管内断层成像系统']['当前帧数:'].texts()
                left_frame = int(left_frame[0].split(':')[-1])
                assert current_frame == left_frame + 30
            with allure.step('后退步长30'):
                right_btn = app['血管内断层成像系统'].child_window(auto_id="rightBtn", control_type="Button")
                rect = right_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                right_frame = app['血管内断层成像系统']['当前帧数:'].texts()
                right_frame = int(right_frame[0].split(':')[-1])
                assert current_frame == right_frame

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
    @allure.title('3D')
    def test_3D(self):
        allure.dynamic.description('3D')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('勾选3D复选框'):
                app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink",
                                                                 control_type="Button").wait('enabled', timeout=120)
                time.sleep(1)
                checkbox_3D = app['血管内断层成像系统'].child_window(title="3D", auto_id="ckb3d",
                                                                          control_type="CheckBox")
                rect = checkbox_3D.rectangle()
                rect = re.sub('[a-zA-Z() ]', '', str(rect)).split(',')
                pos = (int(rect[2]) - 3, int(rect[1]))
                mouse.move(coords=pos)

                checkbox_3D2 = app['血管内断层成像系统'].child_window(title="3D", control_type="Text", found_index=0)
                rect = checkbox_3D2.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                rect = play_btn.rectangle().mid_point()
                mouse.move(coords=(rect.x, rect.y))
                # 等待loading进度条消失
                app['血管内断层成像系统'].child_window(auto_id="gif", control_type="Image").wait_not(
                    wait_for_not='visible', timeout=50)
                time.sleep(4)
                common_util.screen_shot('显示3D')
                pos_checkbox = app['血管内断层成像系统'].child_window(title="位置", auto_id="ckbShowPos",control_type="CheckBox")
                pos_checkbox.click_input()
                time.sleep(1)
                fly_checkbox = app['血管内断层成像系统'].child_window(title="导航", auto_id="ckbFly",control_type="CheckBox")
                fly_checkbox.click_input()
                time.sleep(2)
                tissue_checkbox = app['血管内断层成像系统'].child_window(title="组织", auto_id="ckbTissue",control_type="CheckBox")
                tissue_checkbox.click_input()
                # 等待loading进度条消失
                app['血管内断层成像系统'].child_window(auto_id="gif", control_type="Image").wait_not(
                    wait_for_not='visible', timeout=50)
                time.sleep(2)
                guide_checkbox = app['血管内断层成像系统'].child_window(title="导丝", auto_id="ckbGuide",control_type="CheckBox")
                guide_checkbox.click_input()
                time.sleep(1)
                stent_checkbox = app['血管内断层成像系统'].child_window(title="支架", auto_id="ckbStent",control_type="CheckBox")
                stent_checkbox.click_input()
                # 等待loading进度条消失
                app['血管内断层成像系统'].child_window(auto_id="gif", control_type="Image").wait_not(
                    wait_for_not='visible', timeout=50)
                time.sleep(6)
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                if ok_btn.exists():
                    ok_btn.click()
                onlyStent_checkbox = app['血管内断层成像系统'].child_window(title="仅支架", auto_id="ckbOnlyStent",control_type="CheckBox")
                onlyStent_checkbox.click_input()
                time.sleep(1)

                reset_checkbox = app['血管内断层成像系统'].child_window(auto_id="btnReset", control_type="Button",
                                                                             found_index=0).wait('active', timeout=10)
                reset_checkbox.click_input()
                time.sleep(1)
                bifurcation_checkbox = app['血管内断层成像系统'].child_window(title="分叉", auto_id="ckbBifurcation",control_type="CheckBox")
                bifurcation_checkbox.click_input()
                # 等待loading进度条消失
                app['血管内断层成像系统'].child_window(auto_id="gif", control_type="Image").wait_not(
                    wait_for_not='visible', timeout=50)
                time.sleep(3)

                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                if ok_btn.exists():
                    ok_btn.click()
                clip_checkbox = app['血管内断层成像系统'].child_window(title="切面", auto_id="ckbClip",control_type="CheckBox").wait('enabled',
                                                                                                          timeout=50)
                clip_checkbox.click_input()
                time.sleep(1)
                reset_checkbox = app['血管内断层成像系统'].child_window(auto_id="btnReset", control_type="Button",found_index=0).wait('active', timeout=10)
                reset_checkbox.click_input()
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

    # @pytest.mark.test
    @allure.title('DSA')
    def test_DSA(self):
        dsa = common_util.read_systemInfo()
        if dsa['DSA'] ==True:
            allure.dynamic.description('DSA')
            try:
                app = common_util.connect_application()
                common_util.back_imageViewPage()
                with allure.step('显示DSA'):
                    app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink",control_type="Button").wait('enabled', timeout=120)
                    time.sleep(1)
                    checkbox_DSA = app['血管内断层成像系统'].child_window(title="DSA", auto_id="ckbdsa",
                                                                               control_type="CheckBox")
                    rect = checkbox_DSA.rectangle()
                    rect = re.sub('[a-zA-Z() ]', '', str(rect)).split(',')
                    pos = (int(rect[2]) - 3, int(rect[1]))
                    mouse.move(coords=pos)
                    checkbox_DSA2 = app['血管内断层成像系统'].child_window(title="DSA", control_type="Text",
                                                                                found_index=0)
                    rect = checkbox_DSA2.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                    rect = play_btn.rectangle().mid_point()
                    mouse.move(coords=(rect.x, rect.y))
                    app['血管内断层成像系统'].child_window(auto_id="gif", control_type="Image").wait_not(
                        wait_for_not='visible', timeout=50)
                    time.sleep(1)
                    common_util.screen_shot('显示DSA')
                    pei_btn = app['血管内断层成像系统'].child_window(title="配准", control_type="Text", found_index=0)
                    rect = pei_btn.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    time.sleep(2)
                    common_util.screen_shot('选择导丝和导引导管')
                    mouse.click(coords=(556, 666))
                    error_text = app['血管内断层成像系统'].child_window(title="* 该数据无法配准", auto_id="txtInfo", control_type="Text")
                    if error_text.exists():
                        time.sleep(1)
                        common_util.screen_shot('无法配准')
                        cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnRegionCancel",control_type="Button")
                        cancel_btn.click_input()
                    else:
                        mouse.click(coords=(375, 300))
                        time.sleep(1)
                        confirm_btn = app['血管内断层成像系统'].child_window(auto_id="btnConfirm", control_type="Button")
                        rect_confirm = confirm_btn.rectangle().mid_point()
                        mouse.click(coords=(rect_confirm.x, rect_confirm.y))
                        time.sleep(1)
                        common_util.screen_shot('计算ing')
                        # 等待loading进度条消失
                        app['血管内断层成像系统'].child_window(auto_id="gif", control_type="Image").wait_not(wait_for_not='visible', timeout=100)
                        next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnNext",control_type="Button")
                        rect = next_btn.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        mouse.click(coords=(1023,556))
                        time.sleep(1)
                        common_util.screen_shot('选择mark点')
                        ok_btn = app['血管内断层成像系统'].child_window(title="确 定", auto_id="OkButton",control_type="Button")
                        rect = ok_btn.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('配准ing')
                        # 等待loading进度条消失
                        app['血管内断层成像系统'].child_window(auto_id="gif", control_type="Image").wait_not(
                            wait_for_not='visible',timeout=100)
                        ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                        if ok_btn.exists():
                            ok_btn.click()
                        thumb = app['血管内断层成像系统'].child_window(auto_id="thb", control_type="Thumb")
                        rect = thumb.rectangle().mid_point()
                        mouse.press(coords=(rect.x, rect.y))
                        mouse.move(coords=(rect.x - 1000, rect.y))
                        mouse.release(coords=(rect.x - 1000, rect.y))
                        time.sleep(0.5)
                        thumb = app['血管内断层成像系统'].child_window(auto_id="thb", control_type="Thumb")
                        rect = thumb.rectangle().mid_point()
                        mouse.press(coords=(rect.x, rect.y))
                        mouse.move(coords=(rect.x + 1000, rect.y))
                        mouse.release(coords=(rect.x + 1000, rect.y))
                        play_btn = app['血管内断层成像系统'].child_window(auto_id="playBtn", control_type="Button")
                        rect = play_btn.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('配准结果')
                        time.sleep(5)
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
            common_util.back_imageViewPage()
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
    # @pytest.mark.test
    @allure.title('结束查看')
    def test_endView(self):
        allure.dynamic.description('结束查看')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('结束查看'):
                end_btn = app['血管内断层成像系统'].child_window(auto_id="close", control_type="Button")
                end_btn.click()
                time.sleep(1)
                reset_btn = app['血管内断层成像系统'].child_window(title="校准", auto_id="btnResetShrink", control_type="Button")
                assert reset_btn.exists()== False
                look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=1)
                rect = look_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
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

    # @pytest.mark.test
    @allure.title('新建OCT')
    def test_newOCT(self):
        allure.dynamic.description('新建OCT')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
            with allure.step('新建OCT'):
                end_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT", control_type="Button")
                end_btn.click()
                time.sleep(2)
                sacn_btn = app['血管内断层成像系统'].child_window(title="开始扫描", control_type="Text", found_index=0)
                assert sacn_btn.exists()
                imglist_btn = app['血管内断层成像系统'].child_window(title="患者图像", control_type="Text", found_index=0)
                rect = imglist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=1)
                rect = look_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
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
    @allure.title('关机(取消)')
    def test_shutDown_no(self):
        allure.dynamic.description('关机，点击取消按钮，应该不会关机')
        try:
            app = common_util.connect_application()
            common_util.back_imageViewPage()
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


