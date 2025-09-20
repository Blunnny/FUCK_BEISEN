"""
形容词排序测试自动化模块
专门处理北森性格测试中的形容词排序题目
"""
import time
from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import Config
from utils import Utils
from button_handler import ButtonHandler

class AdjectiveTestAutomation:
    """形容词排序测试自动化类"""
    
    def __init__(self, config_file: str = "answers.json"):
        self.config = Config(config_file)
        self.driver = None
        self.button_handler = None
        self.adjective_ranking = self.config.get_adjective_ranking()
        self.test_selectors = self.config.get_test_selectors()
        self.wait_time = self.config.get_wait_time()
        self.retry_count = self.config.get_retry_count()
        self.wait_timeout = self.config.get_wait_timeout()
    
    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
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
            
            # 初始化按钮处理器
            self.button_handler = ButtonHandler(self.driver, {
                "button_selectors": self.config.get_button_selectors(),
                "wait_timeout": self.wait_timeout,
                "retry_count": self.retry_count
            })
            
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
    
    def navigate_to_test_area(self) -> bool:
        """导航到答题区域"""
        if not self.button_handler:
            print("按钮处理器未初始化")
            return False
        
        return self.button_handler.navigate_to_test_area()
    
    def find_adjective_elements(self) -> List[WebElement]:
        """查找形容词元素"""
        try:
            # 等待形容词容器出现
            container_selector = self.test_selectors.get("adjective_container", ".adjective-group, .word-group, .choice-group")
            container = Utils.wait_for_element(self.driver, container_selector, timeout=self.wait_timeout)
            
            if not container:
                print("未找到形容词容器")
                return []
            
            # 查找所有形容词项
            item_selector = self.test_selectors.get("adjective_items", ".adjective-item, .word-item, .choice-item")
            items = self.driver.find_elements(By.CSS_SELECTOR, item_selector)
            
            if not items:
                print("未找到形容词项")
                return []
            
            print(f"找到 {len(items)} 个形容词项")
            return items
            
        except Exception as e:
            print(f"查找形容词元素失败: {e}")
            return []
    
    def extract_adjective_text(self, element: WebElement) -> str:
        """提取形容词文本"""
        try:
            # 尝试多种方式获取文本
            text = element.text.strip()
            if text:
                return text
            
            # 尝试从子元素获取文本
            text_elements = element.find_elements(By.CSS_SELECTOR, "span, div, p, label")
            for text_elem in text_elements:
                text = text_elem.text.strip()
                if text:
                    return text
            
            # 尝试从属性获取
            text = element.get_attribute("title") or element.get_attribute("data-text") or element.get_attribute("value")
            if text:
                return text.strip()
            
            return ""
            
        except Exception as e:
            print(f"提取形容词文本失败: {e}")
            return ""
    
    def find_most_least_buttons(self) -> Tuple[Optional[WebElement], Optional[WebElement]]:
        """查找最符合和最不符合按钮"""
        try:
            most_selector = self.test_selectors.get("most_suitable", ".most-suitable, .most-like, .most-match")
            least_selector = self.test_selectors.get("least_suitable", ".least-suitable, .least-like, .least-match")
            
            most_button = Utils.wait_for_element(self.driver, most_selector, timeout=5)
            least_button = Utils.wait_for_element(self.driver, least_selector, timeout=5)
            
            return most_button, least_button
            
        except Exception as e:
            print(f"查找最符合/最不符合按钮失败: {e}")
            return None, None
    
    def select_adjective(self, adjective: str, elements: List[WebElement], is_most: bool) -> bool:
        """选择形容词"""
        try:
            print(f"正在选择{'最符合' if is_most else '最不符合'}的形容词: {adjective}")
            
            # 查找匹配的形容词元素
            target_element = None
            for element in elements:
                text = self.extract_adjective_text(element)
                if adjective in text or text in adjective:
                    target_element = element
                    break
            
            if not target_element:
                print(f"未找到形容词: {adjective}")
                return False
            
            # 点击形容词元素
            success = Utils.safe_click(self.driver, target_element, self.retry_count)
            if not success:
                print(f"点击形容词失败: {adjective}")
                return False
            
            Utils.random_delay(0.5, 1.0)
            
            # 查找并点击最符合/最不符合按钮
            most_button, least_button = self.find_most_least_buttons()
            target_button = most_button if is_most else least_button
            
            if target_button:
                success = Utils.safe_click(self.driver, target_button, self.retry_count)
                if success:
                    print(f"成功选择{adjective}为{'最符合' if is_most else '最不符合'}")
                    Utils.random_delay(1, 2)
                    return True
                else:
                    print(f"点击{'最符合' if is_most else '最不符合'}按钮失败")
                    return False
            else:
                print(f"未找到{'最符合' if is_most else '最不符合'}按钮")
                return False
                
        except Exception as e:
            print(f"选择形容词失败: {e}")
            return False
    
    def answer_adjective_question(self, question_num: int) -> bool:
        """回答一道形容词题目"""
        try:
            print(f"\n开始回答第 {question_num} 题...")
            
            # 查找形容词元素
            elements = self.find_adjective_elements()
            if not elements:
                print(f"未找到第 {question_num} 题的形容词元素")
                return False
            
            # 提取页面上的形容词
            page_adjectives = []
            for elem in elements:
                text = self.extract_adjective_text(elem)
                if text:
                    page_adjectives.append((text, elem))
            
            if len(page_adjectives) != 3:
                print(f"第 {question_num} 题找到的形容词数量不正确: {len(page_adjectives)}")
                return False
            
            print(f"页面形容词: {[adj[0] for adj in page_adjectives]}")
            
            # 根据统一排序选择最符合和最不符合的形容词
            most_suitable, least_suitable = self.select_most_and_least_suitable(page_adjectives)
            
            if not most_suitable or not least_suitable:
                print(f"第 {question_num} 题无法确定最符合/最不符合的形容词")
                return False
            
            print(f"最符合: {most_suitable[0]}, 最不符合: {least_suitable[0]}")
            
            # 选择最符合的形容词
            if not self.select_adjective(most_suitable[0], [most_suitable[1]], is_most=True):
                print(f"选择最符合形容词失败: {most_suitable[0]}")
                return False
            
            # 选择最不符合的形容词
            if not self.select_adjective(least_suitable[0], [least_suitable[1]], is_most=False):
                print(f"选择最不符合形容词失败: {least_suitable[0]}")
                return False
            
            print(f"第 {question_num} 题回答完成")
            return True
            
        except Exception as e:
            print(f"回答第 {question_num} 题失败: {e}")
            return False
    
    def select_most_and_least_suitable(self, page_adjectives: List[Tuple[str, WebElement]]) -> Tuple[Optional[Tuple[str, WebElement]], Optional[Tuple[str, WebElement]]]:
        """根据统一排序选择最符合和最不符合的形容词"""
        try:
            # 计算每个形容词的优先级
            adjective_priorities = []
            for text, element in page_adjectives:
                priority = self.config.get_adjective_priority(text)
                adjective_priorities.append((text, element, priority))
            
            # 按优先级排序（数字越小优先级越高）
            adjective_priorities.sort(key=lambda x: x[2])
            
            print(f"优先级排序: {[(adj[0], adj[2]) for adj in adjective_priorities]}")
            
            # 最符合的是优先级最高的（数字最小）
            most_suitable = (adjective_priorities[0][0], adjective_priorities[0][1])
            
            # 最不符合的是优先级最低的（数字最大）
            least_suitable = (adjective_priorities[-1][0], adjective_priorities[-1][1])
            
            return most_suitable, least_suitable
            
        except Exception as e:
            print(f"选择最符合/最不符合形容词失败: {e}")
            return None, None
    
    def click_next_question(self) -> bool:
        """点击下一题按钮"""
        try:
            next_selector = self.test_selectors.get("next_question", ".next-question, .continue, .next")
            next_button = Utils.wait_for_element(self.driver, next_selector, timeout=5)
            
            if next_button:
                success = Utils.safe_click(self.driver, next_button, self.retry_count)
                if success:
                    print("成功点击下一题按钮")
                    Utils.random_delay(2, 3)
                    return True
            
            # 如果找不到专门的下一题按钮，尝试通用按钮
            if self.button_handler:
                return self.button_handler.click_next_button()
            
            print("未找到下一题按钮")
            return False
            
        except Exception as e:
            print(f"点击下一题按钮失败: {e}")
            return False
    
    def submit_test(self) -> bool:
        """提交测试"""
        try:
            submit_selectors = [
                ".submit", ".submit-button", ".finish", ".complete",
                "button[class*='submit']", "input[value*='提交']", "input[value*='完成']"
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
            print("开始北森形容词排序测试自动化...")
            
            # 设置浏览器驱动
            if not self.setup_driver():
                return False
            
            # 打开测试页面
            if not self.open_test_page():
                return False
            
            # 导航到答题区域
            if not self.navigate_to_test_area():
                print("导航到答题区域失败，尝试继续...")
            
            # 检查形容词排序配置
            if not self.adjective_ranking:
                print("未配置形容词排序")
                return False
            
            print(f"形容词排序配置: {self.adjective_ranking}")
            print("开始答题，程序将根据排序自动选择最符合和最不符合的形容词...")
            
            # 开始答题
            question_num = 1
            max_questions = 50  # 设置一个合理的最大题目数
            failed_questions = []
            
            while question_num <= max_questions:
                print(f"\n{'='*60}")
                print(f"当前进度: 第 {question_num} 题")
                
                # 回答题目
                success = self.answer_adjective_question(question_num)
                if not success:
                    failed_questions.append(question_num)
                    # 如果连续失败多次，可能已经完成所有题目
                    if len(failed_questions) >= 3 and question_num > 5:
                        print("连续失败多次，可能已完成所有题目")
                        break
                
                # 点击下一题
                if not self.click_next_question():
                    print("无法进入下一题，可能已完成所有题目")
                    break
                
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
