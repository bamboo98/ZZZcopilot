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
import os
import json
os.system('chcp 65001')

start_time = time.time()

async def main():
    print("！！！本项目开源免费，如果您遇到任何收费情况都属于被他人欺骗")
    print("！！！请勿购买任何收费版本，如已购买请立刻申请退款并举报商家")
    print("开源仓库地址https://github.com/bamboo98/ZenlessZoneZero-Copilot")
    print("请确保模拟器分辨率为1280x720,DPI为240")
    print("游戏设置镜头灵敏度:5  镜头自动跟随转动:关闭  游戏语言:简体中文")
    # 尝试打开version文件,获取当前build的commit hash
    try:
        with open("version", "r") as f:
            print("当前版本:", f.read())
    except:
        pass
    # Process实例化时不指定pid参数，默认使用当前进程PID，即os.getpid()
    p = psutil.Process()
    cpu_lst = p.cpu_affinity()
    if len(cpu_lst)>=4:
        cpu_lst = cpu_lst[-4:]
        print("使用CPU", cpu_lst)
        # 用最后4个CPU核心(13和14代的小核)
        p.cpu_affinity(cpu_lst)
    print("Maa框架开始初始化")
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
    maa_inst.register_action("DataStatistic", DataStatistic)
    print("MAA框架初始化完成,开始执行任务")
    print("拿命验收!启动!")
    print("队伍1号位建议上妮可,用比利步子迈大了可能定位会歪,2号位上一个跑得快的")

        
        
    await maa_inst.run_task("界面检测")
    


# class MyRecognizer(CustomRecognizer):
#     def analyze(
#         self, context, image, task_name, custom_param
#     ) -> Tuple[bool, RectType, str]:
#         return True, (0, 0, 100, 100), "Hello World!"



class DataStatistic(CustomAction):
    battle_restart = 0
    gold_get = 0
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        global start_time
        # 解码json参数
        par = json.loads(custom_param)
        match par["key"]:
            case "battle_restart":
                self.battle_restart += par["value"]
                print(f"战斗重启次数:{self.battle_restart}")
            case "gold_get":
                self.gold_get += par["value"]
                # 计算每小时获取率
                time_now = time.time()
                time_diff = time_now - start_time
                gold_per_hour = self.gold_get / time_diff * 3600
                print(f"累计丁尼获取:{self.gold_get}  本次运行:{int(gold_per_hour)}丁尼/小时")
            case _:
                pass
        return True
    def stop(self) -> None:
        pass

class NikoAttack(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        # 前进
        context.touch_down(0,233,411,50)
        time.sleep(0.10)
        # 闪避
        context.touch_down(1,1131,599,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.05)
        # 攻击
        context.touch_down(1,1011,535,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.05)
        # 切人
        context.touch_down(1,1131,463,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.05)
        context.touch_up(0)
        return True
    def stop(self) -> None:
        pass

class JustRun(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        time_scale = 1
        flag,rec,detail = context.run_recognition(context.cached_image(),"check_is_eren")
        if(flag):
            time_scale = 0.75
        # 前进
        context.touch_down(0,331,430,50) #大约42度左右
        time.sleep(0.05)
        # 闪避
        context.touch_down(1,1131,599,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(0.20*time_scale)
        # 闪避
        context.touch_down(1,1131,599,50)
        time.sleep(0.05)
        context.touch_up(1)
        time.sleep(3.1*time_scale)
        # 转向
        context.touch_move(0,233,386,50) #90度
        time.sleep(1.6*time_scale)
        context.touch_up(0)

        return True
    def stop(self) -> None:
        pass


# my_rec = MyRecognizer()
NikoAttack = NikoAttack()
JustRun = JustRun()
DataStatistic = DataStatistic()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"程序执行过程中发生错误: {e}")
        traceback.print_exc()
        input("按回车键退出...")