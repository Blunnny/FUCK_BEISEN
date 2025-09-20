"""
配置管理模块
"""
import json
import os
from typing import Dict, Any, List, Optional

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "answers.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {self.config_file} 不存在，请先创建配置文件")
            return {}
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}")
            return {}
    
    def get_test_url(self) -> str:
        """获取测试链接"""
        return self.config.get("test_url", "")
    
    def get_answers(self) -> Dict[str, str]:
        """获取答案配置（兼容旧格式）"""
        return self.config.get("answers", {})
    
    def get_adjective_ranking(self) -> List[str]:
        """获取形容词排序配置"""
        return self.config.get("adjective_ranking", [])
    
    def get_settings(self) -> Dict[str, Any]:
        """获取设置配置"""
        return self.config.get("settings", {})
    
    def get_selectors(self) -> Dict[str, str]:
        """获取选择器配置（兼容旧格式）"""
        return self.config.get("selectors", {})
    
    def get_button_selectors(self) -> Dict[str, List[str]]:
        """获取按钮选择器配置"""
        return self.config.get("button_selectors", {})
    
    def get_test_selectors(self) -> Dict[str, str]:
        """获取测试选择器配置"""
        return self.config.get("test_selectors", {})
    
    def get_wait_time(self) -> int:
        """获取等待时间"""
        return self.get_settings().get("wait_time", 3)
    
    def get_retry_count(self) -> int:
        """获取重试次数"""
        return self.get_settings().get("retry_count", 3)
    
    def is_headless(self) -> bool:
        """是否无头模式"""
        return self.get_settings().get("headless", False)
    
    def get_browser(self) -> str:
        """获取浏览器类型"""
        return self.get_settings().get("browser", "chrome")
    
    def get_wait_timeout(self) -> int:
        """获取等待超时时间"""
        return self.get_settings().get("wait_timeout", 10)
    
    def get_adjective_priority(self, adjective: str) -> int:
        """获取形容词的优先级（数字越小优先级越高）"""
        ranking = self.get_adjective_ranking()
        try:
            return ranking.index(adjective)
        except ValueError:
            return len(ranking)  # 如果不在列表中，返回最低优先级
