#!/usr/bin/env python3
"""
测试ChromeDriver修复的脚本
"""
import sys
import os
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

def test_chromedriver_setup():
    """测试ChromeDriver设置"""
    print(f"{Fore.CYAN}测试ChromeDriver设置...")
    
    try:
        from utils import Utils
        import platform
        
        # 显示系统信息
        system = platform.system().lower()
        print(f"操作系统: {system}")
        print(f"Python版本: {sys.version}")
        
        # 清理缓存
        print(f"\n{Fore.YELLOW}清理webdriver_manager缓存...")
        Utils.clear_webdriver_cache()
        
        # 获取ChromeDriver路径
        print(f"\n{Fore.YELLOW}获取ChromeDriver路径...")
        driver_path = Utils.get_chromedriver_path()
        
        if driver_path and os.path.exists(driver_path):
            print(f"{Fore.GREEN}✓ ChromeDriver路径获取成功: {driver_path}")
            
            # 检查文件权限
            if os.access(driver_path, os.R_OK):
                print(f"{Fore.GREEN}✓ ChromeDriver文件可读")
            else:
                print(f"{Fore.RED}✗ ChromeDriver文件不可读")
                return False
                
            if os.access(driver_path, os.X_OK):
                print(f"{Fore.GREEN}✓ ChromeDriver文件可执行")
            else:
                print(f"{Fore.RED}✗ ChromeDriver文件不可执行")
                return False
            
            return True
        else:
            print(f"{Fore.RED}✗ 无法获取有效的ChromeDriver路径")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}✗ 测试失败: {e}")
        return False

def test_selenium_setup():
    """测试Selenium设置"""
    print(f"\n{Fore.CYAN}测试Selenium设置...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from utils import Utils
        
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 获取ChromeDriver路径
        driver_path = Utils.get_chromedriver_path()
        
        if not driver_path or not os.path.exists(driver_path):
            print(f"{Fore.RED}✗ ChromeDriver路径无效")
            return False
        
        # 创建服务
        service = Service(driver_path)
        
        # 创建WebDriver实例
        print(f"{Fore.YELLOW}创建WebDriver实例...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 测试基本功能
        print(f"{Fore.YELLOW}测试基本功能...")
        driver.get("https://www.baidu.com")
        title = driver.title
        print(f"页面标题: {title}")
        
        # 关闭浏览器
        driver.quit()
        print(f"{Fore.GREEN}✓ Selenium设置测试成功")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ Selenium设置测试失败: {e}")
        return False

def main():
    """主函数"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}    ChromeDriver修复测试")
    print(f"{Fore.CYAN}{'='*60}")
    
    # 测试ChromeDriver设置
    if not test_chromedriver_setup():
        print(f"\n{Fore.RED}ChromeDriver设置测试失败！")
        return False
    
    # 测试Selenium设置
    if not test_selenium_setup():
        print(f"\n{Fore.RED}Selenium设置测试失败！")
        return False
    
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}✓ 所有测试通过！ChromeDriver修复成功！")
    print(f"{Fore.CYAN}{'='*60}")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
