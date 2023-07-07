# -*- coding: utf-8 -*-
# @Time ： 2023/6/6 9:06
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有
import allure
import pywinauto
import pytest
import time
from pywinauto import mouse, keyboard
from common import common_util
@pytest.mark.run(order=6)
@allure.feature('系统设置界面')
class Test_SystemSettingPage:
    # @pytest.mark.test
    @pytest.mark.parametrize('listType', common_util.read_yaml('/extract.yaml')['settingPage'])
    @allure.title('配置血管类型和手术类型')
    def test_vessel_procedure(self,listType):
        allure.dynamic.description('配置血管类型和手术类型：删除前后数量对比')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('初始化Vessel数据'):
                initial_btn = app['血管内断层成像系统'].child_window(title="初始化", control_type="Text",
                                                                          found_index=0)
                rect = initial_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                time.sleep(0.5)
            with allure.step('实际软件中的内容和需求的内容一致'):
                vessel_list = app['血管内断层成像系统'].child_window(auto_id="listBoxVessel", control_type="List")
                rect = vessel_list.rectangle().mid_point()
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=-10)
                vessel_type = vessel_list.texts()
                assert vessel_type== listType['list_Vessel']
            with allure.step('删除后的数量比原来少一个'):
                RCA_btn = app['血管内断层成像系统'].child_window(title="LCX OM2", control_type="ListItem")
                rect = RCA_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                del_btn1 = app['血管内断层成像系统'].child_window(title="删除", control_type="Text", found_index=0)
                rect = del_btn1.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                vessel_list = app['血管内断层成像系统'].child_window(auto_id="listBoxVessel", control_type="List")
                rect = vessel_list.rectangle().mid_point()
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=10)
                mouse.scroll(coords=(rect.x, rect.y), wheel_dist=10)
                vessel_type = vessel_list.texts()
                assert len(listType['list_Vessel'])==(len(vessel_type) + 1)

            with allure.step('再次初始化，恢复Vessel数据'):
                initial_btn = app['血管内断层成像系统'].child_window(title="初始化", control_type="Text",
                                                                          found_index=0)
                rect = initial_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()

            with allure.step('初始化Procedure数据'):
                initial_btn = app['血管内断层成像系统'].child_window(title="初始化", control_type="Text",
                                                                          found_index=1)
                rect = initial_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
            with allure.step('实际软件中的内容和需求的内容一致'):
                procedure_list = app['血管内断层成像系统'].child_window(auto_id="listBoxProcedure",control_type="List")
                procedure_type = procedure_list.texts()
                # 实际软件中的内容和给定的内容一致
                assert listType['list_Procedure']==procedure_type
            with allure.step('删除后的数量比原来少一个'):
                RCA_btn = app['血管内断层成像系统'].child_window(title="Follow-Up", control_type="ListItem")
                rect = RCA_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
                del_btn1 = app['血管内断层成像系统'].child_window(title="删除", control_type="Text", found_index=1)
                rect = del_btn1.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                procedure_list = app['血管内断层成像系统'].child_window(auto_id="listBoxProcedure",control_type="List")
                procedure_type = procedure_list.texts()
                # 删除后的数量比原来少一个
                assert len(listType['list_Procedure'])==(len(procedure_type) + 1)
            with allure.step('再次初始化，恢复Procedure数据'):
                initial_btn = app['血管内断层成像系统'].child_window(title="初始化", control_type="Text",
                                                                          found_index=1)
                rect = initial_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(0.5)
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
    @allure.title('设置语言类型')
    def test_langueType(self):
        allure.dynamic.description('设置语言类型')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('查看类型：中文和英语'):
                langueType = app['血管内断层成像系统'].child_window(auto_id="cmbLanguage", control_type="ComboBox")
                rect = langueType.rectangle().mid_point()
                mouse.move(coords=(rect.x, rect.y))
                content = langueType.texts()
                assert ['中文', '英语']== content
                for i in range(len(content)):
                    langueType.select(i)
                langueType.select(0)
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
    @allure.title('设置lumen类型')
    def test_lumenType(self):
        allure.dynamic.description('设置lumen类型')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('查看类型：面积和直径'):
                lumenType = app['血管内断层成像系统'].child_window(auto_id="cmbLumen", control_type="ComboBox")
                rect = lumenType.rectangle().mid_point()
                mouse.move(coords=(rect.x, rect.y))
                content = lumenType.texts()
                assert ['面积', '直径'] == content
                for i in range(len(content)):
                    lumenType.select(i)
                lumenType.select(0)
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

    @allure.title('设置时间')
    def test_show_timePane(self):
        allure.dynamic.description('设置时间')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('打开系统时间设置界面'):
                timeBtn = app['血管内断层成像系统'].child_window(title="设置时间", control_type="Text")
                rect = timeBtn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(2)
                app1 = pywinauto.Desktop()
                systemTime = app1.window(title_re='日期和时间')
                time.sleep(1)
                common_util.screen_shot('日期和时间设置界面')
                assert systemTime.exists()
                systemTime.close()
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

    @allure.title('打开工程师模式')
    def test_show_engineerMode(self):
        allure.dynamic.description('打开工程师模式')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('点击显示工程师模式按钮'):
                show_test = app['血管内断层成像系统'].child_window(title="显示工程师模式",auto_id="btnEngineerMode",
                                                                        control_type="Button")
                rect = show_test.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
            with allure.step('不输入密码，点击确定按钮'):

                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk",
                                                                     control_type="Button", found_index=0)
                rect = ok_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('不输入密码')
                content = app['提示']['pane'].texts()
                assert ['密码不正确'] == content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
            with allure.step('输入错误密码，点击确定按钮'):
                pwd_edit = app['血管内断层成像系统'].child_window(auto_id="pwd", control_type="Edit")
                pwd_edit.type_keys('6666')
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk",
                                                                control_type="Button", found_index=0)
                rect = ok_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                common_util.screen_shot('输入错误密码')
                content = app['提示']['pane'].texts()
                assert ['密码不正确'] == content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()

            with allure.step('输入正确密码，点击确定按钮'):
                pwd_edit = app['血管内断层成像系统'].child_window(auto_id="pwd", control_type="Edit")
                rect = pwd_edit.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                keyboard.send_keys('^a')
                time.sleep(0.5)
                keyboard.send_keys('{BACKSPACE}')
                time.sleep(0.5)
                pwd_edit.type_keys('14606c66')
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk",
                                                                control_type="Button", found_index=0)
                rect = ok_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                exit_test = app['血管内断层成像系统'].child_window(title="退出工程师模式",
                                                                        auto_id="btnEngineerMode",
                                                                        control_type="Button")
                assert exit_test.exists()
                time.sleep(1)
                common_util.screen_shot('输入正确密码')
            with allure.step('打开工程师界面'):
                show_test = app['血管内断层成像系统'].child_window(title="工程师", auto_id="btnOpenEngineer",
                                                                        control_type="Button")
                rect = show_test.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                test_pane = app['血管内断层成像系统'].child_window(title="工程师", control_type="Window")
                time.sleep(1)
                common_util.screen_shot('工程师界面')
                assert test_pane.exists()
                test_pane.close()
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

    @allure.title('显示NVDIA控制面板')
    def test_show_nvdiaPane(self):
        allure.dynamic.description('工程师模式下，显示NVDIA控制面板')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('点击NVDIA控制面板按钮'):
                nvdia_Btn = app['血管内断层成像系统'].child_window(title="NVDIA控制面板", control_type="Text")
                rect = nvdia_Btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(2)
                app1 = pywinauto.Desktop()
                nvdia = app1.window(title_re='NVIDIA Control Panel')
                time.sleep(1)
                common_util.screen_shot('nvdia面板界面')
                assert nvdia.exists()
                nvdia.close()

            with allure.step('退出工程师模式后需要输入密码'):
                time.sleep(3)
                exit_test = app['血管内断层成像系统'].child_window(title="退出工程师模式", auto_id="btnEngineerMode", control_type="Button")
                rect = exit_test.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                nvdia_Btn = app['血管内断层成像系统'].child_window(title="NVDIA控制面板", control_type="Text")
                rect = nvdia_Btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('退出工程师后需要密码')
                cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel", control_type="Button")
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

    @allure.title('显示直方图')
    def test_showHistogram(self):
        allure.dynamic.description('显示直方图:查看图像界面、扫描界面')
        try:
            app = common_util.connect_application()
            common_util.back_patientListPage()
            patient_list = app['血管内断层成像系统']['ListView']
            time.sleep(1)
            if len(patient_list.texts()) == 0:
                common_util.import_testdata()
            common_util.back_systemSettingPage()
            with allure.step('勾选直方图'):
                histogram = app['血管内断层成像系统'].child_window(title="显示直方图", control_type="Text",
                                                                        found_index=0)
                rect = histogram.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                ok_btn = app['血管内断层成像系统'].child_window(title="确认", control_type="Text")
                rect = ok_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
            with allure.step('查看图像界面显示直方图'):
                patient_list = app['血管内断层成像系统'].child_window(title="F_2.Models.PatientInfo",
                                                                           control_type="DataItem",
                                                                           found_index=0)
                patient_list.click_input()
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk",
                                                                     control_type="Button")
                ok_btn.click()
                time.sleep(1)
                look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=0)
                rect = look_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                histogramPane = app['血管内断层成像系统'].child_window(auto_id="histogramControl",
                                                                            control_type="Custom")

                time.sleep(1)
                common_util.screen_shot('查看图像界面显示直方图')
                assert histogramPane.is_visible()
                time.sleep(1)
            with allure.step('扫描界面显示直方图'):
                add_btn = app['血管内断层成像系统'].child_window(auto_id="addOCT", control_type="Button")
                rect = add_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))

                histogramPane = app['血管内断层成像系统'].child_window(auto_id="histogramControl",
                                                                            control_type="Custom")
                time.sleep(1)
                common_util.screen_shot('扫描界面显示直方图')
                assert histogramPane.is_visible()
                common_util.back_systemSettingPage()
                histogram = app['血管内断层成像系统'].child_window(title="显示直方图", control_type="Text",
                                                                   found_index=0)
                rect = histogram.rectangle().mid_point()
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

    # @pytest.mark.skip(1)
    @allure.title('硬件自检')
    def test_selfTest(self):
        allure.dynamic.description('硬件自检')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('点击硬件自检按钮'):
                selfTest = app['血管内断层成像系统'].child_window(title="硬件自检", auto_id="btnSelfTest", control_type="Button")
                rect = selfTest.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button").wait(wait_for='exists', timeout=100)
                time.sleep(1)
                common_util.screen_shot('自检结果')
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

    @allure.title('图像配置')
    def test_imageSet(self):
        allure.dynamic.description('图像配置相关设置:标记颜色，线宽，断点大小，图像颜色，样式')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('标记颜色'):
                Image_conf_btn = app['血管内断层成像系统'].child_window(title="图像配置", control_type="TabItem")
                rect = Image_conf_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                markColor = app['血管内断层成像系统'].child_window(auto_id="comColor", control_type="ComboBox")
                content = markColor.texts()
                assert ['随机色', '紫色', '黄色', '蓝色', '绿色', '青色']==content
                for i in range(len(content)):
                    markColor.select(i)
                markColor.select(0)
            with allure.step('线宽'):
                lineWidth = app['血管内断层成像系统'].child_window(auto_id="comLineWidth", control_type="ComboBox")
                content = lineWidth.texts()
                assert ['1', '2', '3', '4']== content
                for i in range(len(content)):
                    lineWidth.select(i)
                lineWidth.select(2)
            with allure.step('断点大小'):
                point = app['血管内断层成像系统'].child_window(auto_id="comPoint", control_type="ComboBox")
                content = point.texts()
                assert ['1', '2', '3', '4']== content
                for i in range(len(content)):
                    point.select(i)
                point.select(2)
            with allure.step('图像颜色'):
                color = app['血管内断层成像系统'].child_window(auto_id="comPicColor", control_type="ComboBox")
                content = color.texts()
                assert ['黑白', '黄褐']== content
                for i in range(len(content)):
                    color.select(i)
                color.select(1)
            with allure.step('样式'):
                type = app['血管内断层成像系统'].child_window(auto_id="comStyle", control_type="ComboBox")
                content = type.texts()
                assert ['无', '基准点', '边缘']== content
                for i in range(len(content)):
                    type.select(i)
                type.select(1)
            time.sleep(1)
            common_util.screen_shot('设置后的结果')
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

    @allure.title('支架配置')
    def test_stentSet(self):
        allure.dynamic.description('支架配置:值范围、正常颜色和异常颜色')
        try:
            app = common_util.connect_application()
            common_util.back_systemSettingPage()
            with allure.step('设置值：最大1 μm、最小300 μm'):
                Bracket_conf_btn = app['血管内断层成像系统'].child_window(title="支架配置", control_type="TabItem")
                rect = Bracket_conf_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                stentRange = app['血管内断层成像系统'].child_window(auto_id="sliderStent", control_type="Slider")
                rect = stentRange.rectangle().mid_point()
                assert stentRange.min_value()== 1.0
                assert stentRange.max_value()== 300.0
                stentRange.set_value(150)
                mouse.press(coords=(rect.x, rect.y))
                mouse.move(coords=(rect.x - 500, rect.y))
                setValue = app['血管内断层成像系统']['Static6']
                assert ['1 μm']== setValue.texts()
                mouse.move(coords=(rect.x + 800, rect.y))
                mouse.release(coords=(rect.x + 800, rect.y))
                setValue = app['血管内断层成像系统']['Static6']
                assert ['300 μm']== setValue.texts()
                stentRange.set_value(150)
                mouse.press(coords=(rect.x, rect.y))
                mouse.move(coords=(rect.x + 50, rect.y))
                mouse.release(coords=(rect.x + 50, rect.y))
                setValue = app['血管内断层成像系统']['Static6']
                list1 = [str(int(stentRange.value())) + ' μm']
                list2 = setValue.texts()
                assert list1== list2
            with allure.step('显示正常颜色设置面板'):
                normalBtn = app['血管内断层成像系统'].child_window(title=". . .", auto_id="btnSelColorNormal",
                                                                        control_type="Button")
                rect = normalBtn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                colorPane = app['血管内断层成像系统'].child_window(title="颜色", control_type="Window")
                time.sleep(1)
                common_util.screen_shot('颜色设置面板')
                assert colorPane.exists()
                colorPane.close()
            with allure.step('显示正常颜色设置面板'):
                abnormalBtn = app['血管内断层成像系统'].child_window(title=". . .", auto_id="btnSelColorAbNormal",
                                                                          control_type="Button")
                rect = abnormalBtn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                colorPane = app['血管内断层成像系统'].child_window(title="颜色", control_type="Window")
                time.sleep(1)
                common_util.screen_shot('颜色设置面板')
                assert colorPane.exists()
                colorPane.close()
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
