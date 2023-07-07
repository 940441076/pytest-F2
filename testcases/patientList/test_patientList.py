# -*- coding: utf-8 -*-
# @Time ： 2023/6/6 9:06
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有
import allure
import pytest
from pywinauto import mouse, keyboard
import time
from common import common_util
@pytest.mark.run(order=2)
@allure.feature('患者列表界面')
class Test_PatientListPage:

    @allure.title('新增患者')
    def test_register(self):
        allure.dynamic.description('新增患者')
        try:
            app= common_util.connect_application()
            common_util.del_all_patients()
            common_util.back_patientListPage()
            with allure.step('点击新增按钮'):
                new_patient = app['血管内断层成像系统'].child_window(title="新增患者", control_type="Text",
                                                                          found_index=1)
                rect = new_patient.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
            with allure.step('输入患者信息'):
                hospitalId = app['血管内断层成像系统'].child_window(auto_id="txtPatientID", control_type="Edit")
                hospitalId.type_keys('1')
                time.sleep(0.5)
                name = app['血管内断层成像系统'].child_window(auto_id="txtName", control_type="Edit")
                name.type_keys('test')
                time.sleep(0.5)
                age = app['血管内断层成像系统'].child_window(auto_id="txtOld", control_type="Edit")
                age.type_keys(100)
                time.sleep(0.5)
                sex_btn = app['血管内断层成像系统'].child_window(title="男", control_type="RadioButton")
                sex_btn.click()
                time.sleep(0.5)
                newOCT_btn = app['血管内断层成像系统'].child_window(auto_id="btnAddOCT", control_type="Button")
                newOCT_btn.click()
                time.sleep(2)
            with allure.step('返回到患者列表界面，判断患者数量为1'):
                common_util.back_patientListPage()
                patient_list = app['血管内断层成像系统']['ListView']
                assert len(patient_list.texts()) == 1
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

    @allure.title('删除患者')
    def test_delPatient(self):
        allure.dynamic.description('删除患者，判断提示框内容是否正确')
        try:
            app = common_util.connect_application()
            common_util.back_patientListPage()
            patient_list = app['血管内断层成像系统']['ListView']
            time.sleep(1)
            if len(patient_list.texts()) == 0:
                common_util.import_testdata()
                common_util.back_patientListPage()
            with allure.step('不选择患者，点击删除患者按钮'):
                del_patient = app['血管内断层成像系统'].child_window(title="删除患者", control_type="Text",
                                                                          found_index=1)
                rect = del_patient.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                common_util.screen_shot('未选择提示')
                content = app['提示']['Pane'].texts()[0]
                assert '请选择需要删除的患者！' == content
                ok_btn = app['提示'].child_window(title="确 定", auto_id="OkButton", control_type="Button")
                ok_btn.click()
                time.sleep(0.5)
            with allure.step('选择患者后，点击删除患者按钮，选择否'):
                patient_list = app['血管内断层成像系统'].child_window(title="F_2.Models.PatientInfo",
                                                                           control_type="DataItem", found_index=0)
                patient_list.click_input()
                time.sleep(1)
                del_patient = app['血管内断层成像系统'].child_window(title="删除患者", control_type="Text",
                                                                     found_index=1)
                rect = del_patient.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                time.sleep(1)
                no_btn = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                no_btn.click()
                time.sleep(0.5)
                del_patient = app['血管内断层成像系统'].child_window(title="删除患者", control_type="Text",
                                                                     found_index=1)
                rect = del_patient.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                time.sleep(0.5)
                no_btn2 = app['提示'].child_window(title="否", auto_id="NoButton", control_type="Button")
                no_btn2.click()
                time.sleep(0.5)
            with allure.step('选择一个患者后，点击删除患者按钮，选择是，判断提示框内容'):
                del_patient = app['血管内断层成像系统'].child_window(title="删除患者", control_type="Text",found_index=1)
                rect = del_patient.rectangle().mid_point()
                mouse.click(coords=(rect.x, rect.y))
                content = app['提示']['Pane'].texts()[0]
                time.sleep(1)
                common_util.screen_shot('删除提示一')
                assert '确定要删除吗？' == content
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                time.sleep(1)
                common_util.screen_shot('删除提示二')
                content = app['提示']['Pane'].texts()[0]
                assert '删除后不可恢复，确定要删除吗？' == content
                is_btn = app['提示'].child_window(title="是", auto_id="YesButton", control_type="Button")
                is_btn.click()
                time.sleep(1)
                patient_list = app['血管内断层成像系统']['ListView']
                assert len(patient_list.texts()) == 0
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
    @allure.title('筛选和条件搜索')
    def test_filter_search(self):
        allure.dynamic.description('筛选类型后，输入不同的关键词搜索，对比结果')
        try:
            app = common_util.connect_application()
            common_util.del_all_patients()
            common_util.import_testdata(index=1)
            time.sleep(2)
            common_util.back_patientListPage()
            with allure.step('选择不同类型，判断筛选结果'):
                OCT_type = app['血管内断层成像系统'].child_window(auto_id="cmbType", control_type="ComboBox")
                type = OCT_type.texts()
                for i in range(len(type)):
                    OCT_type.select(i + 1)
                    time.sleep(1)
                    if type[i] == 'ALL':
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        assert len(patient_info) == 4
                        time.sleep(1)
                        common_util.screen_shot('未筛选时结果')
                        search_edit = app['血管内断层成像系统'].child_window(auto_id="autoText",
                                                                                  control_type="Edit")
                        search_edit.type_keys('备注')
                        search_btn = app['血管内断层成像系统'].child_window(auto_id="btnSearch",
                                                                                 control_type="Button")
                        search_btn.click()
                        time.sleep(1)
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        mark = []
                        for j in range(len(patient_info)):
                            mark.append(patient_info[j][7])
                        assert mark == ['备注DSA', '备注OCT']
                        time.sleep(1)
                        common_util.screen_shot('ALL结果')
                        clear_btn = app['血管内断层成像系统'].child_window(auto_id="btnClear",
                                                                                control_type="Button")
                        clear_btn.click()
                        time.sleep(1)
                        search_edit.type_keys('测试')
                        search_btn = app['血管内断层成像系统'].child_window(auto_id="btnSearch",
                                                                                 control_type="Button")
                        search_btn.click()
                        time.sleep(1)
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        assert 0 == len(patient_info)
                        clear_btn = app['血管内断层成像系统'].child_window(auto_id="btnClear",
                                                                                control_type="Button")
                        clear_btn.click()
                        time.sleep(1)
                    elif type[i] == 'OCT':
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        assert len(patient_info)== 1
                        search_edit = app['血管内断层成像系统'].child_window(auto_id="autoText",
                                                                                  control_type="Edit")
                        search_edit.type_keys('备注')
                        search_btn = app['血管内断层成像系统'].child_window(auto_id="btnSearch",
                                                                                 control_type="Button")
                        search_btn.click()
                        time.sleep(1)
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        mark = []
                        for j in range(len(patient_info)):
                            mark.append(patient_info[j][7])
                        assert mark == ['备注OCT']
                        time.sleep(1)
                        common_util.screen_shot('OCT结果')
                        clear_btn = app['血管内断层成像系统'].child_window(auto_id="btnClear",
                                                                                control_type="Button")
                        clear_btn.click()
                        time.sleep(1)
                        search_edit.type_keys('测试')
                        search_btn = app['血管内断层成像系统'].child_window(auto_id="btnSearch",
                                                                                 control_type="Button")
                        search_btn.click()
                        time.sleep(1)
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        assert 0== len(patient_info)
                        clear_btn = app['血管内断层成像系统'].child_window(auto_id="btnClear",
                                                                                control_type="Button")
                        clear_btn.click()
                        time.sleep(1)
                    elif type[i] == 'OCT-DSA':
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        assert len(patient_info)== 3
                        search_edit = app['血管内断层成像系统'].child_window(auto_id="autoText",
                                                                                  control_type="Edit")
                        search_edit.type_keys('备注')
                        search_btn = app['血管内断层成像系统'].child_window(auto_id="btnSearch",
                                                                                 control_type="Button")
                        search_btn.click()
                        time.sleep(1)
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        mark = []
                        for j in range(len(patient_info)):
                            mark.append(patient_info[j][7])
                        assert mark==['备注DSA']
                        time.sleep(1)
                        common_util.screen_shot('OCT-DSA结果')
                        clear_btn = app['血管内断层成像系统'].child_window(auto_id="btnClear",
                                                                                control_type="Button")
                        clear_btn.click()
                        time.sleep(1)
                        search_edit.type_keys('测试')
                        content = search_edit.texts()
                        assert ['测试'] == content
                        search_btn = app['血管内断层成像系统'].child_window(auto_id="btnSearch",
                                                                                 control_type="Button")
                        search_btn.click()
                        time.sleep(1)
                        patient_list = app['血管内断层成像系统'].child_window(auto_id="dataGridPatientInfo",
                                                                                   control_type="DataGrid")
                        patient_info = patient_list.texts()
                        assert 0== len(patient_info)

                        clear_btn = app['血管内断层成像系统'].child_window(auto_id="btnClear",
                                                                                control_type="Button")
                        clear_btn.click()
                        time.sleep(1)
                        content = search_edit.texts()
                        assert [''] == content
                        time.sleep(1)
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

    @allure.title('选择一个患者查看')
    def test_selectOne(self):
        allure.dynamic.description('选择一个患者，点击确定按钮查看')
        try:
            app = common_util.connect_application()
            common_util.back_patientListPage()
            patient_list = app['血管内断层成像系统']['ListView']
            time.sleep(1)
            if len(patient_list.texts()) == 0:
                common_util.import_testdata()
                common_util.back_patientListPage()
            with allure.step('选择一个患者查看'):
                patient_list = app['血管内断层成像系统'].child_window(title="F_2.Models.PatientInfo",
                                                                           control_type="DataItem", found_index=0)
                patient_list.click_input()
                ok_btn = app['血管内断层成像系统'].child_window(title="确定", auto_id="btnOk",control_type="Button")
                ok_btn.click()
                time.sleep(1)
                look_btn = app['血管内断层成像系统'].child_window(title="查看", control_type="Text", found_index=0)
                assert look_btn.exists()
                time.sleep(1)
                common_util.back_patientListPage()
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
        allure.dynamic.description('患者列表界面，显示软件协议信息，且内容不可以修改和删除')
        try:
            app = common_util.connect_application()
            common_util.back_patientListPage()

            with allure.step('点击关于按钮'):
                show_btn = app['血管内断层成像系统']['Button2']
                show_btn.click()
                time.sleep(1)
                detail = app['血管内断层成像系统']['Document'].texts()[0]
                except_num = common_util.read_systemInfo()['info_text']
                except_key = common_util.read_systemInfo()['info_key']
                assert len(detail) == except_num
                assert except_key in detail
                common_util.add_text('结果：文本内容初始长度为{}，包含关键信息：{}'.format(except_num,except_key))
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

    @allure.title('关机(取消)')
    def test_shutDown_no(self):
        allure.dynamic.description('患者列表界面，点击取消按钮，应该不会关机')
        try:
            app = common_util.connect_application()
            common_util.back_patientListPage()
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
