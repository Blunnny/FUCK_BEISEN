"""
北森性格测试自动化主程序
"""
import sys
import os
from colorama import init, Fore, Style
from adjective_test_automation import AdjectiveTestAutomation

# 初始化colorama，支持Windows彩色输出
init(autoreset=True)

def print_banner():
    """打印程序横幅"""
    banner = f"""
{Fore.CYAN}{'='*60}
{Fore.YELLOW}    北森性格测试自动化工具
{Fore.CYAN}{'='*60}
{Fore.GREEN}功能: 自动填写北森性格测试题库
{Fore.GREEN}作者: Blunnny
{Fore.GREEN}版本: 1.0.0
{Fore.CYAN}{'='*60}
"""
    print(banner)

def check_config_file():
    """检查配置文件是否存在"""
    if not os.path.exists("answers.json"):
        print(f"{Fore.RED}错误: 配置文件 answers.json 不存在！")
        print(f"{Fore.YELLOW}请先创建配置文件，参考以下格式:")
        print(f"""
{{
  "test_url": "你的测试链接",
  "adjective_ranking": [
    "外向", "活泼", "谨慎", "细心", "乐观", "现实", "创新", "独立", 
    "合作", "冒险", "保守", "依赖", "安静", "粗心", "悲观"
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
    print_banner()
    
    # 检查配置文件
    if not check_config_file():
        sys.exit(1)
    
    try:
        # 创建自动化实例
        automation = AdjectiveTestAutomation("answers.json")
        
        # 显示配置信息
        print(f"{Fore.CYAN}配置信息:")
        print(f"  测试链接: {automation.config.get_test_url()}")
        print(f"  等待时间: {automation.wait_time}秒")
        print(f"  重试次数: {automation.retry_count}")
        print(f"  无头模式: {'是' if automation.config.is_headless() else '否'}")
        print()
        
        # 检查形容词排序配置
        adjective_ranking = automation.config.get_adjective_ranking()
        if not adjective_ranking:
            print(f"{Fore.RED}未配置形容词排序！")
            sys.exit(1)
        
        # 确认开始
        confirm = input(f"{Fore.YELLOW}是否开始自动化测试？(y/n): ").lower().strip()
        if confirm not in ['y', 'yes', '是']:
            print(f"{Fore.RED}用户取消操作")
            sys.exit(0)
        
        # 运行自动化
        print(f"\n{Fore.GREEN}开始自动化测试...")
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
