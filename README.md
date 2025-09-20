# 北森性格测试自动化工具

一个用于自动填写北森性格测试题库的 Python 工具，支持多种题型和预设答案自动答题。已完全实现形容词三选二和单选题两种题型的自动化填写。

## 功能特点

- 🚀 自动打开测试链接并完成整个答题流程
- 📝 根据预设答案自动答题，支持智能题目匹配
- 🎯 支持两种题型：形容词三选二、单选题
- ⚙️ 灵活的 JSON 配置文件，易于维护和修改
- 🔄 智能重试机制和多种点击方式
- 🎯 多种选择器支持，适应不同页面结构
- 📊 实时进度显示和详细调试信息
- 🛡️ 完善的错误处理和异常恢复
- 🔧 完全复用的按钮操作逻辑

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 选择题型并配置

**形容词三选二题型**：

```bash
cp answers_template.json answers.json
# 编辑 answers.json，配置测试URL和形容词排序
python adjective_test_automation.py
```

**单选题题型**：

```bash
cp single_choice_answers_template.json single_choice_answers.json
# 编辑 single_choice_answers.json，配置测试URL和题目答案
python single_choice_automation.py
```

### 3. 运行程序

程序会自动完成从打开链接到答题结束的全过程！

## 配置说明

### 形容词三选二题型

1. 复制 `answers_template.json` 为 `answers.json` 配置文件
2. 修改以下配置项：

```json
{
  "test_url": "你的北森测试链接",
  "adjective_ranking": ["善解人意的", "有计划性的", "有领导意愿的"],
  "settings": {
    "wait_timeout": 10,
    "page_load_timeout": 30,
    "implicit_wait": 5
  }
}
```

#### 形容词三选二配置项说明

- `test_url`: 北森测试的完整链接
- `adjective_ranking`: 形容词优先级排序数组
  - 按优先级排序：第一位最符合，最后一位最不符合
  - 例如：`["善解人意的", "有计划性的", "有领导意愿的"]`
- `settings`: 运行设置
  - `wait_timeout`: 元素等待超时时间（秒）
  - `page_load_timeout`: 页面加载超时时间（秒）
  - `implicit_wait`: 隐式等待时间（秒）

### 单选题题型

1. 复制 `single_choice_answers_template.json` 为 `single_choice_answers.json` 配置文件
2. 修改以下配置项：

```json
{
  "test_url": "你的北森测试链接",
  "question_answers": [
    {
      "question_text": "当我感到心烦时,我能控制住自己不要发火",
      "answer": "比较符合"
    },
    {
      "question_text": "我能够很好地处理压力",
      "answer": "非常符合"
    },
    {
      "question_text": "我经常感到焦虑",
      "answer": "比较不符合"
    }
  ],
  "settings": {
    "wait_timeout": 10,
    "page_load_timeout": 30,
    "implicit_wait": 5
  }
}
```

#### 单选题配置项说明

- `test_url`: 北森测试的完整链接
- `question_answers`: 题目答案数组，包含题目文本和对应答案
  - `question_text`: 题目文本内容（用于匹配）
  - `answer`: 对应的答案选项
  - 支持的答案选项：`"非常不符合"`、`"比较不符合"`、`"比较符合"`、`"非常符合"`
- `settings`: 运行设置
  - `wait_timeout`: 元素等待超时时间（秒）
  - `page_load_timeout`: 页面加载超时时间（秒）
  - `implicit_wait`: 隐式等待时间（秒）

#### 题目匹配机制

程序会通过以下方式匹配题目：

1. **自动识别题目文本**：从页面中提取题目内容
2. **智能匹配**：在配置文件中查找包含该文本的题目配置
3. **关键词匹配**：即使题目文本不完全相同，也能通过关键词匹配
4. **按顺序匹配**：如果无法匹配，按题目顺序使用配置中的答案
5. **默认答案**：如果完全无法匹配，使用默认答案"非常不符合"

## 使用方法

### 形容词三选二题型

1. 确保已安装 Chrome 浏览器
2. 复制 `answers_template.json` 为 `answers.json`
3. 配置 `answers.json` 文件中的测试链接和形容词排序
4. 激活虚拟环境：`source venv/bin/activate`
5. 运行程序：

```bash
python adjective_test_automation.py
```

### 单选题题型

1. 确保已安装 Chrome 浏览器
2. 复制 `single_choice_answers_template.json` 为 `single_choice_answers.json`
3. 配置 `single_choice_answers.json` 文件中的测试链接和答案
4. 激活虚拟环境：`source venv/bin/activate`
5. 运行程序：

```bash
python single_choice_automation.py
```

### 形容词排序说明

北森性格测试会随机给出三个形容词，需要选择：

- **最符合**：选择排序列表中的第一位
- **最不符合**：选择排序列表中的最后一位

例如配置：

```json
{
  "adjective_ranking": ["善解人意的", "有计划性的", "有领导意愿的"]
}
```

当页面出现这三个形容词时，程序会：

1. 选择"善解人意的"作为最符合
2. 选择"有领导意愿的"作为最不符合

## 项目结构

```
FUCK_BEISEN/
├── adjective_test_automation.py      # 形容词三选二自动化模块
├── single_choice_automation.py       # 单选题自动化模块
├── button_handler.py                 # 按钮处理模块（复用）
├── utils.py                          # 工具函数模块（复用）
├── answers.json                      # 形容词三选二答案配置文件（不提交）
├── answers_template.json             # 形容词三选二配置文件模板
├── single_choice_answers.json        # 单选题答案配置文件（不提交）
├── single_choice_answers_template.json # 单选题配置文件模板
├── test_single_choice.py             # 单选题测试脚本
├── requirements.txt                  # 依赖包列表
├── .gitignore                       # Git忽略文件
└── README.md                        # 说明文档
```

## 注意事项

1. **测试链接**：请确保测试链接有效且可访问
2. **配置准确性**：形容词配置需要与页面实际显示的形容词完全匹配
3. **题目匹配**：单选题的题目文本需要与配置文件中的文本匹配（支持部分匹配）
4. **浏览器环境**：确保已安装 Chrome 浏览器和对应的 ChromeDriver
5. **网络环境**：确保网络连接稳定，避免页面加载超时
6. **使用条款**：请遵守相关网站的使用条款，仅用于学习和研究

## 故障排除

### 常见问题

1. **找不到元素**：

   - 检查页面是否完全加载
   - 确认题目类型是否正确识别
   - 查看调试输出中的选择器匹配结果

2. **题目匹配失败**：

   - 检查配置文件中的题目文本是否与页面显示一致
   - 程序会自动使用默认答案"非常不符合"
   - 可以按题目顺序匹配配置中的答案

3. **浏览器启动失败**：

   - 确保 Chrome 浏览器已安装
   - 检查 ChromeDriver 版本是否与 Chrome 版本匹配

4. **页面加载超时**：

   - 增加 `wait_timeout` 或 `page_load_timeout` 设置
   - 检查网络连接是否稳定

5. **无法进入答题区域**：
   - 程序会自动处理所有导航步骤
   - 如果失败，检查测试链接是否正确

### 调试建议

1. **查看控制台输出**：程序会输出详细的调试信息
2. **检查配置文件**：确保 JSON 格式正确，URL 和答案配置无误
3. **逐步测试**：可以先运行测试脚本检查基本功能

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 免责声明

本工具仅供学习和研究使用，请遵守相关网站的使用条款。使用者需自行承担使用风险。
