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
├── backend/                   # 后端（Flask + 数据&模型）
│   ├── main.py               # 命令行入口
│   ├── requirements.txt      # 依赖列表
│   ├── src/                  # 业务代码
│   │   ├── config/           # 配置模块
│   │   ├── data/             # 数据处理
│   │   ├── models/           # 机器学习模型
│   │   ├── analysis/         # 统计分析
│   │   ├── visualization/    # 图表生成
│   │   ├── assistant/        # AI 助手
│   │   ├── web/              # Flask 应用 (API)
│   │   └── utils/            # 工具方法
│   ├── scripts/              # 独立运行脚本
│   ├── data/                 # 业务数据（CSV 等）
│   ├── models/               # 训练产出
│   └── output/               # 报表/日志等输出
│
├── frontend/                 # 前端可视化大屏
│   ├── dashboard.html        # 单页 ECharts 大屏
│   └── static/               # 静态资源（可选）
│
├── legacy/                   # 老版本代码与参考资料
│   └── ...                   # 保留只读
│
└── wrapDoc/                  # 项目过程文档
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+ (可选，用于数据库查询)

### 安装依赖

```bash
cd BankMind/backend
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

将数据文件放入 `backend/data/` 目录：
- `customer_base.csv` - 客户基础信息
- `customer_behavior_assets.csv` - 客户行为资产数据

## 📖 使用指南

### 命令行接口

> 先进入 `BankMind/backend` 目录后再执行以下命令。

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

> 同样需要在 `BankMind/backend` 目录中执行。

```bash
# 训练高价值预测模型
python scripts/train_high_value.py

# 运行客户分群分析
python scripts/run_clustering.py --n-clusters 5

# 运行产品关联分析
python scripts/run_association.py --min-support 0.1
```

### Python API 使用

> 在 `BankMind/backend` 目录中通过 Python 交互或脚本引用。

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

