"""
北森性格测试自动化模块
"""
import time
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import Config
from utils import Utils

class BeisenAutomation:
    """北森性格测试自动化类"""
    
    def __init__(self, config_file: str = "answers.json"):
        self.config = Config(config_file)
        self.driver = None
        self.answers = self.config.get_answers()
        self.selectors = self.config.get_selectors()
        self.wait_time = self.config.get_wait_time()
        self.retry_count = self.config.get_retry_count()
    
    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            import platform
            import os
            
            chrome_options = Options()
            
            # 根据配置设置无头模式
            if self.config.is_headless():
                chrome_options.add_argument("--headless")
            
            # 添加常用选项
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # 检测操作系统并设置正确的ChromeDriver
            system = platform.system().lower()
            print(f"检测到操作系统: {system}")
            
            try:
                # 使用工具函数获取ChromeDriver路径
                driver_path = Utils.get_chromedriver_path()
                
                if driver_path and os.path.exists(driver_path):
                    print(f"ChromeDriver路径: {driver_path}")
                    service = Service(driver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    raise FileNotFoundError("无法获取有效的ChromeDriver路径")
                
            except Exception as e:
                print(f"自动下载ChromeDriver失败: {e}")
                print("尝试清理缓存后重新下载...")
                
                # 清理缓存后重试
                Utils.clear_webdriver_cache()
                try:
                    driver_path = Utils.get_chromedriver_path()
                    if driver_path and os.path.exists(driver_path):
                        print(f"重新下载ChromeDriver成功: {driver_path}")
                        service = Service(driver_path)
                        self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    else:
                        raise Exception("重新下载失败")
                except Exception as e2:
                    print(f"重新下载ChromeDriver失败: {e2}")
                    print("尝试使用系统PATH中的ChromeDriver...")
                    
                    # 最后备用方案：使用系统PATH中的ChromeDriver
                    service = Service()  # 不指定路径，让Selenium在PATH中查找
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("浏览器驱动设置成功")
            return True
            
        except Exception as e:
            print(f"浏览器驱动设置失败: {e}")
            return False
    
    def open_test_page(self) -> bool:
        """打开测试页面"""
        try:
            test_url = self.config.get_test_url()
            if not test_url:
                print("测试链接未配置，请在 answers.json 中设置 test_url")
                return False
            
            print(f"正在打开测试页面: {test_url}")
            self.driver.get(test_url)
            
            # 等待页面加载
            Utils.random_delay(2, 4)
            
            print("测试页面打开成功")
            return True
            
        except Exception as e:
            print(f"打开测试页面失败: {e}")
            return False
    
    def find_question_elements(self) -> List[Dict]:
        """查找题目和选项元素"""
        try:
            # 等待题目容器出现
            question_container = Utils.wait_for_element(
                self.driver, 
                self.selectors.get("question_container", ".question, .question-item, .test-question"),
                timeout=10
            )
            
            if not question_container:
                print("未找到题目容器")
                return []
            
            # 查找所有选项按钮
            option_buttons = self.driver.find_elements(
                By.CSS_SELECTOR, 
                self.selectors.get("option_buttons", ".option, .choice, .answer-option, button[class*='option']")
            )
            
            if not option_buttons:
                print("未找到选项按钮")
                return []
            
            # 构建选项信息
            options = []
            for i, button in enumerate(option_buttons):
                try:
                    text = button.text.strip()
                    if text:
                        options.append({
                            'element': button,
                            'text': text,
                            'index': i,
                            'value': self._extract_option_value(button, text)
                        })
                except Exception as e:
                    print(f"处理选项 {i} 时出错: {e}")
                    continue
            
            return options
            
        except Exception as e:
            print(f"查找题目元素失败: {e}")
            return []
    
    def _extract_option_value(self, element, text: str) -> str:
        """提取选项值（A、B、C、D等）"""
        try:
            # 尝试从元素的class或data属性获取值
            value = element.get_attribute("data-value") or element.get_attribute("value")
            if value:
                return value
            
            # 尝试从文本中提取字母
            import re
            match = re.search(r'^([A-Z])[\.\)]\s*', text)
            if match:
                return match.group(1)
            
            # 尝试从文本开头提取
            if text and len(text) > 0:
                first_char = text[0].upper()
                if first_char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    return first_char
            
            # 默认返回索引对应的字母
            index = int(element.get_attribute("data-index") or "0")
            return chr(ord('A') + index)
            
        except Exception:
            return "A"  # 默认返回A
    
    def answer_question(self, question_num: int) -> bool:
        """回答单个题目"""
        try:
            print(f"\n正在回答第 {question_num} 题...")
            
            # 查找题目元素
            options = self.find_question_elements()
            if not options:
                print(f"第 {question_num} 题未找到选项")
                return False
            
            # 获取答案
            answer_key = f"question_{question_num}"
            expected_answer = self.answers.get(answer_key)
            
            if not expected_answer:
                print(f"第 {question_num} 题未配置答案，跳过")
                return True
            
            print(f"期望答案: {expected_answer}")
            print(f"找到 {len(options)} 个选项:")
            for opt in options:
                print(f"  {opt['value']}: {opt['text'][:50]}...")
            
            # 查找匹配的选项
            selected_option = None
            for opt in options:
                if opt['value'].upper() == expected_answer.upper():
                    selected_option = opt
                    break
            
            if not selected_option:
                print(f"未找到匹配的选项 {expected_answer}")
                return False
            
            # 点击选项
            print(f"选择选项: {selected_option['value']} - {selected_option['text'][:50]}...")
            success = Utils.safe_click(self.driver, selected_option['element'], self.retry_count)
            
            if success:
                print(f"第 {question_num} 题回答成功")
                Utils.random_delay(1, 2)  # 等待页面响应
                return True
            else:
                print(f"第 {question_num} 题回答失败")
                return False
                
        except Exception as e:
            print(f"回答第 {question_num} 题时出错: {e}")
            return False
    
    def click_next_button(self) -> bool:
        """点击下一题按钮"""
        try:
            next_selectors = [
                self.selectors.get("next_button", ".next, .next-button, .btn-next"),
                "button[class*='next']",
                "input[value*='下一题']",
                "input[value*='Next']",
                ".btn-primary",
                "button[type='submit']"
            ]
            
            for selector in next_selectors:
                try:
                    next_button = Utils.wait_for_element(self.driver, selector, timeout=3)
                    if next_button and next_button.is_enabled():
                        print("点击下一题按钮")
                        success = Utils.safe_click(self.driver, next_button, self.retry_count)
                        if success:
                            Utils.random_delay(2, 3)
                            return True
                except Exception:
                    continue
            
            print("未找到下一题按钮，尝试按回车键")
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.RETURN)
            Utils.random_delay(2, 3)
            return True
            
        except Exception as e:
            print(f"点击下一题按钮失败: {e}")
            return False
    
    def submit_test(self) -> bool:
        """提交测试"""
        try:
            submit_selectors = [
                self.selectors.get("submit_button", ".submit, .submit-button, .finish"),
                "button[class*='submit']",
                "input[value*='提交']",
                "input[value*='Submit']",
                "input[value*='完成']",
                "input[value*='Finish']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = Utils.wait_for_element(self.driver, selector, timeout=3)
                    if submit_button and submit_button.is_enabled():
                        print("点击提交按钮")
                        success = Utils.safe_click(self.driver, submit_button, self.retry_count)
                        if success:
                            Utils.random_delay(3, 5)
                            return True
                except Exception:
                    continue
            
            print("未找到提交按钮")
            return False
            
        except Exception as e:
            print(f"提交测试失败: {e}")
            return False
    
    def run_automation(self) -> bool:
        """运行自动化测试"""
        try:
            print("开始北森性格测试自动化...")
            
            # 设置浏览器驱动
            if not self.setup_driver():
                return False
            
            # 打开测试页面
            if not self.open_test_page():
                return False
            
            # 开始答题
            question_num = 1
            max_questions = len(self.answers)
            failed_questions = []
            
            while question_num <= max_questions:
                print(f"\n{'='*60}")
                print(f"当前进度: {question_num}/{max_questions}")
                
                # 回答题目
                success = self.answer_question(question_num)
                if not success:
                    failed_questions.append(question_num)
                
                # 点击下一题（除了最后一题）
                if question_num < max_questions:
                    if not self.click_next_button():
                        print("无法进入下一题，尝试继续...")
                
                question_num += 1
                Utils.random_delay(2, 4)  # 题目间延迟
            
            # 提交测试
            print(f"\n{'='*60}")
            print("所有题目回答完成，正在提交...")
            self.submit_test()
            
            # 显示结果
            print(f"\n{'='*60}")
            print("自动化测试完成！")
            if failed_questions:
                print(f"失败的题目: {failed_questions}")
            else:
                print("所有题目都成功回答！")
            
            return True
            
        except Exception as e:
            print(f"自动化测试运行失败: {e}")
            return False
        
        finally:
            if self.driver:
                print("关闭浏览器...")
                self.driver.quit()
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
