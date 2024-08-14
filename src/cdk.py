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

import os
import asyncio
import time
import psutil
import traceback
import sys

# 全局变量传参,貌似也可以直接run_task去传参,懒得改了,能跑就行
next_cdk = ""

async def main():
    global next_cdk  # 声明使用全局变量
    print("！！！本项目开源免费，如果您遇到任何收费情况都属于被他人欺骗")
    print("！！！请勿购买任何收费版本，如已购买请立刻申请退款并举报商家")
    print("开源仓库地址https://github.com/bamboo98/ZenlessZoneZero-Copilot")
    print("请确保模拟器分辨率为1280x720,DPI为240")
    print("游戏设置镜头灵敏度:5  镜头自动跟随转动:关闭  游戏语言:简体中文")
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

    maa_inst.register_action("py_input", py_input)
    print("MAA框架初始化完成,开始执行任务")
    print("开始兑换CDK,请进入游戏输入兑换码的界面")

    # 加载文件cdk.txt,一行一个cdk
    try:
        with open(os.path.join("cdk.txt"), "r") as f:
            cdk = f.read().splitlines()
            print("共有", len(cdk), "个CDK")
    except FileNotFoundError:
        print("未找到cdk.txt文件，请将兑换码放置在cdk.txt中，每行一个CDK")

    # 打开或创建cdkused.txt文件
    cdk_log = open(os.path.join("cdkused.txt"), "a+")

    print("已兑换完成的CDK会记录在cdkused.txt中")
        
    # 逐行输出数组
    for line in cdk:
        await maa_inst.run_task("清除文本")
        await maa_inst.run_task("选中输入框")
        next_cdk = line
        await maa_inst.run_task("输入文本")
        await maa_inst.run_task("点击确认兑换")
        time.sleep(1)
        ret=await maa_inst.run_recognition("兑换成功")
        if ret!=None:
            print("SUCCESS:"+next_cdk)
            cdk_log.write("成功:"+next_cdk+'\n')
            cdk_log.flush()
        else:
            ret=await maa_inst.run_recognition("兑换码同类型")
            if ret!=None:
                print("SAMEUSE:"+next_cdk)
                cdk_log.write("已使用同类型:"+next_cdk+'\n')
                cdk_log.flush()
            else:
                ret=await maa_inst.run_recognition("兑换码已被使用")
                if ret!=None:
                    print("USED:"+next_cdk)
                    cdk_log.write("已使用:"+next_cdk+'\n')
                    cdk_log.flush()
                else:
                    ret=await maa_inst.run_recognition("兑换码无效")
                    if ret!=None:
                        print("INVAILD:"+next_cdk)
                        cdk_log.write("无效:"+next_cdk+'\n')
                        cdk_log.flush()
                    else:
                        print("UNKNOW:"+next_cdk)
                        cdk_log.write("未知:"+next_cdk+'\n')
                        cdk_log.flush()
    cdk_log.close()
    print("任务执行完毕")
    


class py_input(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        global next_cdk  # 声明使用全局变量
        context.input_text(next_cdk)
        time.sleep(0.1)
        context.click( 628, 200) # 收回输入焦点
        return True
    def stop(self) -> None:
        pass


py_input = py_input()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"程序执行过程中发生错误: {e}")
        traceback.print_exc()
        input("按回车键退出...")