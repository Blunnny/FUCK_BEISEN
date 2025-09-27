"""
北森性格测试自动化主程序
"""
import sys
import os
from colorama import init, Fore, Style
from adjective_test_automation import AdjectiveTestAutomation

# 初始化colorama，支持Windows彩色输出
init(autoreset=True)


def check_config_file():
    """检查配置文件是否存在"""
    if not os.path.exists("answers.json"):
        print(f"{Fore.RED}错误: 配置文件 answers.json 不存在！")
        print(f"{Fore.YELLOW}请先创建配置文件，参考以下格式:")
        print(f"""
{{
  "test_url": "你的测试链接",
  "adjective_ranking": [
    "愿意主动探索未知的领域",
    "喜欢学习新事物",
    "对新知识抱有好奇心",
  ],
  "settings": {{
    "wait_time": 3,
    "retry_count": 3,
    "headless": false,
    "browser": "chrome"
  }}
}}
        """)
        return False
    return True

def main():
    """主函数"""
    
    # 检查配置文件
    if not check_config_file():
        sys.exit(1)
    
    try:
        # 创建自动化实例
        automation = AdjectiveTestAutomation("answers.json")
        
        # 检查形容词排序配置
        adjective_ranking = automation.config.get_adjective_ranking()
        if not adjective_ranking:
            print(f"{Fore.RED}未配置形容词排序！")
            sys.exit(1)
        
        # 直接运行自动化
        print(f"{Fore.GREEN}开始自动化测试...")
        success = automation.run_automation()
        
        if success:
            print(f"\n{Fore.GREEN}✓ 自动化测试完成！")
        else:
            print(f"\n{Fore.RED}✗ 自动化测试失败！")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}用户中断程序")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}程序运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
