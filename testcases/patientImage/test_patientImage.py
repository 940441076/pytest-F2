# -*- coding: utf-8 -*-
# @Time ： 2023/6/6 9:06
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有
import time

import allure
import pyautogui
import pytest
from pywinauto import mouse, keyboard

import pywinauto

from common import common_util
@pytest.mark.run(order=3)
@allure.feature('患者图像界面')
class Test_PatientImagePage:

    def setup_class(self):
        app = common_util.connect_application()
        common_util.del_all_patients()
        common_util.import_testdata()

    # @pytest.mark.test
    @allure.title('查看图像')
    def test_view_image(self):
        allure.dynamic.description('查看图像')
        try:
            app = common_util.connect_application()
            common_util.back_patientImgPage()
            with allure.step('点击查看按钮，进入图像播放界面'):
                look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=1)
                rect = look_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(3)
                common_util.screen_shot('图像播放界面')
                end_btn = app['血管内断层成像系统'].child_window(auto_id="close", control_type="Button").wait(wait_for='exists', timeout=50)
                end_btn.click()
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
    @allure.title('编辑患者')
    def test_edit_patient(self):
        allure.dynamic.description('编辑患者：不可以修改为已存在的住院号，姓名不管')
        try:
            app = common_util.connect_application()
            common_util.back_patientImgPage()
            with allure.step('编辑患者：不做修改'):
                edit_btn = app['血管内断层成像系统'].child_window(auto_id="btnEditPatient", control_type="Button")
                edit_btn.click()
                time.sleep(0.5)
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOK",control_type="Button")
                ok_btn.click()
                time.sleep(0.5)
            with allure.step('编辑患者：住院号不存在'):
                edit_btn = app['血管内断层成像系统'].child_window(auto_id="btnEditPatient", control_type="Button")
                edit_btn.click()
                time.sleep(0.5)
                hospitalId = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                rect = hospitalId.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                keyboard.send_keys('^a')
                time.sleep(0.5)
                hospitalId.type_keys('edit_id')
                time.sleep(0.5)
                name = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                rect = name.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                keyboard.send_keys('^a')
                time.sleep(0.5)
                name.type_keys('edit_name')
                age = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
                age.type_keys(120)
                time.sleep(0.5)
                sex_btn = app['血管内断层成像系统'].child_window(title="女", auto_id="rbtnWoman",
                                                                      control_type="RadioButton")
                sex_btn.click()
                time.sleep(0.5)
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOK",
                                                                     control_type="Button")
                ok_btn.click()
                time.sleep(3)
                common_util.screen_shot('修改后')
                info_hospitalId = app['血管内断层成像系统']['Static6']
                info_name = app['血管内断层成像系统']['Static10']
                info_sex = app['血管内断层成像系统']['Static14']
                assert info_hospitalId.texts()== ['edit_id']
                assert info_name.texts()== ['edit_name']
                assert info_sex.texts()== ['女']
                time.sleep(1)
            with allure.step('新建一个患者，后面作为住院号存在数据'):
                common_util.new_patient(hospitalId='id',patientName='name',age=1)
                time.sleep(1)
                clip_btn = app['血管内断层成像系统'].child_window(auto_id="btnClipImage", control_type="Button")
                clip_btn.click()
                time.sleep(1)
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
                imglist_btn = app['血管内断层成像系统'].child_window(auto_id="btnPatientImage", control_type="Button")
                rect = imglist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(3)
            with allure.step('编辑患者：住院号存在，姓名不变'):
                edit_btn = app['血管内断层成像系统'].child_window(auto_id="btnEditPatient", control_type="Button")
                edit_btn.click()
                time.sleep(1)
                hospitalId = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                rect = hospitalId.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                keyboard.send_keys('^a')
                hospitalId.type_keys('edit_id')
                time.sleep(0.5)
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOK",control_type="Button")
                ok_btn.click()
                time.sleep(1)
                common_util.screen_shot('修改住院号已存在')
                content = app['提示']['Pane'].texts()
                assert ['该住院号已被注册过！'] ==content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)

            with allure.step('编辑患者：住院号不存在，姓名已存在'):
                hospitalId = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                rect = hospitalId.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                keyboard.send_keys('^a')
                hospitalId.type_keys('new_id')
                time.sleep(0.5)
                name = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                rect = name.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                keyboard.send_keys('^a')
                name.type_keys('edit_name')
                time.sleep(0.5)
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOK",control_type="Button")
                ok_btn.click()
                time.sleep(3)
                common_util.screen_shot('修改姓名存在后')
                info_hospitalId = app['血管内断层成像系统']['Static6']
                info_name = app['血管内断层成像系统']['Static10']
                info_sex = app['血管内断层成像系统']['Static14']
                assert info_hospitalId.texts() == ['new_id']
                assert info_name.texts() == ['edit_name']
                assert info_sex.texts() == ['男']
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
    def test_import(self):
        allure.dynamic.description('导出')
        try:
            app = common_util.connect_application()
            common_util.back_patientImgPage()
            with allure.step('选中数据后，点击导出按钮'):
                check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox", control_type="CheckBox",found_index=0)
                rect = check_mark.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                export_btn = app['血管内断层成像系统'].child_window(title="导出", control_type="Text",found_index=0)
                rect = export_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",control_type="Button")
                next_btn.click()
                time.sleep(1)
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",control_type="Button").wait(wait_for='enabled', timeout=100)
                time.sleep(1)
                usb_btn = app['血管内断层成像系统'].child_window(title="USB", auto_id="usbRadio",control_type="RadioButton")
                rect = usb_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                out_btn = app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",control_type="Button")
                out_btn.click()
                time.sleep(1)
                app['提示'].wait(wait_for='exists', timeout=100)
                time.sleep(2)
                common_util.screen_shot('导出提示')
                success_pane = app['提示']['Static3']
                num = int(success_pane.texts()[0].split(':')[-1])
                assert num == 1
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
                cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",control_type="Button")
                cancel_btn.click()
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
    @allure.title('删除患者图像')
    def test_del_image(self):
        allure.dynamic.description('删除患者图像')
        try:
            app = common_util.connect_application()
            common_util.back_patientImgPage()
            with allure.step('不勾选数据点击删除'):
                check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox", control_type="CheckBox", found_index=0)
                state = check_mark.get_toggle_state()
                if state==1:
                    rect = check_mark.rectangle().mid_point()
                    mouse.click(coords=(rect.x, rect.y))
                    time.sleep(0.5)
                del_btn = app['血管内断层成像系统'].child_window(title="删除", control_type="Text", found_index=0)
                rect = del_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                content = app['提示']['Pane'].texts()[0]
                time.sleep(1)
                common_util.screen_shot('未选择数据，点击删除')
                assert content=='请选择需要删除的图像！'
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(1)
            with allure.step('勾选数据点击删除'):
                check_mark = app['血管内断层成像系统'].child_window(auto_id="checkBox", control_type="CheckBox", found_index=0)
                rect = check_mark.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                del_btn = app['血管内断层成像系统'].child_window(title="删除", control_type="Text", found_index=0)
                rect = del_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
            with allure.step('选择否'):
                no_btn = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                no_btn.click()
                time.sleep(1)
                del_btn = app['血管内断层成像系统'].child_window(title="删除", control_type="Text", found_index=0)
                rect = del_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
            with allure.step('选择是'):
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                time.sleep(1)
                common_util.screen_shot('删除后数量为0')
                img_num = app['血管内断层成像系统'].child_window(auto_id="lstBox_Date", control_type="List")
                assert len(img_num.texts())== 0
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
            common_util.back_patientImgPage()
            with allure.step('点击新建OCT按钮'):
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                time.sleep(1)
                scan_btn = app['血管内断层成像系统'].child_window(auto_id="autoCalibration", control_type="Button")
                time.sleep(1)
                common_util.screen_shot('跳转到患者图像界面')
                assert scan_btn.exists()
                imglist_btn = app['血管内断层成像系统'].child_window(auto_id="btnPatientImage", control_type="Button")
                rect = imglist_btn.rectangle().mid_point()
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
    @allure.title('关于软件使用协议')
    def test_showInfo(self):
        allure.dynamic.description('患者图像界面显示软件协议信息，且内容不可以修改和删除')
        try:
            app = common_util.connect_application()
            common_util.back_patientImgPage()
            with allure.step('点击关于按钮'):
                show_btn = app['血管内断层成像系统']['Button2']
                show_btn.click()
                time.sleep(1)
                detail = app['血管内断层成像系统']['Document'].texts()[0]
                except_num = common_util.read_systemInfo()['info_text']
                except_key = common_util.read_systemInfo()['info_key']
                assert len(detail) == except_num
                assert except_key in detail
                common_util.add_text('结果：文本内容初始长度为{}，包含关键信息：{}'.format(except_num, except_key))
            with allure.step('点击弹窗中间，输入:测试修改内容'):
                content = app['血管内断层成像系统']['使用协议Dialog']
                rect = content.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                keyboard.send_keys('测试修改内容')
                detail = app['血管内断层成像系统']['Document'].texts()[0]
                except_num = common_util.read_systemInfo()['info_text']
                assert len(detail) == except_num
                common_util.add_text('结果：文本内容长度为{}，没能修改成功'.format(except_num))
            with allure.step('点击弹窗中间，按删除键Backspace'):
                content = app['血管内断层成像系统']['使用协议Dialog']
                rect = content.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                keyboard.send_keys('{BACKSPACE}')
                except_num = common_util.read_systemInfo()['info_text']
                assert len(detail) == except_num
                common_util.add_text('结果：文本内容长度为{}，没能删除成功'.format(except_num))
            with allure.step('退出协议界面'):
                close_btn = app['血管内断层成像系统'].child_window(auto_id="btnClose", control_type="Button")
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
    @allure.title('关机(取消)')
    def test_shutDown_no(self):
        allure.dynamic.description('患者图像界面关机，点击取消按钮，应该不会关机')
        try:
            app = common_util.connect_application()
            common_util.back_patientImgPage()
            with allure.step('点击关机按钮'):
                clsoe_btn = app['血管内断层成像系统'].child_window(auto_id="imgClose", control_type="Button")
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