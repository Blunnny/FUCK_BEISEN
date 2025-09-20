#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单选题自动化测试脚本
用于测试单选题自动化功能
"""

from single_choice_automation import SingleChoiceAutomation
from colorama import init, Fore

# 初始化colorama
init(autoreset=True)

def test_single_choice():
    """测试单选题自动化功能"""
    try:
        print(f"{Fore.CYAN}开始测试单选题自动化功能...")
        
        # 创建自动化实例
        automation = SingleChoiceAutomation()
        
        # 测试配置加载
        print(f"{Fore.GREEN}✓ 配置加载成功")
        print(f"  题目数量: {len(automation.question_answers)}")
        print(f"  等待超时: {automation.wait_timeout}秒")
        
        # 测试浏览器驱动初始化
        if automation.driver:
            print(f"{Fore.GREEN}✓ 浏览器驱动初始化成功")
        else:
            print(f"{Fore.RED}✗ 浏览器驱动初始化失败")
            return False
        
        # 测试按钮处理器初始化
        if automation.button_handler:
            print(f"{Fore.GREEN}✓ 按钮处理器初始化成功")
        else:
            print(f"{Fore.RED}✗ 按钮处理器初始化失败")
            return False
        
        print(f"\n{Fore.GREEN}所有测试通过！单选题自动化功能准备就绪。")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}测试失败: {e}")
        return False
    finally:
        if 'automation' in locals() and automation.driver:
            automation.driver.quit()

if __name__ == "__main__":
    test_single_choice()
