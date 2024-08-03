# -*- coding: UTF-8 -*-
from typing import Tuple

# python -m pip install maafw
from maa.define import RectType
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit

from maa.custom_recognizer import CustomRecognizer
from maa.custom_action import CustomAction

import maa
import asyncio
import time
import psutil
import traceback
import sys

async def main():
    user_path = "./"
    Toolkit.init_option(user_path)

    resource = Resource()
    await resource.load("./assets/resource/base")

    device_list = await Toolkit.adb_devices()
    if not device_list:
        print("未找到任何ADB设备")
        input("按任意键退出")
        sys.exit()

    # for demo, we just use the first device
    device = device_list[0]
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
    )
    await controller.connect()

    maa_inst = Instance()
    maa_inst.bind(resource, controller)
    
    if not maa_inst.inited:
        print("MAA框架初始化失败")
        input("按任意键退出")
        sys.exit()

    # maa_inst.register_recognizer("MyRec", my_rec)
    maa_inst.register_action("NikoAttack", NikoAttack)
    maa_inst.register_action("JustRun", JustRun)
    print("ZZZ!启动!")
    print("队伍1号位建议上妮可,用比利步子迈大了可能定位会歪,2号位上一个跑得快的")

    await maa_inst.run_task("界面检测")


# class MyRecognizer(CustomRecognizer):
#     def analyze(
#         self, context, image, task_name, custom_param
#     ) -> Tuple[bool, RectType, str]:
#         return True, (0, 0, 100, 100), "Hello World!"


class NikoAttack(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        # 前进
        context.touch_down(0,239,456,50)
        time.sleep(0.10)
        # 闪避
        context.touch_down(1,1119,636,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.05)
        # 攻击
        context.touch_down(1,1024,576,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.05)
        # 切人
        context.touch_down(1,1118,527,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.05)
        context.touch_up(0)
        return True
    def stop(self) -> None:
        pass

class JustRun(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        # 前进
        context.touch_down(0,315,519,50)
        time.sleep(0.05)
        # 闪避
        context.touch_down(1,1119,636,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.20)
        # 闪避
        context.touch_down(1,1119,636,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(3.1)
        # 转向
        context.touch_move(0,238,472,50)
        time.sleep(1.6)
        context.touch_up(0)

        return True
    def stop(self) -> None:
        pass


# my_rec = MyRecognizer()
NikoAttack = NikoAttack()
JustRun = JustRun()


if __name__ == "__main__":
    try:
        count = psutil.cpu_count()
        print(f"逻辑cpu的数量是{count}")
        # Process实例化时不指定pid参数，默认使用当前进程PID，即os.getpid()
        p = psutil.Process()
        cpu_lst = p.cpu_affinity()
        if len(cpu_lst)>=4:
            cpu_lst = cpu_lst[-4:]
            print("使用CPU", cpu_lst)
            # 用最后4个CPU核心(13和14代的小核)
            p.cpu_affinity(cpu_lst)
        asyncio.run(main())
    except Exception as e:
        print(f"程序执行过程中发生错误: {e}")
        traceback.print_exc()
        input("按回车键退出...")