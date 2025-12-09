# BankMind - 银行零售客户经营智能分析系统

> 🏦 数据驱动的精准营销解决方案

## 📋 项目简介

BankMind 是一个面向银行零售业务的**数据驱动精准营销**解决方案，通过机器学习与数据分析技术，帮助银行实现百万级客群的高效经营，提升客户转化率并降低营销成本。

## ✨ 核心功能

| 功能模块 | 描述 | 技术实现 |
|---------|------|---------|
| 📊 可视化大屏 | 动态展示客户结构、资产分布、产品持有等核心指标 | Flask + ECharts |
| 🎯 高价值客户预测 | 预测客户未来3个月资产提升至100万+的概率 | LightGBM + SHAP |
| 👥 客户分群分析 | 基于多维特征的客户聚类分群 | K-Means + PCA |
| 🔗 产品关联分析 | 挖掘产品组合模式，发现交叉销售机会 | Apriori |
| 📈 资产趋势预测 | 预测客户未来季度 AUM 增长趋势 | ARIMA |
| 🤖 智能对话助手 | 自然语言查询客户数据，自动生成 SQL 和图表 | Qwen Agent |

## 📁 项目结构

```
BankMind/
├── main.py                    # 主入口文件（命令行接口）
├── requirements.txt           # 依赖包列表
├── README.md                  # 项目说明
│
├── src/                       # 源代码目录
│   ├── __init__.py
│   │
│   ├── config/               # 配置模块
│   │   ├── __init__.py
│   │   ├── settings.py       # 全局配置
│   │   └── database.py       # 数据库配置
│   │
│   ├── data/                 # 数据处理模块
│   │   ├── __init__.py
│   │   ├── loader.py         # 数据加载器
│   │   ├── preprocessor.py   # 数据预处理
│   │   └── feature_engineering.py  # 特征工程
│   │
│   ├── models/               # 机器学习模型模块
│   │   ├── __init__.py
│   │   ├── base.py           # 模型基类
│   │   ├── high_value_predictor.py  # 高价值客户预测
│   │   └── customer_clustering.py   # 客户分群
│   │
│   ├── analysis/             # 分析模块
│   │   ├── __init__.py
│   │   ├── association.py    # 产品关联分析
│   │   ├── time_series.py    # 时间序列分析
│   │   └── explainer.py      # 模型可解释性(SHAP)
│   │
│   ├── visualization/        # 可视化模块
│   │   ├── __init__.py
│   │   ├── style.py          # 样式配置
│   │   ├── charts.py         # 图表生成器
│   │   └── dashboard.py      # Dashboard数据生成
│   │
│   ├── assistant/            # AI助手模块
│   │   ├── __init__.py
│   │   ├── agent.py          # 智能助手
│   │   ├── tools.py          # 助手工具
│   │   └── prompts.py        # 提示词模板
│   │
│   ├── web/                  # Web应用模块
│   │   ├── __init__.py
│   │   ├── app.py            # Flask应用
│   │   ├── api.py            # API路由
│   │   └── templates/        # HTML模板
│   │
│   └── utils/                # 工具模块
│       ├── __init__.py
│       ├── helpers.py        # 通用工具函数
│       └── logger.py         # 日志配置
│
├── scripts/                  # 独立脚本
│   ├── train_high_value.py   # 训练高价值预测模型
│   ├── run_clustering.py     # 运行客户分群
│   └── run_association.py    # 运行关联分析
│
├── data/                     # 数据目录
│   ├── customer_base.csv
│   └── customer_behavior_assets.csv
│
├── output/                   # 输出目录
│   ├── charts/              # 图表输出
│   ├── reports/             # 报告输出
│   └── logs/                # 日志
│
└── models/                   # 模型目录
    └── saved/               # 保存的模型文件
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+ (可选，用于数据库查询)

### 安装依赖

```bash
cd BankMind
pip install -r requirements.txt
```

### 配置环境变量

```bash
# DashScope API Key (用于 AI 助手)
export DASHSCOPE_API_KEY="your_api_key_here"

# 数据库配置 (可选)
export DB_HOST="localhost"
export DB_PORT="3306"
export DB_NAME="bank"
export DB_USER="root"
export DB_PASSWORD="password"
```

### 准备数据

将数据文件放入 `data/` 目录：
- `customer_base.csv` - 客户基础信息
- `customer_behavior_assets.csv` - 客户行为资产数据

## 📖 使用指南

### 命令行接口

```bash
# 查看帮助
python main.py --help

# 启动 AI 助手 (Web 界面)
python main.py assistant --mode gui

# 启动 AI 助手 (终端模式)
python main.py assistant --mode tui

# 启动可视化大屏
python main.py dashboard --port 5001

# 训练高价值预测模型
python main.py train --model high_value

# 训练客户分群模型
python main.py train --model clustering

# 执行产品关联分析
python main.py analyze --type association

# 执行资产趋势分析
python main.py analyze --type trend
```

### 独立脚本

```bash
# 训练高价值预测模型
python scripts/train_high_value.py

# 运行客户分群分析
python scripts/run_clustering.py --n-clusters 5

# 运行产品关联分析
python scripts/run_association.py --min-support 0.1
```

### Python API 使用

```python
# 数据加载
from src.data import DataLoader
loader = DataLoader()
df = loader.load_merged_data()

# 高价值客户预测
from src.models import HighValuePredictor
predictor = HighValuePredictor()
X, y = predictor.prepare_data(df)
predictor.fit(X, y)
predictions = predictor.predict(X_new)

# 客户分群
from src.models import CustomerClustering
clustering = CustomerClustering(n_clusters=3)
X = clustering.prepare_data(df)
clustering.fit(X)
labels = clustering.predict(X)

# 产品关联分析
from src.analysis import ProductAssociationAnalyzer
analyzer = ProductAssociationAnalyzer()
itemsets, rules = analyzer.analyze(df)
recommendations = analyzer.get_product_recommendations(["deposit_flag"])

# 生成图表
from src.visualization import ChartGenerator
chart = ChartGenerator()
chart.bar_chart(data, x="category", y="value", title="分析结果")
```

## 🛠️ 技术栈

| 类别 | 技术 |
|-----|------|
| **机器学习** | LightGBM, Scikit-learn, SHAP |
| **数据分析** | Pandas, NumPy, Statsmodels |
| **关联分析** | MLxtend (Apriori) |
| **可视化** | Matplotlib, ECharts |
| **Web 框架** | Flask |
| **AI 框架** | Qwen Agent, DashScope |
| **数据库** | MySQL, SQLAlchemy |

## 📊 数据说明

### customer_base.csv - 客户基础信息

| 字段 | 说明 |
|-----|------|
| customer_id | 客户唯一标识 |
| age | 年龄 |
| gender | 性别 |
| occupation | 职业 |
| monthly_income | 月收入 |
| city_level | 城市级别 |
| lifecycle_stage | 生命周期阶段 |

### customer_behavior_assets.csv - 客户行为资产

| 字段 | 说明 |
|-----|------|
| customer_id | 客户唯一标识 |
| total_assets | 总资产 |
| deposit_balance | 存款余额 |
| financial_balance | 理财余额 |
| fund_balance | 基金余额 |
| insurance_balance | 保险余额 |
| app_login_count | APP登录次数 |
| product_count | 持有产品数 |

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

MIT License

## 👤 作者

BankMind Team

---

**BankMind** - 让银行客户经营更智能 🚀

