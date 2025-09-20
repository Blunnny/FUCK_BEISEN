# 北森性格测试自动化工具

一个用于自动填写北森性格测试题库的 Python 工具，支持多种题型和预设答案自动答题。

## 功能特点

- 🚀 自动打开测试链接
- 📝 根据预设答案自动答题
- 🎯 支持多种题型：形容词三选二、单选题
- ⚙️ 灵活的配置选项
- 🔄 智能重试机制
- 🎯 多种选择器支持
- 📊 实时进度显示
- 🛡️ 错误处理和日志

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 形容词三选二题型

1. 复制 `answers_template.json` 为 `answers.json` 配置文件
2. 修改以下配置项：

```json
{
  "test_url": "你的北森测试链接",
  "adjective_rankings": {
    "group_1": {
      "adjectives": ["活泼", "安静", "外向"],
      "ranking": ["外向", "活泼", "安静"]
    },
    "group_2": {
      "adjectives": ["细心", "粗心", "谨慎"],
      "ranking": ["谨慎", "细心", "粗心"]
    }
  },
  "settings": {
    "wait_time": 3,
    "retry_count": 3,
    "headless": false,
    "browser": "chrome",
    "wait_timeout": 10
  },
  "button_selectors": {
    "next_button": [".next-button", ".btn-next", "button[class*='next']"],
    "start_button": [".start-button", ".btn-start", "button[class*='start']"],
    "confirm_button": [
      ".confirm-button",
      ".btn-confirm",
      "button[class*='confirm']"
    ]
  },
  "test_selectors": {
    "adjective_container": ".adjective-group, .word-group, .choice-group",
    "adjective_items": ".adjective-item, .word-item, .choice-item",
    "most_suitable": ".most-suitable, .most-like, .most-match",
    "least_suitable": ".least-suitable, .least-like, .least-match",
    "next_question": ".next-question, .continue, .next"
  }
}
```

### 配置项说明

- `test_url`: 北森测试的完整链接
- `adjective_rankings`: 形容词排序配置
  - `adjectives`: 每组出现的三个形容词
  - `ranking`: 按优先级排序的形容词列表（第一位最符合，最后一位最不符合）
- `settings`: 运行设置
  - `wait_time`: 操作间等待时间（秒）
  - `retry_count`: 失败重试次数
  - `headless`: 是否无头模式运行
  - `browser`: 浏览器类型（目前支持 chrome）
  - `wait_timeout`: 元素等待超时时间（秒）
- `button_selectors`: 按钮选择器配置（用于进入答题区域）
- `test_selectors`: 测试页面元素选择器（根据实际页面调整）

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

1. 自动识别页面上的题目文本
2. 在配置文件中查找包含该文本的题目配置
3. 使用匹配的题目配置中的答案
4. 如果未找到匹配，使用默认答案"比较符合"

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
"group_1": {
  "adjectives": ["活泼", "安静", "外向"],
  "ranking": ["外向", "活泼", "安静"]
}
```

当页面出现这三个形容词时，程序会：

1. 选择"外向"作为最符合
2. 选择"安静"作为最不符合

## 项目结构

```
FUCK_BEISEN/
├── adjective_test_automation.py      # 形容词三选二自动化模块
├── single_choice_automation.py       # 单选题自动化模块
├── button_handler.py                 # 按钮处理模块（复用）
├── utils.py                          # 工具函数模块（复用）
├── answers.json                      # 形容词三选二答案配置文件
├── answers_template.json             # 形容词三选二配置文件模板
├── single_choice_answers.json        # 单选题答案配置文件
├── single_choice_answers_template.json # 单选题配置文件模板
├── test_single_choice.py             # 单选题测试脚本
├── requirements.txt                  # 依赖包列表
└── README.md                        # 说明文档
```

## 注意事项

1. 请确保测试链接有效且可访问
2. 形容词配置需要与页面实际显示的形容词完全匹配
3. 如页面结构变化，需要调整 `button_selectors` 和 `test_selectors` 配置
4. 建议先在非无头模式下测试，确认无误后再使用无头模式
5. 程序会自动处理进入答题区域前的各种按钮点击
6. 请遵守相关网站的使用条款

## 故障排除

### 常见问题

1. **找不到元素**: 检查 `button_selectors` 和 `test_selectors` 配置是否正确
2. **形容词不匹配**: 确认配置中的形容词与页面显示完全一致
3. **浏览器启动失败**: 确保 Chrome 浏览器已安装
4. **页面加载超时**: 增加 `wait_time` 或 `wait_timeout` 设置
5. **无法进入答题区域**: 检查 `button_selectors` 配置，可能需要添加更多按钮选择器

### 调试模式

设置 `headless: false` 可以观察自动化过程，便于调试。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 免责声明

本工具仅供学习和研究使用，请遵守相关网站的使用条款。使用者需自行承担使用风险。
