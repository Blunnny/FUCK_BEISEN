"""
按钮处理模块
用于处理进入答题区域前的各种按钮点击
"""
import time
import random
from typing import List, Optional, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from utils import Utils

class ButtonHandler:
    """按钮处理类"""
    
    def __init__(self, driver, config: Dict[str, Any] = None):
        self.driver = driver
        self.config = config or {}
        self.button_selectors = self.config.get("button_selectors", {})
        self.wait_timeout = self.config.get("wait_timeout", 10)
        self.retry_count = self.config.get("retry_count", 3)
    
    def find_button_by_text(self, text_variations: List[str], timeout: int = 5) -> Optional[WebElement]:
        """根据文本内容查找按钮"""
        for text in text_variations:
            try:
                # 尝试多种XPath模式
                xpath_patterns = [
                    f"//button[contains(text(), '{text}')]",
                    f"//input[@value='{text}']",
                    f"//a[contains(text(), '{text}')]",
                    f"//div[contains(text(), '{text}')]",
                    f"//span[contains(text(), '{text}')]",
                    f"//*[contains(text(), '{text}')]"
                ]
                
                for pattern in xpath_patterns:
                    try:
                        element = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, pattern))
                        )
                        if element and element.is_displayed():
                            return element
                    except TimeoutException:
                        continue
                        
            except Exception:
                continue
        
        return None
    
    def find_button_by_selector(self, selectors: List[str], timeout: int = 5) -> Optional[WebElement]:
        """根据CSS选择器查找按钮"""
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                if element and element.is_displayed():
                    return element
            except TimeoutException:
                continue
        return None
    
    def click_button(self, element: WebElement, button_name: str = "按钮") -> bool:
        """安全点击按钮"""
        try:
            print(f"正在点击 {button_name}...")
            
            # 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            Utils.random_delay(0.5, 1.0)
            
            # 等待元素可点击
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(element))
            
            # 尝试点击
            try:
                element.click()
            except Exception:
                # 如果普通点击失败，尝试JavaScript点击
                self.driver.execute_script("arguments[0].click();", element)
            
            print(f"{button_name} 点击成功")
            Utils.random_delay(1, 2)
            return True
            
        except Exception as e:
            print(f"点击 {button_name} 失败: {e}")
            return False
    
    def click_next_button(self) -> bool:
        """点击下一步按钮"""
        next_texts = [
            "下一步", "Next", "继续", "Continue", "下一步>", ">",
            "开始答题", "开始测试", "Start", "开始", "进入测试",
            "我知道了", "了解", "明白", "好的", "OK", "确定"
        ]
        
        next_selectors = [
            ".next-button", ".btn-next", ".continue-button", ".start-button",
            "button[class*='next']", "button[class*='continue']", "button[class*='start']",
            "input[value*='下一步']", "input[value*='Next']", "input[value*='开始']",
            ".btn-primary", ".btn-success", "button[type='submit']"
        ]
        
        # 先尝试按文本查找
        button = self.find_button_by_text(next_texts)
        if button:
            return self.click_button(button, "下一步按钮")
        
        # 再尝试按选择器查找
        button = self.find_button_by_selector(next_selectors)
        if button:
            return self.click_button(button, "下一步按钮")
        
        print("未找到下一步按钮")
        return False
    
    def click_start_button(self) -> bool:
        """点击开始答题按钮"""
        start_texts = [
            "开始答题", "开始测试", "Start Test", "开始", "Start",
            "进入答题", "进入测试", "开始作答", "开始评估"
        ]
        
        start_selectors = [
            ".start-button", ".btn-start", ".test-start", ".begin-button",
            "button[class*='start']", "button[class*='begin']", "button[class*='test']",
            "input[value*='开始']", "input[value*='Start']", "input[value*='进入']"
        ]
        
        # 先尝试按文本查找
        button = self.find_button_by_text(start_texts)
        if button:
            return self.click_button(button, "开始答题按钮")
        
        # 再尝试按选择器查找
        button = self.find_button_by_selector(start_selectors)
        if button:
            return self.click_button(button, "开始答题按钮")
        
        print("未找到开始答题按钮")
        return False
    
    def click_enter_test_button(self) -> bool:
        """点击进入试卷按钮（带5秒等待）"""
        print("查找进入试卷按钮...")
        
        # 专门针对进入试卷按钮的选择器
        enter_test_selectors = [
            ".phoenix-button.wraper--primary",  # 主要按钮样式
            ".phoenix-button.wraper--middle",   # 中等大小按钮
            ".phoenix-button.wraper",           # 通用按钮包装器
            "div.phoenix-button[class*='primary']",  # 主要按钮
            "div.phoenix-button[class*='middle']",   # 中等按钮
            ".phoenix-button.content",          # 按钮内容
            "div[class*='phoenix-button'][class*='primary']",  # 组合选择器
        ]
        
        # 尝试按选择器查找按钮
        button = None
        for selector in enter_test_selectors:
            try:
                print(f"尝试选择器: {selector}")
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and "进入试卷" in element.text:
                        button = element
                        print(f"找到进入试卷按钮: {element.text}")
                        break
                if button:
                    break
            except Exception as e:
                print(f"选择器 {selector} 查找失败: {e}")
                continue
        
        # 如果按选择器没找到，尝试按文本查找
        if not button:
            print("按选择器未找到，尝试按文本查找...")
            button = self.find_button_by_text(["进入试卷", "进入测试", "开始答题"])
        
        if not button:
            print("未找到进入试卷按钮")
            return False
        
        # 智能等待按钮可点击
        print("等待按钮可点击...")
        max_wait_time = 10  # 最大等待10秒
        wait_interval = 0.5  # 每0.5秒检查一次
        waited_time = 0
        
        while waited_time < max_wait_time:
            try:
                # 检查按钮是否可点击
                if button.is_enabled() and button.is_displayed():
                    # 尝试点击，如果成功就跳出循环
                    try:
                        WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(button))
                        print(f"按钮在 {waited_time:.1f} 秒后变为可点击")
                        break
                    except TimeoutException:
                        pass
                
                time.sleep(wait_interval)
                waited_time += wait_interval
                
                # 每2秒打印一次进度
                if int(waited_time) % 2 == 0 and waited_time > 0:
                    print(f"已等待 {waited_time:.1f} 秒...")
                    
            except Exception as e:
                print(f"检查按钮状态时出错: {e}")
                time.sleep(wait_interval)
                waited_time += wait_interval
        
        if waited_time >= max_wait_time:
            print("按钮等待超时，尝试强制点击")
        
        # 点击按钮
        return self.click_button(button, "进入试卷按钮")
    
    def click_confirm_button(self) -> bool:
        """点击确认按钮"""
        confirm_texts = [
            "确认", "确定", "Confirm", "OK", "好的", "我知道了",
            "明白", "了解", "同意", "Agree", "接受", "Accept"
        ]
        
        confirm_selectors = [
            ".confirm-button", ".btn-confirm", ".ok-button", ".agree-button",
            "button[class*='confirm']", "button[class*='ok']", "button[class*='agree']",
            "input[value*='确认']", "input[value*='确定']", "input[value*='OK']"
        ]
        
        # 先尝试按文本查找
        button = self.find_button_by_text(confirm_texts)
        if button:
            return self.click_button(button, "确认按钮")
        
        # 再尝试按选择器查找
        button = self.find_button_by_selector(confirm_selectors)
        if button:
            return self.click_button(button, "确认按钮")
        
        print("未找到确认按钮")
        return False
    
    def click_skip_button(self) -> bool:
        """点击跳过按钮"""
        skip_texts = [
            "跳过", "Skip", "略过", "Pass", "下一题", "继续"
        ]
        
        skip_selectors = [
            ".skip-button", ".btn-skip", ".pass-button", ".next-button",
            "button[class*='skip']", "button[class*='pass']", "button[class*='next']"
        ]
        
        # 先尝试按文本查找
        button = self.find_button_by_text(skip_texts)
        if button:
            return self.click_button(button, "跳过按钮")
        
        # 再尝试按选择器查找
        button = self.find_button_by_selector(skip_selectors)
        if button:
            return self.click_button(button, "跳过按钮")
        
        print("未找到跳过按钮")
        return False
    
    def wait_for_page_load(self, timeout: int = 10) -> bool:
        """等待页面加载完成"""
        try:
            # 等待页面基本元素加载
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # 额外等待一下，确保动态内容加载
            Utils.random_delay(2, 3)
            return True
            
        except TimeoutException:
            print("页面加载超时")
            return False
    
    def navigate_to_test_area(self) -> bool:
        """导航到答题区域"""
        print("开始导航到答题区域...")
        
        max_attempts = 10  # 最多尝试10次按钮点击
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            print(f"\n第 {attempt} 次尝试导航...")
            
            # 等待页面加载
            if not self.wait_for_page_load():
                print("页面加载失败，继续尝试...")
                continue
            
            # 尝试点击各种可能的按钮
            buttons_clicked = False
            
            # 1. 优先尝试点击进入试卷按钮（带5秒等待）
            if self.click_enter_test_button():
                buttons_clicked = True
                continue
            
            # 2. 尝试点击开始答题按钮
            if self.click_start_button():
                buttons_clicked = True
                continue
            
            # 3. 尝试点击下一步按钮
            if self.click_next_button():
                buttons_clicked = True
                continue
            
            # 4. 尝试点击确认按钮
            if self.click_confirm_button():
                buttons_clicked = True
                continue
            
            # 4. 尝试按回车键
            try:
                print("尝试按回车键...")
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.RETURN)
                buttons_clicked = True
                Utils.random_delay(2, 3)
                continue
            except Exception:
                pass
            
            if not buttons_clicked:
                print(f"第 {attempt} 次尝试未找到可点击的按钮")
                
                # 检查是否已经到达答题区域
                if self.is_in_test_area():
                    print("已到达答题区域！")
                    return True
                
                # 等待一下再继续
                Utils.random_delay(3, 5)
        
        print("导航到答题区域失败")
        return False
    
    def is_in_test_area(self) -> bool:
        """检查是否已进入答题区域"""
        # 检查答题区域的特征元素
        test_indicators = [
            ".question", ".test-question", ".question-item",
            ".option", ".choice", ".answer-option",
            ".adjective", ".word-choice", ".word-option",
            "input[type='radio']", "input[type='checkbox']",
            ".test-content", ".quiz-content", ".assessment-content"
        ]
        
        for indicator in test_indicators:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                if elements:
                    print(f"检测到答题区域特征元素: {indicator}")
                    return True
            except Exception:
                continue
        
        return False
    
    def handle_modal_dialogs(self) -> bool:
        """处理可能出现的模态对话框"""
        modal_selectors = [
            ".modal", ".popup", ".dialog", ".overlay",
            ".modal-dialog", ".popup-dialog", ".alert-dialog"
        ]
        
        for selector in modal_selectors:
            try:
                modal = self.driver.find_element(By.CSS_SELECTOR, selector)
                if modal and modal.is_displayed():
                    print("检测到模态对话框，尝试关闭...")
                    
                    # 尝试点击关闭按钮
                    close_buttons = [
                        ".close", ".modal-close", ".popup-close", ".dialog-close",
                        "button[class*='close']", ".btn-close", "×", "✕"
                    ]
                    
                    for close_btn in close_buttons:
                        try:
                            close_element = modal.find_element(By.CSS_SELECTOR, close_btn)
                            if close_element and close_element.is_displayed():
                                self.click_button(close_element, "关闭按钮")
                                return True
                        except Exception:
                            continue
                    
                    # 如果找不到关闭按钮，尝试按ESC键
                    try:
                        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                        Utils.random_delay(1, 2)
                        return True
                    except Exception:
                        pass
                        
            except Exception:
                continue
        
        return False
