"""
按钮处理模块
用于处理进入答题区域前的各种按钮点击
"""
import time
import random
from typing import List, Optional, Dict, Any, Tuple
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
        
        # 专门针对进入试卷按钮的选择器（根据实际测试结果优化）
        enter_test_selectors = [
            ".phoenix-button.wraper--primary",  # 实际有效的选择器
            # 以下选择器暂时注释，根据测试结果它们无效
            # ".phoenix-button.wraper--middle",   # 中等大小按钮
            # ".phoenix-button.wraper",           # 通用按钮包装器
            # "div.phoenix-button[class*='primary']",  # 主要按钮
            # "div.phoenix-button[class*='middle']",   # 中等按钮
            # ".phoenix-button.content",          # 按钮内容
            # "div[class*='phoenix-button'][class*='primary']",  # 组合选择器
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
    
    def click_continue_button(self) -> bool:
        """点击继续答题或去答题按钮"""
        print("查找继续答题/去答题按钮...")
        
        # 根据实际测试结果优化继续答题按钮的选择器
        continue_selectors = [
            "div[data-cls='outline-part-item-right']",  # 实际有效的选择器
            # 以下选择器暂时注释，根据测试结果它们无效
            # "div[data-cls*='outline-part-item']",       # 更宽泛的匹配
            # ".outline-part-item-right",                 # CSS类选择器
            # "div[class*='outline-part-item']",          # 包含outline-part-item的div
            # "div[class*='part-item']",                  # 包含part-item的div
        ]
        
        # 尝试按选择器查找按钮
        button = None
        for selector in continue_selectors:
            try:
                print(f"尝试选择器: {selector}")
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        # 检查元素内部是否包含"继续答题"或"去答题"文本
                        text = element.text.strip()
                        if "继续答题" in text or "去答题" in text or "继续" in text:
                            button = element
                            print(f"找到继续答题按钮: {text}")
                            break
                if button:
                    break
            except Exception as e:
                print(f"选择器 {selector} 查找失败: {e}")
                continue
        
        # 如果按选择器没找到，尝试按文本查找
        if not button:
            print("按选择器未找到，尝试按文本查找...")
            button = self.find_button_by_text(["继续答题", "去答题", "继续", "开始答题"])
        
        if not button:
            print("未找到继续答题/去答题按钮")
            return False
        
        # 智能等待按钮可点击
        print("等待继续答题按钮可点击...")
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
                        print(f"继续答题按钮在 {waited_time:.1f} 秒后变为可点击")
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
            print("继续答题按钮等待超时，尝试强制点击")
        
        # 点击按钮
        return self.click_button(button, "继续答题按钮")
    
    def click_next_step_button(self) -> bool:
        """点击下一步按钮（答题说明页面）"""
        print("查找下一步按钮...")
        
        # 根据实际测试结果优化下一步按钮的选择器
        next_step_selectors = [
            "div.phoenix-button.content",  # 实际有效的选择器
            # 以下选择器暂时注释，根据测试结果它们无效
            # ".phoenix-button.content",     # CSS类选择器
            # "div[class*='phoenix-button'][class*='content']",  # 组合选择器
            # ".phoenix-button",             # 通用phoenix-button
            # "div[class*='phoenix-button']", # 包含phoenix-button的div
        ]
        
        # 尝试按选择器查找按钮
        button = None
        for selector in next_step_selectors:
            try:
                print(f"尝试选择器: {selector}")
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        # 检查元素内部是否包含"下一步"文本
                        text = element.text.strip()
                        if "下一步" in text or "Next" in text:
                            button = element
                            print(f"找到下一步按钮: {text}")
                            break
                if button:
                    break
            except Exception as e:
                print(f"选择器 {selector} 查找失败: {e}")
                continue
        
        # 如果按选择器没找到，尝试按文本查找
        if not button:
            print("按选择器未找到，尝试按文本查找...")
            button = self.find_button_by_text(["下一步", "Next", "继续", "开始答题"])
        
        if not button:
            print("未找到下一步按钮")
            return False
        
        # 智能等待按钮可点击
        print("等待下一步按钮可点击...")
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
                        print(f"下一步按钮在 {waited_time:.1f} 秒后变为可点击")
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
            print("下一步按钮等待超时，尝试强制点击")
        
        # 点击按钮
        return self.click_button(button, "下一步按钮")
    
    def click_practice_next_step_button(self) -> bool:
        """点击练习题页面的下一步按钮"""
        print("查找练习题页面的下一步按钮...")
        
        # 根据实际测试结果优化练习题下一步按钮的选择器
        practice_next_step_selectors = [
            "div.phoenix-button.content",  # 实际有效的选择器
            # 以下选择器暂时注释，根据测试结果它们无效
            # ".phoenix-button.content",     # CSS类选择器
            # "div[class*='phoenix-button'][class*='content']",  # 组合选择器
            # ".phoenix-button",             # 通用phoenix-button
            # "div[class*='phoenix-button']", # 包含phoenix-button的div
        ]
        
        # 尝试按选择器查找按钮
        button = None
        for selector in practice_next_step_selectors:
            try:
                print(f"尝试选择器: {selector}")
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        # 检查元素内部是否包含"下一步"文本
                        text = element.text.strip()
                        if "下一步" in text or "Next" in text:
                            button = element
                            print(f"找到练习题下一步按钮: {text}")
                            break
                if button:
                    break
            except Exception as e:
                print(f"选择器 {selector} 查找失败: {e}")
                continue
        
        # 如果按选择器没找到，尝试按文本查找
        if not button:
            print("按选择器未找到，尝试按文本查找...")
            button = self.find_button_by_text(["下一步", "Next", "继续", "开始答题"])
        
        if not button:
            print("未找到练习题下一步按钮")
            return False
        
        # 智能等待按钮可点击
        print("等待练习题下一步按钮可点击...")
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
                        print(f"练习题下一步按钮在 {waited_time:.1f} 秒后变为可点击")
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
            print("练习题下一步按钮等待超时，尝试强制点击")
        
        # 点击按钮
        return self.click_button(button, "练习题下一步按钮")
    
    def click_formal_answer_button(self) -> bool:
        """点击正式答题按钮（练习完成页面）"""
        print("查找正式答题按钮...")
        
        # 根据实际测试结果优化正式答题按钮的选择器
        formal_answer_selectors = [
            "div.phoenix-button.content",  # 实际有效的选择器
            # 以下选择器暂时注释，根据测试结果它们无效
            # ".phoenix-button.content",     # CSS类选择器
            # "div[class*='phoenix-button'][class*='content']",  # 组合选择器
            # ".phoenix-button",             # 通用phoenix-button
            # "div[class*='phoenix-button']", # 包含phoenix-button的div
        ]
        
        # 尝试按选择器查找按钮
        button = None
        for selector in formal_answer_selectors:
            try:
                print(f"尝试选择器: {selector}")
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        # 检查元素内部是否包含"正式答题"文本
                        text = element.text.strip()
                        if "正式答题" in text or "正式答題" in text or "开始答题" in text:
                            button = element
                            print(f"找到正式答题按钮: {text}")
                            break
                if button:
                    break
            except Exception as e:
                print(f"选择器 {selector} 查找失败: {e}")
                continue
        
        # 如果按选择器没找到，尝试按文本查找
        if not button:
            print("按选择器未找到，尝试按文本查找...")
            button = self.find_button_by_text(["正式答题", "正式答題", "开始答题", "开始测试", "进入答题"])
        
        if not button:
            print("未找到正式答题按钮")
            return False
        
        # 智能等待按钮可点击
        print("等待正式答题按钮可点击...")
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
                        print(f"正式答题按钮在 {waited_time:.1f} 秒后变为可点击")
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
            print("正式答题按钮等待超时，尝试强制点击")
        
        # 点击按钮
        return self.click_button(button, "正式答题按钮")
    
    def find_adjective_options(self, adjective_list: List[str] = None) -> List[WebElement]:
        """查找页面上的形容词选项"""
        try:
            # 使用传入的形容词列表，如果没有传入则使用默认列表
            if adjective_list is None:
                adjective_list = ["善解人意的", "有计划性的", "有领导意愿的"]
            
            print(f"查找形容词选项，目标列表: {adjective_list}")
            
            # 根据截图分析，形容词选项的选择器
            option_selectors = [
                "div[data-cls='select-block_item']",  # 根据截图的data-cls属性
                ".select-block_item",                 # CSS类选择器
                "div[class*='select-block']",         # 包含select-block的div
                "div[class*='SK9xr']",                # 根据截图的class
                "span[class*='I6Yvw']",               # 根据截图的span class
            ]
            
            options = []
            for selector in option_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"选择器 {selector} 找到 {len(elements)} 个元素")
                    
                    for element in elements:
                        if element.is_displayed():
                            text = element.text.strip()
                            print(f"元素文本: '{text}'")
                            
                            # 检查是否包含目标形容词
                            if text and any(adj in text for adj in adjective_list):
                                options.append(element)
                                print(f"找到形容词选项: {text}")
                    
                    if options:
                        print(f"找到选项，停止搜索")
                        break
                except Exception as e:
                    print(f"选择器 {selector} 查找失败: {e}")
                    continue
            
            print(f"总共找到 {len(options)} 个形容词选项")
            return options
            
        except Exception as e:
            print(f"查找形容词选项失败: {e}")
            return []
    
    def find_most_least_boxes(self) -> Tuple[Optional[WebElement], Optional[WebElement]]:
        """查找最符合和最不符合的选框"""
        try:
            # 根据截图分析，选框的选择器
            box_selectors = [
                "div[data-cls='tuozhuai-content']",  # 根据截图的data-cls属性
                ".tuozhuai-content",                 # CSS类选择器
                "div[class*='tuozhuai']",            # 包含tuozhuai的div
                "div[class*='eMsyU']",               # 根据截图的class
            ]
            
            most_box = None
            least_box = None
            
            for selector in box_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            text = element.text.strip()
                            if "最符合" in text:
                                most_box = element
                                print(f"找到最符合选框: {text}")
                            elif "最不符合" in text:
                                least_box = element
                                print(f"找到最不符合选框: {text}")
                    if most_box and least_box:
                        break
                except Exception as e:
                    print(f"选择器 {selector} 查找失败: {e}")
                    continue
            
            return most_box, least_box
            
        except Exception as e:
            print(f"查找最符合/最不符合选框失败: {e}")
            return None, None
    
    def answer_question(self, adjective_ranking: List[str]) -> bool:
        """回答一道题目"""
        try:
            print("开始回答题目...")
            
            # 查找形容词选项
            options = self.find_adjective_options(adjective_ranking)
            if len(options) < 1:
                print(f"未找到任何形容词选项")
                return False
            
            # 提取选项文本
            option_texts = []
            for option in options:
                text = option.text.strip()
                print(f"选项文本: {text}")
                
                # 如果文本包含多个形容词，按行分割
                if '\n' in text:
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and any(adj in line for adj in adjective_ranking):
                            option_texts.append(line)
                            print(f"提取到形容词: {line}")
                else:
                    option_texts.append(text)
                    print(f"提取到形容词: {text}")
            
            print(f"页面选项: {option_texts}")
            print(f"配置排序: {adjective_ranking}")
            
            # 根据排序选择最符合和最不符合的形容词
            most_suitable, least_suitable = self.select_most_and_least_suitable(option_texts, adjective_ranking)
            
            if not most_suitable or not least_suitable:
                print("无法确定最符合/最不符合的形容词")
                return False
            
            print(f"最符合: {most_suitable}, 最不符合: {least_suitable}")
            
            # 查找最符合和最不符合的选框
            most_box, least_box = self.find_most_least_boxes()
            if not most_box or not least_box:
                print("未找到最符合/最不符合选框")
                return False
            
            # 选择最符合的形容词
            if not self.select_adjective_for_box(most_suitable, options, most_box):
                print(f"选择最符合形容词失败: {most_suitable}")
                return False
            
            Utils.random_delay(1, 2)
            
            # 选择最不符合的形容词
            if not self.select_adjective_for_box(least_suitable, options, least_box):
                print(f"选择最不符合形容词失败: {least_suitable}")
                return False
            
            Utils.random_delay(1, 2)
            
            # 点击确定按钮
            if not self.click_confirm_button():
                print("点击确定按钮失败")
                return False
            
            print("题目回答完成")
            return True
            
        except Exception as e:
            print(f"回答题目失败: {e}")
            return False
    
    def select_most_and_least_suitable(self, page_options: List[str], adjective_ranking: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """根据排序选择最符合和最不符合的形容词"""
        try:
            # 计算每个选项的优先级
            option_priorities = []
            for option in page_options:
                priority = 999  # 默认优先级（数字越大优先级越低）
                for i, adj in enumerate(adjective_ranking):
                    if adj in option or option in adj:
                        priority = i
                        break
                option_priorities.append((option, priority))
            
            # 按优先级排序（数字越小优先级越高）
            option_priorities.sort(key=lambda x: x[1])
            
            print(f"优先级排序: {[(opt[0], opt[1]) for opt in option_priorities]}")
            
            # 最符合的是优先级最高的（数字最小）
            most_suitable = option_priorities[0][0]
            
            # 最不符合的是优先级最低的（数字最大）
            least_suitable = option_priorities[-1][0]
            
            return most_suitable, least_suitable
            
        except Exception as e:
            print(f"选择最符合/最不符合形容词失败: {e}")
            return None, None
    
    def select_adjective_for_box(self, adjective: str, options: List[WebElement], target_box: WebElement) -> bool:
        """将形容词点击到指定选框"""
        try:
            print(f"正在将 '{adjective}' 点击到选框...")
            
            # 查找匹配的形容词选项
            target_option = None
            for option in options:
                text = option.text.strip()
                if adjective in text or text in adjective:
                    target_option = option
                    break
            
            if not target_option:
                print(f"未找到形容词选项: {adjective}")
                return False
            
            # 点击形容词选项
            try:
                print(f"点击形容词选项: {adjective}")
                success = Utils.safe_click(self.driver, target_option, self.retry_count)
                if not success:
                    print(f"点击形容词选项失败: {adjective}")
                    return False
                
                Utils.random_delay(0.5, 1.0)
                
                # 点击目标选框
                print(f"点击目标选框")
                success = Utils.safe_click(self.driver, target_box, self.retry_count)
                if not success:
                    print(f"点击目标选框失败")
                    return False
                
                print(f"成功将 '{adjective}' 点击到选框")
                return True
                
            except Exception as e:
                print(f"点击操作失败: {e}")
                return False
            
        except Exception as e:
            print(f"选择形容词到选框失败: {e}")
            return False
    
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
                # 点击进入试卷后，等待页面加载，然后尝试点击继续答题按钮
                print("等待页面加载...")
                Utils.random_delay(3, 5)
                
                # 尝试点击继续答题按钮
                if self.click_continue_button():
                    print("成功点击继续答题按钮")
                    Utils.random_delay(2, 3)
                    
                    # 点击继续答题后，等待页面加载，然后尝试点击下一步按钮
                    print("等待页面加载...")
                    Utils.random_delay(3, 5)
                    
                    # 尝试点击下一步按钮（答题说明页面）
                    if self.click_next_step_button():
                        print("成功点击下一步按钮")
                        Utils.random_delay(2, 3)
                        
                        # 点击答题说明下一步后，等待页面加载，然后尝试点击练习题下一步按钮
                        print("等待页面加载...")
                        Utils.random_delay(3, 5)
                        
                        # 尝试点击练习题下一步按钮
                        if self.click_practice_next_step_button():
                            print("成功点击练习题下一步按钮")
                            Utils.random_delay(2, 3)
                            
                            # 点击练习题下一步后，等待页面加载，然后尝试点击正式答题按钮
                            print("等待页面加载...")
                            Utils.random_delay(3, 5)
                            
                            # 尝试点击正式答题按钮
                            if self.click_formal_answer_button():
                                print("成功点击正式答题按钮，进入答题区域")
                                return True  # 直接返回，不再继续尝试其他按钮
                            else:
                                print("未找到正式答题按钮，可能已经进入答题区域")
                        else:
                            print("未找到练习题下一步按钮，可能已经进入答题区域")
                    else:
                        print("未找到下一步按钮，可能已经进入答题区域")
                else:
                    print("未找到继续答题按钮，可能已经进入答题区域")
                continue
            
            # 2. 尝试点击继续答题/去答题按钮
            if self.click_continue_button():
                buttons_clicked = True
                # 点击继续答题后，尝试点击下一步按钮
                Utils.random_delay(2, 3)
                if self.click_next_step_button():
                    print("成功点击下一步按钮")
                    Utils.random_delay(2, 3)
                    
                    # 点击答题说明下一步后，尝试点击练习题下一步按钮
                    Utils.random_delay(2, 3)
                    if self.click_practice_next_step_button():
                        print("成功点击练习题下一步按钮")
                        Utils.random_delay(2, 3)
                        
                        # 点击练习题下一步后，尝试点击正式答题按钮
                        Utils.random_delay(2, 3)
                        if self.click_formal_answer_button():
                            print("成功点击正式答题按钮，进入答题区域")
                            return True  # 直接返回，不再继续尝试其他按钮
                continue
            
            # 3. 尝试点击下一步按钮（答题说明页面）
            if self.click_next_step_button():
                buttons_clicked = True
                # 点击答题说明下一步后，尝试点击练习题下一步按钮
                Utils.random_delay(2, 3)
                if self.click_practice_next_step_button():
                    print("成功点击练习题下一步按钮")
                    Utils.random_delay(2, 3)
                    
                    # 点击练习题下一步后，尝试点击正式答题按钮
                    Utils.random_delay(2, 3)
                    if self.click_formal_answer_button():
                        print("成功点击正式答题按钮，进入答题区域")
                        return True  # 直接返回，不再继续尝试其他按钮
                continue
            
            # 4. 尝试点击练习题下一步按钮
            if self.click_practice_next_step_button():
                buttons_clicked = True
                # 点击练习题下一步后，尝试点击正式答题按钮
                Utils.random_delay(2, 3)
                if self.click_formal_answer_button():
                    print("成功点击正式答题按钮，进入答题区域")
                    return True  # 直接返回，不再继续尝试其他按钮
                continue
            
            # 5. 尝试点击正式答题按钮
            if self.click_formal_answer_button():
                buttons_clicked = True
                print("成功点击正式答题按钮，进入答题区域")
                return True  # 直接返回，不再继续尝试其他按钮
            
            # 4. 尝试点击开始答题按钮
            if self.click_start_button():
                buttons_clicked = True
                continue
            
            # 5. 尝试点击通用下一步按钮
            if self.click_next_button():
                buttons_clicked = True
                continue
            
            # 5. 尝试点击确认按钮
            if self.click_confirm_button():
                buttons_clicked = True
                continue
            
            # 6. 尝试按回车键
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
