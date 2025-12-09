# 数据文件说明

| 文件名 | 主要字段 | 用途 | 备注 |
|--------|----------|------|------|
| `customer_base.csv` | 客户编号、性别、年龄、风险偏好、资产等级等 | 作为客户主表，为建模和分析提供基础人口属性与账户信息 | 取代 legacy 目录中的同名文件；被数据加载器作为默认输入 |
| `customer_behavior_assets.csv` | 客户编号、交易笔数、交易金额、产品持有、最近登录时间等行为指标 | 结合 `customer_base.csv` 做特征工程、资产趋势分析以及高价值客户预测 | 与主表通过客户编号关联；包含时间序列字段 |
| `customer_cluster_result.csv` | 客户编号、聚类标签、群组画像指标 | 由旧版聚类脚本输出，在新结构下可作为评估或可视化示例数据 | 主要用于验证聚类模块和 Dashboard 展示 |
| `frequent_product_itemsets.csv` | 项集、支持度 | Apriori 频繁项集分析结果 | 供 `ProductAssociationAnalyzer` 或可视化模块直接读取，避免重复计算 |
| `product_association_rules.csv` | 前置项、后置项、支持度、置信度、提升度 | 关联规则分析结果 | 可被助手/可视化接口用于推荐策略或业务报告 |
| `legacy_case_raw/customer_base.csv` | 客户编号、人口属性、渠道信息 | 早期CASE版本的客户主表，保留最原始字段和记录 | 供比对历史口径或回滚使用，默认流程不会加载 |
| `legacy_case_raw/customer_behavior_assets.csv` | 客户编号、行为指标、资产指标 | 早期CASE版本行为资产明细，字段命名与新版略有不同 | 需要手动映射字段名后再用于训练或分析 |
| `BreadBasket_DMS.csv` | 交易时间、商品、交易ID | BreadBasket零售篮子分析样本，可用于Apriori教学或演示 | 由 `legacy/BreadBasket` 迁移，供关联分析脚本示例 |