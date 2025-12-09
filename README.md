# BankMind - AI运营助手

> 银行零售客户经营智能分析与营销系统，现已拆分为 `backend` 与 `frontend` 两个子项目。

## 📁 目录结构

```
BankMind/
├── backend/                 # Python/Flask/AI 模型
│   ├── main.py             # CLI 入口
│   ├── requirements.txt    # 依赖列表
│   ├── src/                # 业务代码（config/data/models/...）
│   ├── scripts/            # 独立运行脚本
│   ├── data/               # CSV 等业务数据
│   ├── models/             # 训练产出
│   └── output/             # 图表、日志等输出
│
├── frontend/               # 可视化大屏（ECharts 单页）
│   ├── dashboard.html
│   └── static/
│
├── legacy/                 # 老版本代码与参考资料
└── wrapDoc/                # 项目推进文档
```

## ✨ 核心能力

- 📊 **可视化大屏**：`frontend/dashboard.html` 通过调用后端 `/api/*` 数据接口展示客户画像、资产分布、风险预警等指标。
- 🎯 **高价值客户预测**：`backend/src/models/high_value_predictor.py` 使用 LightGBM + SHAP 评估客户成长潜力。
- 👥 **客户分群与关联分析**：`backend/src/models/customer_clustering.py`、`backend/src/analysis/association.py` 支持聚类与 Apriori。
- 🤖 **智能助手**：`backend/src/assistant/agent.py` 基于 Qwen Agent 支持自然语言问答、SQL 查询及图表生成。

## 🚀 快速开始

```bash
# 安装依赖
cd BankMind/backend
pip install -r requirements.txt

# 准备数据（复制/放置 CSV 到 backend/data/）
cp path/to/customer_base.csv backend/data/
cp path/to/customer_behavior_assets.csv backend/data/

# 启动 Dashboard 接口（默认 5001 端口）
python main.py dashboard --host 0.0.0.0 --port 5001

# 启动 AI 助手
python main.py assistant --mode gui

# 训练模型 / 运行分析
python main.py train --model high_value
python main.py analyze --type association
```

前端无需额外构建，直接在浏览器打开 `frontend/dashboard.html`，或将其托管到任意静态服务器。默认会请求 `http://localhost:5001` 的后端 API；若需跨域或自定义 API 地址，可在 HTML 中调整 `fetch` 请求或通过反向代理处理。

## 📊 数据说明

- `backend/data/customer_base.csv`：客户基础属性
- `backend/data/customer_behavior_assets.csv`：客户行为/资产指标
- 其它 CSV（如 `customer_cluster_result.csv`、`BreadBasket_DMS.csv`）供示例分析或可视化演示

## 🛠️ 技术栈

| 类别 | 使用技术 |
|------|----------|
| Web/API | Flask, ECharts |
| 机器学习 | LightGBM, Scikit-learn, SHAP |
| 数据分析 | Pandas, NumPy, Statsmodels |
| AI 助手 | Qwen Agent, DashScope |

## 🤝 贡献

欢迎提交 Issue 或 PR，一起完善 BankMind！👏
