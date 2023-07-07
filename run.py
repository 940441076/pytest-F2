# -*- coding: utf-8 -*-
# @Time ： 2023/5/31 11:25
# @Auth ： 醉在深海里的鱼🐟
# @Motto:  洗洗睡吧，梦里啥都有
import time,os
import pytest
import time
from common import common_util
import threading
import pyautogui



if __name__ == '__main__':
    pass
    time.sleep(3)
    pytest.main()
    time.sleep(1)
    os.system('allure generate ./result/temp -o ./result/report --clean')
    time.sleep(2)
    common_util.set_windows_title()
    time.sleep(0.5)
    common_util.set_report_name()
    time.sleep(0.5)
    common_util.set_report_env_on_html()
    time.sleep(1)
    threading.Thread(target=common_util.open_report, daemon=True).start()
    time.sleep(6)
    pyautogui.screenshot('result/result.jpg')
    time.sleep(1)
    common_util.kill_app()
    common_util.kill_allure_serve()
    common_util.send_mail()
    common_util.send_dingtalk()


# git clone https://github.com/940441076/pytest-VM1.git
# git clone https://github.com/940441076/pytest-F2.git
