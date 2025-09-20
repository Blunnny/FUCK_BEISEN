"""
工具函数模块
"""
import time
import random
import os
import shutil
import platform
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Utils:
    """工具函数类"""
    
    @staticmethod
    def random_delay(min_seconds: float = 0.5, max_seconds: float = 2.0):
        """随机延迟，模拟人类操作"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    @staticmethod
    def safe_click(driver, element: WebElement, retry_count: int = 3):
        """安全点击元素"""
        for attempt in range(retry_count):
            try:
                # 滚动到元素可见
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                Utils.random_delay(0.5, 1.0)
                
                # 等待元素可点击
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
                
                # 点击元素
                element.click()
                return True
            except Exception as e:
                print(f"点击失败，尝试 {attempt + 1}/{retry_count}: {e}")
                if attempt < retry_count - 1:
                    Utils.random_delay(1, 2)
                else:
                    return False
        return False
    
    @staticmethod
    def wait_for_element(driver, selector: str, timeout: int = 10) -> Optional[WebElement]:
        """等待元素出现"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            print(f"等待元素超时: {selector}")
            return None
    
    @staticmethod
    def wait_for_elements(driver, selector: str, timeout: int = 10) -> List[WebElement]:
        """等待多个元素出现"""
        try:
            elements = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            return elements
        except TimeoutException:
            print(f"等待元素超时: {selector}")
            return []
    
    @staticmethod
    def find_element_by_text(driver, text: str, tag: str = "*") -> Optional[WebElement]:
        """根据文本内容查找元素"""
        try:
            xpath = f"//{tag}[contains(text(), '{text}')]"
            return driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None
    
    @staticmethod
    def get_current_question_number(driver) -> int:
        """获取当前题目编号"""
        try:
            # 尝试从进度条获取题目编号
            progress_elements = driver.find_elements(By.CSS_SELECTOR, ".progress, .question-number, .current-question")
            for element in progress_elements:
                text = element.text.strip()
                if text.isdigit():
                    return int(text)
            
            # 尝试从URL获取题目编号
            url = driver.current_url
            if "question" in url.lower():
                import re
                match = re.search(r'question[=:]?(\d+)', url.lower())
                if match:
                    return int(match.group(1))
            
            return 1  # 默认返回1
        except Exception:
            return 1
    
    @staticmethod
    def print_progress(current: int, total: int, question_text: str = ""):
        """打印进度信息"""
        progress = (current / total) * 100 if total > 0 else 0
        print(f"\n进度: {current}/{total} ({progress:.1f}%)")
        if question_text:
            print(f"当前题目: {question_text[:50]}...")
        print("-" * 50)
    
    @staticmethod
    def clear_webdriver_cache():
        """清理webdriver_manager缓存"""
        try:
            # 获取用户主目录
            home_dir = os.path.expanduser("~")
            
            # 不同系统的缓存目录
            cache_dirs = []
            if platform.system().lower() == "windows":
                cache_dirs = [
                    os.path.join(home_dir, ".wdm"),
                    os.path.join(os.environ.get("LOCALAPPDATA", ""), "webdriver_manager"),
                ]
            else:
                cache_dirs = [
                    os.path.join(home_dir, ".wdm"),
                    os.path.join(home_dir, ".cache", "webdriver_manager"),
                ]
            
            # 清理缓存目录
            for cache_dir in cache_dirs:
                if os.path.exists(cache_dir):
                    print(f"清理缓存目录: {cache_dir}")
                    shutil.rmtree(cache_dir, ignore_errors=True)
            
            print("webdriver_manager缓存清理完成")
            return True
            
        except Exception as e:
            print(f"清理缓存失败: {e}")
            return False
    
    @staticmethod
    def get_chromedriver_path():
        """获取ChromeDriver路径"""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            import platform
            
            system = platform.system().lower()
            if system == "windows":
                return ChromeDriverManager(version="latest", os_type="win32").install()
            elif system == "linux":
                return ChromeDriverManager(version="latest", os_type="linux64").install()
            elif system == "darwin":
                return ChromeDriverManager(version="latest", os_type="mac64").install()
            else:
                return ChromeDriverManager().install()
                
        except Exception as e:
            print(f"获取ChromeDriver路径失败: {e}")
            return None
