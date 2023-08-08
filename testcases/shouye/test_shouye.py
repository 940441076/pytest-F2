# -*- coding: utf-8 -*-
# @Time ： 2023/6/6 9:06
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有
import allure
import pytest
from pywinauto import mouse,keyboard
import time
from common import common_util
import logging
log = logging.getLogger(__name__)
# @pytest.mark.skip('忽略')
@pytest.mark.run(order=5)
@allure.feature('首页界面')
class Test_ShowYePage:
    # @pytest.mark.test
    @allure.title('导入数据')
    def test_import(self):
        log.info('导入数据')
        allure.dynamic.description('导出已有的数据后，判断是否有导出成功的提示')
        try:
            app = common_util.connect_application()
            common_util.del_devices_file()
            common_util.del_all_patients()
            common_util.back_homePage()

            with allure.step('点击导入按钮'):
                import_btn = app['血管内断层成像系统'].child_window(title="导入", control_type="Text", found_index=1)
                rect = import_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                import_btn2 = app['血管内断层成像系统'].child_window(title="导入", control_type="Button").wait(wait_for='visible', timeout=50)
                import_btn2.click()
                time.sleep(1)
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button").wait(wait_for='exists', timeout=300)
                time.sleep(1)
                common_util.screen_shot('导入成功')
                content = app['提示']['Pane'].texts()[0]
                assert '数据导入完成！' == content
                ok_btn.click()
                time.sleep(1)
                log.info('导入完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到USB:rawdata')
    def test_export_usb_rawdata(self):
        log.info('导出USB:rawdata')
        allure.dynamic.description('导出USB:rawdata')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            with allure.step('开始导出'):
                export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
                export_btn.click()
                time.sleep(1)
                selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                    control_type="Button")
                selAll_btn.click()
                time.sleep(0.5)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                time.sleep(1)
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput", control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                time.sleep(0.5)
                type.select(0)
                time.sleep(1)
                common_util.screen_shot('导出rawdata')
                common_util.select_device_import(1)
                cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                    control_type="Button")
                cancel_btn.click()
                time.sleep(1)
                log.info('导出USB:rawdata完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到USB:tiff')
    def test_export_usb_tiff(self):
        log.info('导出USB:tiff')
        allure.dynamic.description('导出USB:tiff')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
            export_btn.click()
            time.sleep(1)
            selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                control_type="Button")
            selAll_btn.click()
            for i in range(4):
                time.sleep(1)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                       control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                type.select(1)
                time.sleep(1)
                if i == 0:
                    with allure.step('导出tiff,都不勾选'):
                        time.sleep(1)
                        common_util.screen_shot('都不勾选')
                        common_util.select_device_import(1)
                elif i == 1:
                    with allure.step('导出tiff,只勾选隐藏Lumne'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选隐藏Lumne')
                        common_util.select_device_import(1)
                elif i == 2:
                    with allure.step('导出tiff,只勾选纵切面'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选纵切面')
                        common_util.select_device_import(1)
                elif i == 3:
                    with allure.step('导出tiff,勾选隐藏Lumne和纵切面'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumne和纵切面')
                        common_util.select_device_import(1)
            time.sleep(1)
            cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                control_type="Button")
            cancel_btn.click()
            time.sleep(1)
            log.info('导出USB:tiff完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到USB:dicom')
    def test_export_usb_dicom(self):
        log.info('导出USB:dicom')
        allure.dynamic.description('导出USB:dicom')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
            export_btn.click()
            time.sleep(1)
            selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                control_type="Button")
            selAll_btn.click()
            for i in range(8):
                time.sleep(1)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                       control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                type.select(2)
                time.sleep(1)
                if i == 0:
                    with allure.step('导出dicom,都不勾选'):
                        time.sleep(1)
                        common_util.screen_shot('都不勾选')
                        common_util.select_device_import(1)
                elif i == 1:
                    with allure.step('导出dicom,只勾选隐藏Lumne'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选隐藏Lumne')
                        common_util.select_device_import(1)
                elif i == 2:
                    with allure.step('导出dicom,只勾选纵切面'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选纵切面')
                        common_util.select_device_import(1)
                elif i == 3:
                    with allure.step('导出dicom,只勾选匿名'):
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选匿名')
                        common_util.select_device_import(1)
                elif i == 4:
                    with allure.step('导出dicom,勾选隐藏Lumen和纵切面'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumen和纵切面')
                        common_util.select_device_import(1)
                elif i == 5:
                    with allure.step('导出dicom,勾选隐藏Lumen和匿名'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumen和匿名')
                        common_util.select_device_import(1)
                elif i == 6:
                    with allure.step('导出dicom,勾选纵切面和匿名'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选纵切面和匿名')
                        common_util.select_device_import(1)
                elif i == 7:
                    with allure.step('导出dicom,勾选隐藏Lumne、纵切面和匿名'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumne、纵切面和匿名')
                        common_util.select_device_import(1)
            time.sleep(1)
            cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                control_type="Button")
            cancel_btn.click()
            time.sleep(1)
            log.info('导出USB:dicom完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到USB:avi/jpg')
    def test_export_usb_avijpg(self):
        log.info('导出USB:avi/jpg')
        allure.dynamic.description('导出USB:avi/jpg')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
            export_btn.click()
            time.sleep(1)
            selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                control_type="Button")
            selAll_btn.click()
            for i in range(4):
                time.sleep(1)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                       control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                type.select(3)
                time.sleep(1)
                if i == 0:
                    with allure.step('导出avi/jpg,都不勾选'):
                        time.sleep(1)
                        common_util.screen_shot('都不勾选')
                        common_util.select_device_import(1)
                elif i == 1:
                    with allure.step('导出avi/jpg,只勾选隐藏Lumne'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选隐藏Lumne')
                        common_util.select_device_import(1)
                elif i == 2:
                    with allure.step('导出avi/jpg,只勾选纵切面'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选纵切面')
                        common_util.select_device_import(1)
                elif i == 3:
                    with allure.step('导出avi/jpg,勾选隐藏Lumne和纵切面'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumne和纵切面')
                        common_util.select_device_import(1)
            time.sleep(1)
            cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                control_type="Button")
            cancel_btn.click()
            time.sleep(1)
            log.info('导出USB:avi/jpg完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到local:rawdata')
    def test_export_local_rawdata(self):
        log.info('导出local:rawdata')
        allure.dynamic.description('导出local:rawdata')
        try:
            app = common_util.connect_application()
            common_util.open_engineerMode()
            common_util.back_homePage()
            with allure.step('开始导出'):
                export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
                export_btn.click()
                time.sleep(1)
                selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                    control_type="Button")
                selAll_btn.click()
                time.sleep(0.5)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                time.sleep(1)
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput", control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                type.select(0)
                time.sleep(1)
                common_util.screen_shot('导出rawdata')
                common_util.select_device_import(2)
                cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                    control_type="Button")
                cancel_btn.click()
                time.sleep(1)
                log.info('导出local:rawdata完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到local:tiff')
    def test_export_local_tiff(self):
        log.info('导出local:tiff')
        allure.dynamic.description('导出local:tiff')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
            export_btn.click()
            time.sleep(1)
            selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                control_type="Button")
            selAll_btn.click()
            for i in range(4):
                time.sleep(1)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                time.sleep(0.5)
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                       control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                type.select(1)
                time.sleep(1)
                if i == 0:
                    with allure.step('导出tiff,都不勾选'):
                        time.sleep(1)
                        common_util.screen_shot('都不勾选')
                        common_util.select_device_import(2)
                elif i == 1:
                    with allure.step('导出tiff,只勾选隐藏Lumne'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选隐藏Lumne')
                        common_util.select_device_import(2)
                elif i == 2:
                    with allure.step('导出tiff,只勾选纵切面'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选纵切面')
                        common_util.select_device_import(2)
                elif i == 3:
                    with allure.step('导出tiff,勾选隐藏Lumne和纵切面'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumne和纵切面')
                        common_util.select_device_import(2)
            time.sleep(1)
            cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                control_type="Button")
            cancel_btn.click()
            time.sleep(1)
            log.info('导出local:tiff完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到local:dicom')
    def test_export_local_dicom(self):
        log.info('导出local:dicom')
        allure.dynamic.description('导出local:dicom')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
            export_btn.click()
            time.sleep(1)
            selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                control_type="Button")
            selAll_btn.click()
            for i in range(8):
                time.sleep(1)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                time.sleep(0.5)
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                       control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                type.select(2)
                time.sleep(1)
                if i == 0:
                    with allure.step('导出dicom,都不勾选'):
                        time.sleep(1)
                        common_util.screen_shot('都不勾选')
                        common_util.select_device_import(2)
                elif i == 1:
                    with allure.step('导出dicom,只勾选隐藏Lumne'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选隐藏Lumne')
                        common_util.select_device_import(2)
                elif i == 2:
                    with allure.step('导出dicom,只勾选纵切面'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选纵切面')
                        common_util.select_device_import(2)
                elif i == 3:
                    with allure.step('导出dicom,只勾选匿名'):
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选匿名')
                        common_util.select_device_import(2)
                elif i == 4:
                    with allure.step('导出dicom,勾选隐藏Lumen和纵切面'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumen和纵切面')
                        common_util.select_device_import(2)
                elif i == 5:
                    with allure.step('导出dicom,勾选隐藏Lumen和匿名'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumen和匿名')
                        common_util.select_device_import(2)
                elif i == 6:
                    with allure.step('导出dicom,勾选纵切面和匿名'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选纵切面和匿名')
                        common_util.select_device_import(2)
                elif i == 7:
                    with allure.step('导出dicom,勾选隐藏Lumne、纵切面和匿名'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_name = app['血管内断层成像系统'].child_window(title="匿名", control_type="Text",
                                                                           found_index=0)
                        rect = hide_name.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumne、纵切面和匿名')
                        common_util.select_device_import(2)
            time.sleep(1)
            cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                control_type="Button")
            cancel_btn.click()
            time.sleep(1)
            log.info('导出local:dicom完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('导出数据到local:avi/jpg')
    def test_export_local_avijpg(self):
        log.info('导出local:avi/jpg')
        allure.dynamic.description('导出local:avi/jpg')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            export_btn = app['血管内断层成像系统'].child_window(auto_id="btnOutput", control_type="Button")
            export_btn.click()
            time.sleep(1)
            selAll_btn = app['血管内断层成像系统'].child_window(title="全选", auto_id="btnSelectAll",
                                                                control_type="Button")
            selAll_btn.click()
            for i in range(4):
                time.sleep(1)
                next_btn = app['血管内断层成像系统'].child_window(title="下一步", auto_id="btnOutput",
                                                                  control_type="Button")
                next_btn.click()
                time.sleep(0.5)
                app['血管内断层成像系统'].child_window(title="导出", auto_id="btnOutput",
                                                       control_type="Button").wait(
                    wait_for='enabled', timeout=100)
                type = app['血管内断层成像系统'].child_window(auto_id="comType", control_type="ComboBox").wait(
                    wait_for='exists', timeout=10)
                type.select(3)
                time.sleep(1)
                if i == 0:
                    with allure.step('导出avi/jpg,都不勾选'):
                        time.sleep(1)
                        common_util.screen_shot('都不勾选')
                        common_util.select_device_import(2)
                elif i == 1:
                    with allure.step('导出avi/jpg,只勾选隐藏Lumne'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选隐藏Lumne')
                        common_util.select_device_import(2)
                elif i == 2:
                    with allure.step('导出avi/jpg,只勾选纵切面'):
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('只勾选纵切面')
                        common_util.select_device_import(2)
                elif i == 3:
                    with allure.step('导出avi/jpg,勾选隐藏Lumne和纵切面'):
                        hide_lumen = app['血管内断层成像系统'].child_window(title="隐藏Lumen", control_type="Text",
                                                                            found_index=0)
                        rect = hide_lumen.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        hide_zong = app['血管内断层成像系统'].child_window(title="纵切面", control_type="Text",
                                                                           found_index=0)
                        rect = hide_zong.rectangle().mid_point()
                        mouse.click(coords=(rect.x, rect.y))
                        time.sleep(1)
                        common_util.screen_shot('勾选隐藏Lumne和纵切面')
                        common_util.select_device_import(2)
            time.sleep(1)
            cancel_btn = app['血管内断层成像系统'].child_window(title="取消", auto_id="btnCancel",
                                                                control_type="Button")
            cancel_btn.click()
            time.sleep(1)
            common_util.exit_engineerMode()
            time.sleep(1)
            log.info('导出local:avi/jpg')
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
    @allure.title('验证注册字段限制条件')
    @pytest.mark.parametrize('caseInfo', common_util.read_yaml('/extract.yaml')['shouyePage'])
    def test_register(self, caseInfo):
        allure.dynamic.description(
            '住院号：包括英文大小写、下划线、横杠和阿拉伯数字\n患者姓名：包括中文、英文大小写、数字、间隔点、下划线、横线、括号和空格\n年龄：1-120')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            hosptialID = caseInfo["hosptialID"]
            patientName = caseInfo["patientName"]
            age = caseInfo["age"]
            hosptialID_real = ['Abc','123','_-','Abc123_-Abc123_-Abc1','','']
            patientName_real = ['姓名','Abc','123','_-','姓名Abc123_-1678921234','']
            age_real = ['1','120','1','','120','']


            register_btn = app['血管内断层成像系统'].child_window(title="新增患者", auto_id="btnRegist",
                                                                  control_type="Button")
            rect = register_btn.rectangle().mid_point()
            mouse.click(coords=(rect.x, rect.y))
            time.sleep(1)

            with allure.step('验证住院号限制'):
                hospitalID__edit = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                for i in range(len(hosptialID)):
                    hospitalID__edit.type_keys(hosptialID[i])
                    time.sleep(1)
                    hospitalID__edit = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                    common_util.screen_shot('输入：{}，显示：{}'.format(hosptialID[i], hospitalID__edit.texts()[0]))
                    assert hospitalID__edit.texts()[0] ==hosptialID_real[i]
                    if hospitalID__edit.texts()[0] == '':
                        newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                        newOCT_btn.click()
                        time.sleep(1)
                        error_tip = app['血管内断层成像系统'].child_window(title="请输入字母、数字、下划线或横杠", auto_id="txtPatientIDTip",control_type="Text")
                        assert error_tip.exists()
                    keyboard.send_keys('^a')
                    time.sleep(0.5)
                    keyboard.send_keys('{VK_BACK}')
            with allure.step('验证姓名限制:需要手动输入间隔点和括号，程序无法模拟'):
                name_edit = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                for i in range(len(patientName)):
                    name_edit.type_keys(patientName[i])
                    time.sleep(1)
                    name_edit = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                    common_util.screen_shot('输入：{}，显示：{}'.format(patientName[i],name_edit.texts()[0]))
                    assert name_edit.texts()[0] == patientName_real[i]
                    if name_edit.texts()[0] == '':
                        newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                        newOCT_btn.click()
                        time.sleep(1)
                        error_tip = app['血管内断层成像系统'].child_window(title="请输入病人姓名", auto_id="txtNameTip",control_type="Text")
                        assert error_tip.exists()
                    keyboard.send_keys('^a')
                    time.sleep(0.5)
                    keyboard.send_keys('{VK_BACK}')
            with allure.step('验证年龄限制'):
                age_edit = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
                for i in range(len(age)):
                    age_edit.type_keys(age[i])
                    time.sleep(1)
                    age_edit = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
                    common_util.screen_shot('输入：{}，显示：{}'.format(age[i],age_edit.texts()[0]))
                    assert age_edit.texts()[0] == age_real[i]
                    keyboard.send_keys('^a')
                    time.sleep(0.5)
                    keyboard.send_keys('{VK_BACK}')
            with allure.step('验证年龄不输入也可以注册成功'):
                hospitalID__edit = app['血管内断层成像系统'].child_window(auto_id="txtPatientID",
                                                                          control_type="Edit")
                hospitalID__edit.type_keys('testID-age')
                time.sleep(1)
                name_edit = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                name_edit.type_keys('姓名-age')
                time.sleep(1)
                common_util.screen_shot('不输入年龄')
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                time.sleep(3)
                patientImage_btn = app['血管内断层成像系统'].child_window(auto_id="btnPatientImage",
                                                                          control_type="Button")
                time.sleep(1)
                common_util.screen_shot('跳转到扫描界面')
                assert patientImage_btn.exists()

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
    @allure.title('注册患者：住院号不存在')
    def test_register_noExisted(self):
        log.info('注册患者：住院号不存在')
        allure.dynamic.description('注册患者：住院号不存在，可以跳转到扫描界面')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            with allure.step('输入正确字段，可以注册成功'):
                regist_btn = app['血管内断层成像系统'].child_window(title="新增患者", auto_id="btnRegist",
                                                                    control_type="Button")
                rect = regist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                hospitalId = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                hospitalId.type_keys('testID')
                time.sleep(0.5)
                name = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                name.type_keys('testName')
                time.sleep(0.5)
                age = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
                age.type_keys(1)
                time.sleep(0.5)
                sex_btn = app['血管内断层成像系统'].child_window(title="女",auto_id="rbtnWoman",control_type="RadioButton")
                sex_btn.click()
                time.sleep(0.5)
                new_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                new_btn.click()
                time.sleep(3)
                common_util.screen_shot('注册完成跳转界面')
                info_hospitalId = app['血管内断层成像系统']['Static6']
                info_name = app['血管内断层成像系统']['Static10']
                info_sex = app['血管内断层成像系统']['Static14']
                assert info_hospitalId.texts() == ['testID']
                assert info_name.texts() == ['testName']
                assert info_sex.texts() == ['女']
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


    @allure.title('注册患者：住院号已存在')
    def test_register_existed(self):
        log.info('注册患者，住院号已存在')
        allure.dynamic.description('注册患者，住院号已存在，可以跳转到该患者图像界面')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            with allure.step('注册患者，住院号：existedID'):
                regist_btn = app['血管内断层成像系统'].child_window(title="新增患者", auto_id="btnRegist",
                                                                    control_type="Button")
                rect = regist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                hospitalId = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                hospitalId.type_keys('existedID')
                time.sleep(0.5)
                name = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                name.type_keys(1)
                time.sleep(0.5)
                age = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
                age.type_keys(1)
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                time.sleep(3)
                common_util.screen_shot('注册完成跳转界面')
                imglist_btn = app['血管内断层成像系统'].child_window(auto_id="btnPatientImage", control_type="Button")
                rect = imglist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(2)
                home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
                home_btn.click()
                time.sleep(1)
            with allure.step('再次注册患者，住院号：existedID'):
                regist_btn = app['血管内断层成像系统'].child_window(title="新增患者", auto_id="btnRegist",
                                                                    control_type="Button")
                rect = regist_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                hospitalId = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                hospitalId.type_keys('existedID')
                time.sleep(0.5)
                name = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                name.type_keys(1)
                time.sleep(0.5)
                age = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
                age.type_keys(1)
                time.sleep(0.5)
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                time.sleep(1)
                common_util.screen_shot('患者已存在提示')
                existed_tip = app['提示']['Pane']
                content = existed_tip.texts()[0]
                assert '该住院号已被注册过' in content
                no_btn = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                rect = no_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                rect = is_btn.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('已存在的患者图像列表界面')
                mark_ID = app['血管内断层成像系统'].child_window(title="existedID", auto_id="id", control_type="Text")
                assert mark_ID.exists() == True
            home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
            home_btn.click()
            time.sleep(1)
            log.info('注册患者，住院号已存在完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False

    @allure.title('选择已有')
    def test_choosePatient(self):
        log.info('选择已有')
        allure.dynamic.description('选择已有患者')
        try:
            app = common_util.connect_application()
            common_util.del_all_patients()
            common_util.back_homePage()
            with allure.step('不导入数据，点击选择已有按钮,患者列表为空'):
                select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist",
                                                                        control_type="Button")
                select_btn.click()
                time.sleep(2)
                patient_list = app['血管内断层成像系统']['ListView']
                time.sleep(1)
                common_util.screen_shot('患者列表为空')
                assert len(patient_list.texts()) ==0
                home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
                home_btn.click()
            with allure.step('导入一个数据后，点击选择已有按钮,患者列表数量为1'):
                common_util.import_testdata()
                time.sleep(1)
                select_btn = app['血管内断层成像系统'].child_window(title="选择患者", auto_id="btnSelExist",
                                                                        control_type="Button")
                select_btn.click()
                time.sleep(2)
                patient_list = app['血管内断层成像系统']['ListView']
                time.sleep(1)
                common_util.screen_shot('患者列表为1')
                assert len(patient_list.texts()) ==1
                home_btn = app['血管内断层成像系统'].child_window(auto_id="btnHome", control_type="Button")
                home_btn.click()
                time.sleep(2)
                log.info('选择已有完成！')
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
        log.info('关于软件使用协议')
        allure.dynamic.description('首页显示软件协议信息，且内容不可以修改和删除')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
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
                log.info('关于软件使用协议完成！')
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
        log.info('首页关机：取消')
        allure.dynamic.description('首页关机，点击取消按钮，应该不会关机')
        try:
            app = common_util.connect_application()
            common_util.back_homePage()
            with allure.step('点击关机按钮'):
                clsoe_btn = app['血管内断层成像系统'].child_window(auto_id="imgClose", control_type="Button")
                clsoe_btn.click()
                time.sleep(1)
                common_util.screen_shot('关机提示框')
                no_btn = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                no_btn.click()
                time.sleep(1)
                log.info('首页关机：取消完成！')
        except Exception as e:
            time.sleep(1)
            common_util.screen_shot('异常截图')
            time.sleep(1)
            common_util.kill_app()
            time.sleep(2)
            common_util.connect_application()
            common_util.add_text(str(e))
            assert False



