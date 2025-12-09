# BankMind - AI运营助手

> 银行零售客户经营智能分析与营销系统

## 📋 项目简介

BankMind 是一个面向银行零售业务的**数据驱动精准营销**解决方案，通过机器学习与数据分析技术，帮助银行实现百万级客群的高效经营，提升客户转化率并降低营销成本。

## ✨ 核心功能

### 1. 📊 可视化大屏
基于客户基础信息和行为资产数据，搭建动态可视化大屏，展示：
- 客户结构分析
- 资产分布统计
- 产品持有情况
- 行为活跃度监控
- 风险预警指标

### 2. 🎯 高价值客户预测
使用多种机器学习算法（逻辑回归、决策树、LightGBM）预测客户未来3个月资产提升至100万+的概率：
- 模型可解释性分析（SHAP）
- 特征重要性排序
- 客户价值评分

### 3. 👥 客户分群分析
基于客户属性、资产、产品、行为特征进行聚类分析：
- 高复购客户群体
- 中产家庭群体
- 年轻高消费群体
- 差异化运营策略

### 4. 🔗 产品关联分析
使用 Apriori 算法挖掘产品组合模式：
- 存款、理财、基金、保险产品关联规则
- 高频产品组合推荐
- 交叉销售机会识别

### 5. 📈 资产趋势预测
使用时间序列分析（ARIMA）预测客户未来季度 AUM 增长趋势：
- 资产波动预测
- 增长/流失风险预警
- 客户分层管理

### 6. 🤖 智能对话助手
基于 Qwen Agent 框架的智能对话助手：
- 自然语言查询客户数据
- 自动生成并执行 SQL
- 自动生成可视化图表
- 支持 Web 界面和命令行交互

## 🛠️ 技术栈

- **机器学习**: LightGBM, Scikit-learn, SHAP
- **数据分析**: Pandas, NumPy
- **可视化**: Matplotlib, ECharts, Flask
- **AI 框架**: Qwen Agent, DashScope
- **数据库**: MySQL
- **Web 框架**: Flask

## 📁 项目结构

```
BankMind/
├── 【完成参考】CASE-百万客群经营/    # 主要功能模块
│   ├── bank_customer_assistant.py   # 智能对话助手
│   ├── dashboard_app.py              # 可视化大屏
│   ├── lightgbm_high_value.py       # LightGBM 预测模型
│   ├── clustering_customer_segmentation.py  # 客户分群
│   ├── apriori_product_combination.py       # 产品关联分析
│   ├── arima_asset_trend.py                 # 资产趋势预测
│   └── ...
├── CASE-百万客群经营/                # 数据文件
└── BreadBasket/                      # 关联分析示例
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

### 运行智能助手

```bash
cd 【完成参考】CASE-百万客群经营/
python bank_customer_assistant.py
```

### 运行可视化大屏

```bash
python dashboard_app.py
# 访问 http://localhost:5000
```

## 📊 数据说明

项目使用银行客户数据，包括：
- **客户基础信息**: 年龄、职业、收入、城市等级等
- **客户行为数据**: 交易次数、登录频率、产品持有等
- **资产数据**: 存款、理财、基金、保险余额等

## 📝 使用示例

### 智能助手查询示例

```
用户: 客户年龄分布情况如何？哪个年龄段客户最多？
助手: [自动生成SQL查询，返回统计表格和可视化图表]

用户: 预测哪些客户在未来6个月内可能成为高净值客户？
助手: [调用预测模型，返回客户列表和概率评分]
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👤 作者

BankMind Team

---

**BankMind** - 让银行客户经营更智能 🚀

