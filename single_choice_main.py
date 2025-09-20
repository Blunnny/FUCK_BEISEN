#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北森单选题自动化测试程序
支持单选题类型的自动化填写
"""

import json
import time
from typing import List, Dict, Any, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from button_handler import ButtonHandler
from utils import Utils
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

class SingleChoiceAutomation:
    """单选题自动化测试类"""
    
    def __init__(self, config_file: str = "single_choice_answers.json"):
        """初始化自动化测试"""
        self.config_file = config_file
        self.driver = None
        self.button_handler = None
        self.question_answers = []
        self.settings = {}
        self.wait_timeout = 10
        
        # 加载配置
        self.load_config()
        
        # 设置浏览器选项
        self.setup_driver()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.question_answers = config.get('question_answers', [])
            self.settings = config.get('settings', {})
            self.wait_timeout = self.settings.get('wait_timeout', 10)
            
            print(f"{Fore.GREEN}成功加载配置文件: {self.config_file}")
            print(f"{Fore.CYAN}共加载 {len(self.question_answers)} 道题目")
            
        except FileNotFoundError:
            print(f"{Fore.RED}配置文件不存在: {self.config_file}")
            raise
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}配置文件格式错误: {e}")
            raise
        except Exception as e:
            print(f"{Fore.RED}加载配置文件失败: {e}")
            raise
    
    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 设置页面加载超时
            page_load_timeout = self.settings.get('page_load_timeout', 30)
            implicit_wait = self.settings.get('implicit_wait', 5)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(page_load_timeout)
            self.driver.implicitly_wait(implicit_wait)
            
            # 初始化按钮处理器
            self.button_handler = ButtonHandler(self.driver)
            
            print(f"{Fore.GREEN}浏览器驱动初始化成功")
            
        except Exception as e:
            print(f"{Fore.RED}浏览器驱动初始化失败: {e}")
            raise
    
    def navigate_to_test_area(self) -> bool:
        """导航到测试区域"""
        if not self.button_handler:
            print("按钮处理器未初始化")
            return False
        
        return self.button_handler.navigate_to_test_area()
    
    def find_question_elements(self) -> List[Any]:
        """查找单选题选项元素"""
        try:
            print("正在查找单选题选项...")
            
            # 等待页面加载
            time.sleep(2)
            
            # 根据截图分析，使用正确的选择器
            option_selectors = [
                "div[data-cls*='single-choice'] div[class*='single-choice_item']",  # 根据截图的class结构
                "div[class*='single-choice_item']",  # 根据截图的class
                "div[data-cls*='single-choice item']",  # 根据截图的data-cls
                "div[class*='-5frG']",  # 根据截图的特定class
            ]
            
            for selector in option_selectors:
                try:
                    items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"选择器 {selector} 找到 {len(items)} 个元素")
                    
                    if items:
                        print(f"找到 {len(items)} 个单选题选项")
                        return items
                except Exception as e:
                    print(f"选择器 {selector} 查找失败: {e}")
                    continue
            
            print("未找到单选题选项元素")
            return []
            
        except Exception as e:
            print(f"查找单选题选项失败: {e}")
            return []
    
    def extract_option_text(self, element) -> str:
        """提取选项文本"""
        try:
            # 尝试多种方式获取文本
            text = element.text.strip()
            print(f"元素文本: '{text}'")
            
            if text:
                return text
            
            # 尝试从子元素获取文本
            text_elements = element.find_elements(By.CSS_SELECTOR, "span, div, p, label")
            print(f"找到 {len(text_elements)} 个子元素")
            
            for i, text_elem in enumerate(text_elements):
                sub_text = text_elem.text.strip()
                print(f"子元素 {i}: '{sub_text}'")
                if sub_text:
                    return sub_text
            
            # 尝试从属性获取
            title = element.get_attribute("title")
            data_text = element.get_attribute("data-text")
            value = element.get_attribute("value")
            print(f"属性: title='{title}', data-text='{data_text}', value='{value}'")
            
            if title:
                return title.strip()
            if data_text:
                return data_text.strip()
            if value:
                return value.strip()
            
            return ""
            
        except Exception as e:
            print(f"提取选项文本失败: {e}")
            return ""
    
    def find_confirm_button(self) -> Optional[Any]:
        """查找确定按钮"""
        try:
            print("正在查找确定按钮...")
            
            # 等待一下，让按钮完全加载
            time.sleep(1)
            
            # 根据之前的经验，确定按钮的选择器
            confirm_selectors = [
                "div.phoenix-button.content",  # 根据之前的class
                "div[class*='phoenix-button'][class*='content']",
                "button[class*='phoenix-button']",
                "div[class*='phoenix-button']",
                "button:contains('确定')",
                "div:contains('确定')",
                "button:contains('提交')",
                "div:contains('提交')",
                "button:contains('下一步')",
                "div:contains('下一步')"
            ]
            
            for selector in confirm_selectors:
                try:
                    if ":contains" in selector:
                        # 使用XPath查找包含文本的元素
                        text = selector.split("'")[1]  # 提取文本内容
                        xpath = f"//*[contains(text(), '{text}')]"
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            confirm_button = elements[0]
                            print(f"找到确定按钮: {xpath}")
                            return confirm_button
                    else:
                        confirm_button = Utils.wait_for_element(self.driver, selector, timeout=2)
                        if confirm_button:
                            print(f"找到确定按钮: {selector}")
                            return confirm_button
                except:
                    continue
            
            # 尝试查找所有包含"确定"文本的元素
            try:
                all_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '确定')]")
                if all_elements:
                    confirm_button = all_elements[0]
                    print(f"通过XPath找到确定按钮")
                    return confirm_button
            except:
                pass
            
            print("未找到确定按钮")
            return None
            
        except Exception as e:
            print(f"查找确定按钮失败: {e}")
            return None
    
    def click_confirm_button(self) -> bool:
        """点击确定按钮"""
        try:
            confirm_button = self.find_confirm_button()
            if not confirm_button:
                return False
            
            # 点击确定按钮
            try:
                confirm_button.click()
                print("成功点击确定按钮")
                time.sleep(2)  # 等待页面跳转
                return True
            except Exception as e:
                print(f"点击确定按钮失败: {e}")
                # 尝试JavaScript点击
                try:
                    self.driver.execute_script("arguments[0].click();", confirm_button)
                    print("使用JavaScript成功点击确定按钮")
                    time.sleep(2)
                    return True
                except Exception as e2:
                    print(f"JavaScript点击确定按钮也失败: {e2}")
                    return False
            
        except Exception as e:
            print(f"点击确定按钮失败: {e}")
            return False
    
    def find_question_text(self) -> str:
        """查找当前题目的文本"""
        try:
            # 尝试多种选择器查找题目文本
            question_selectors = [
                "div[class*='question']",
                "div[class*='title']",
                "h1, h2, h3, h4, h5, h6",
                "div[data-cls*='question']",
                "div[data-cls*='title']"
            ]
            
            for selector in question_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and len(text) > 10:  # 题目文本通常比较长
                            print(f"找到题目文本: {text}")
                            return text
                except:
                    continue
            
            print("未找到题目文本")
            return ""
            
        except Exception as e:
            print(f"查找题目文本失败: {e}")
            return ""
    
    def find_matching_answer(self, question_text: str) -> str:
        """根据题目文本查找匹配的答案"""
        try:
            # 如果题目文本为空，返回默认答案
            if not question_text:
                return "非常不符合"
            
            print(f"正在匹配题目: {question_text}")
            
            # 在配置中查找匹配的题目
            for i, question_data in enumerate(self.question_answers):
                config_question = question_data.get('question_text', '')
                print(f"配置题目 {i+1}: {config_question}")
                
                # 尝试多种匹配方式
                if config_question and question_text in config_question:
                    print(f"找到匹配的题目配置: {config_question}")
                    return question_data.get('answer', '非常不符合')
                elif config_question and config_question in question_text:
                    print(f"找到匹配的题目配置: {config_question}")
                    return question_data.get('answer', '非常不符合')
                # 尝试关键词匹配
                elif config_question and any(keyword in question_text for keyword in config_question.split() if len(keyword) > 2):
                    print(f"通过关键词找到匹配的题目配置: {config_question}")
                    return question_data.get('answer', '非常不符合')
            
            # 如果按顺序匹配（作为备选方案）
            if len(self.question_answers) > 0:
                print(f"使用按顺序匹配，第1题使用配置中的第1个答案")
                return self.question_answers[0].get('answer', '非常不符合')
            
            print(f"未找到匹配的题目配置，使用默认答案")
            return "非常不符合"
            
        except Exception as e:
            print(f"查找匹配答案失败: {e}")
            return "非常不符合"

    def answer_single_choice_question(self, question_num: int, target_answer: str) -> bool:
        """回答一道单选题"""
        try:
            print(f"\n开始回答第 {question_num} 题...")
            print(f"目标答案: {target_answer}")
            
            # 查找选项元素
            elements = self.find_question_elements()
            if not elements:
                print(f"未找到第 {question_num} 题的选项元素")
                return False
            
            # 提取页面上的选项
            page_options = []
            for i, elem in enumerate(elements):
                text = self.extract_option_text(elem)
                print(f"元素 {i}: 文本='{text}'")
                if text:
                    page_options.append((text, elem))
                else:
                    print(f"元素 {i} 文本为空，跳过")
            
            print(f"提取到的选项: {[opt[0] for opt in page_options]}")
            
            if len(page_options) < 4:
                print(f"第 {question_num} 题找到的选项数量不足: {len(page_options)}")
                return False
            
            # 查找匹配的选项
            target_element = None
            for text, element in page_options:
                if text == target_answer:
                    target_element = element
                    break
            
            if not target_element:
                print(f"未找到目标答案: {target_answer}")
                print(f"可用选项: {[opt[0] for opt in page_options]}")
                return False
            
            # 点击目标选项
            try:
                print(f"正在点击选项: {target_answer}")
                target_element.click()
                print(f"成功点击选项: {target_answer}")
                time.sleep(1)
            except Exception as e:
                print(f"点击选项失败: {e}")
                # 尝试JavaScript点击
                try:
                    self.driver.execute_script("arguments[0].click();", target_element)
                    print(f"使用JavaScript成功点击选项: {target_answer}")
                    time.sleep(1)
                except Exception as e2:
                    print(f"JavaScript点击选项也失败: {e2}")
                    return False
            
            # 点击选项后自动跳转，无需点击确定按钮
            print("选项已选择，等待自动跳转到下一题...")
            time.sleep(2)  # 等待自动跳转
            
            print(f"第 {question_num} 题回答完成")
            return True
            
        except Exception as e:
            print(f"回答第 {question_num} 题失败: {e}")
            return False
    
    def is_question_page(self) -> bool:
        """检查当前页面是否为题目页面"""
        try:
            # 检查页面是否包含单选题特征元素
            question_indicators = [
                "div[data-cls*='single-choice']",
                "div[class*='single-choice_item']",
                "非常不符合",
                "比较不符合",
                "比较符合",
                "非常符合"
            ]
            
            for indicator in question_indicators:
                try:
                    if ":contains" in indicator or any(text in indicator for text in ["非常不符合", "比较不符合", "比较符合", "非常符合"]):
                        # 使用XPath查找包含文本的元素
                        xpath = f"//*[contains(text(), '{indicator}')]"
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            print(f"检测到题目页面特征元素: {xpath}")
                            return True
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                        if elements:
                            print(f"检测到题目页面特征元素: {indicator}")
                            return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"检查题目页面失败: {e}")
            return False
    
    def run_automation(self) -> bool:
        """运行自动化测试"""
        try:
            print("开始北森单选题自动化测试...")
            
            # 打开测试URL
            test_url = self.settings.get('test_url') or 'https://your-test-url-here.com'
            if hasattr(self, 'question_answers') and self.question_answers:
                # 从配置中获取test_url
                config = {}
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    test_url = config.get('test_url', test_url)
                except:
                    pass
            
            print(f"正在打开测试URL: {test_url}")
            self.driver.get(test_url)
            time.sleep(3)  # 等待页面加载
            
            # 导航到测试区域
            if not self.navigate_to_test_area():
                print("导航到测试区域失败")
                return False
            
            # 开始答题
            question_count = 0
            max_questions = len(self.question_answers)
            
            while question_count < max_questions:
                # 检查是否为题目页面
                if not self.is_question_page():
                    print("等待题目页面加载...")
                    time.sleep(2)
                    continue
                
                question_count += 1
                print(f"\n{'='*60}")
                print(f"当前进度: 第 {question_count} 题")
                
                # 查找当前题目文本
                current_question_text = self.find_question_text()
                print(f"当前题目: {current_question_text}")
                
                # 根据题目文本查找匹配的答案
                target_answer = self.find_matching_answer(current_question_text)
                print(f"匹配的答案: {target_answer}")
                
                # 回答题目
                if not self.answer_single_choice_question(question_count, target_answer):
                    print(f"第 {question_count} 题回答失败")
                    return False
                
                # 等待页面跳转到下一题
                print("等待页面跳转到下一题...")
                time.sleep(3)
            
            print(f"\n{Fore.GREEN}所有题目回答完成！")
            return True
            
        except Exception as e:
            print(f"自动化测试运行失败: {e}")
            return False
        
        finally:
            if self.driver:
                print("关闭浏览器...")
                self.driver.quit()

def main():
    """主函数"""
    try:
        print(f"{Fore.CYAN}北森单选题自动化测试程序")
        print(f"{Fore.CYAN}=" * 50)
        
        # 创建自动化实例
        automation = SingleChoiceAutomation()
        
        # 运行自动化测试
        success = automation.run_automation()
        
        if success:
            print(f"\n{Fore.GREEN}自动化测试完成！")
        else:
            print(f"\n{Fore.RED}自动化测试失败！")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}用户中断程序")
    except Exception as e:
        print(f"\n{Fore.RED}程序运行失败: {e}")

if __name__ == "__main__":
    main()
