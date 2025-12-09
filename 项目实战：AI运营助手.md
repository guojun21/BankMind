# 项目实战：AI运营助手（百万客群经营）

> 今天的学习目标

## 学习目标

- 搭建可视化大屏
- 分类模型（高价值客户预测）
  - 逻辑回归
  - 决策树
  - XGBoost/LightGBM
- 聚类分析（客户分群）
- 关联分析（产品组合推荐）
- 时间序列分析（资产变动预测）

---

## 一、CASE：百万客群经营

银行零售客户经营项目，旨在通过整合客户基础信息、资产、行为等多维度数据，利用数据分析和智能算法，提升客户价值挖掘、精准营销和风险管理能力，助力银行实现客户资产增长和业务创新。

### 1.1 数据表说明

- `customer_base.csv`：客户基础信息表，一个客户一条记录
- `customer_behavior_assets.csv`：客户行为资产表，一个客户每月一条记录

#### customer_base.csv 字段

| 字段名 | 含义说明 |
|--------|----------|
| customer_id | 客户唯一标识 |
| name | 客户姓名 |
| age | 客户年龄 |
| gender | 客户性别 |
| occupation | 客户职业 |
| occupation_type | 职业类型（如专业人士、私营业主等） |
| monthly_income | 月收入 |
| open_account_date | 开户日期 |
| lifecycle_stage | 客户生命周期阶段（如新客户、成熟客户等） |
| marriage_status | 婚姻状况 |
| city_level | 城市级别（如一线、二线城市） |
| branch_name | 所属银行网点名称 |

#### customer_behavior_assets.csv 字段

| 字段名 | 含义说明 |
|--------|----------|
| id | 记录唯一标识 |
| customer_id | 客户唯一标识（与基础表关联） |
| total_assets | 客户总资产 |
| deposit_balance | 存款余额 |
| financial_balance | 理财余额 |
| fund_balance | 基金余额 |
| insurance_balance | 保险产品余额 |
| asset_level | 资产等级区间（如"50-80万"） |
| deposit_flag | 是否有存款产品（0/1） |
| financial_flag | 是否有理财产品（0/1） |
| fund_flag | 是否有基金产品（0/1） |
| insurance_flag | 是否有保险产品（0/1） |
| product_count | 持有产品数量 |
| financial_repurchase_count | 理财复购次数 |
| credit_card_monthly_expense | 信用卡月均消费 |
| investment_monthly_count | 月均投资次数 |
| app_login_count | 手机银行登录次数 |
| app_financial_view_time | 手机银行理财浏览时长 |
| app_product_compare_count | 手机银行产品对比次数 |
| last_app_login_time | 最近一次手机银行登录时间 |
| last_contact_time | 最近一次客户经理联系时间 |
| contact_result | 最近一次联系结果（如"成功"、"未接通"等） |
| marketing_cool_period | 营销冷静期 |
| stat_month | 统计月份 |

### 1.2 项目 TO DO

1. **搭建可视化大屏开发**
   - 核心指标卡片：客户总数、总资产、平均资产、活跃客户数、产品复购率等
   - 客户结构与分布
   - 客户资产与产品分析
   - 客户行为与活跃度
   - 风险与预警分析（如有相关字段）
2. **分类算法**（预测高价值客户）
3. **聚类分析**（客户分群）
4. **关联分析**（产品组合推荐）
5. **时间序列分析**（资产变动预测）

---

## 二、搭建可视化大屏

### 2.1 数据探索

> 帮我编写Python，读取 customer_base.csv 和 customer_behavior_assets.csv 的前5行数据，通过运行，可以让AI看到前5行的数据，方便理解数据表的字段含义。

### 2.2 项目说明文档

> 编写项目说明.txt，方便AI理解项目的作用。

**AI打造助手的过程**，并非一帆风顺，可以将中间过程文档进行保存。比如：项目说明（类似需求文档），关键字段整理等，方便AI重构项目。

**核心目标**：通过数据驱动精准营销，提升百万级客户转化率，降低营销成本与客户流失率。

**核心任务**：
- 客户分层分析（资产/年龄/职业分布）
- 构建预测模型（AUC≥0.85）
- 分群策略（如高复购、中产家庭等群体）
- 优化线上线下触达方式

**关键举措**：

1. **数据分析**：可视化资产分层、高潜力客户画像，分析行为与资产相关性
2. **智能建模**：预测百万级客户（SHAP解释关键因子），聚类分群并定制策略（如私募理财推荐给高收入客群）
3. **精准营销**：动态更新高潜力名单，结合APP弹窗、电话外呼等渠道，设定转化率监控与预警机制

### 2.3 字段含义整理

> 基于 @项目说明.txt 和这两个数据表的前5行数据，帮我理解这两张数据表的字段含义。

让AI理解数据表的字段含义，也可以写入到 `.md` 中，方便后续使用。

> 将字段含义写入到 数据表字段含义.md

**Markdown格式是AI最方便理解的格式。**

### 2.4 看板规划

> 我想搭建可视化大屏，针对 @项目说明.txt 以及当前的数据表，都有哪些图表可以展示，先说明思路即可。

让AI输出看板规划，然后筛选适合的图表。

> 帮我规划可视化大屏，选择适合的图表样式，整体图表数量不超过5个，使用 Flask + Echarts。

### 2.5 前端调试

**Thinking**：如何查看前端页面的问题？

> Console中有报错，帮我查看。

**解决方案**：将 `echarts.min.js` 下载下来，新建文件夹 `static`，并放到 static 文件夹下面。

下载地址：https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js

### 2.6 图表优化

> 这个漏斗图的逻辑关系不对吧，也帮我统计下这些人的数量。

> 去掉客户生命周期中的流失预警客户、流失客户的显示。

---

## 三、分类算法（预测高价值客户）

### 3.1 场景描述

**TO DO**：预测客户未来3个月资产提升至100万+的概率

#### 场景1：高收入高活跃型客户资产跃升

- 客户当前资产为60万，月收入较高（如3万元以上），且近3个月手机银行活跃度高、理财复购频繁
- 模型预测其未来3个月资产有望突破100万
- **业务动作**：提前推送高端理财、专属客户经理服务，提升客户粘性

#### 场景2：多产品持有型客户资产跃升

- 客户当前资产为70万，持有多种金融产品（存款、理财、基金、保险均有涉猎），产品复购率高
- 模型预测其资产组合优化后，未来半年内资产有望突破100万
- **业务动作**：定制产品组合推荐，推动交叉销售，助力客户资产快速增长

#### 场景3：年轻成长型客户资产跃升

- 客户年龄30岁左右，当前资产为50万，近半年收入持续增长，投资行为活跃（月均投资次数高）
- 模型预测未来一年资产有望突破100万
- **业务动作**：为其提供成长激励、资产配置建议，提升客户粘性

### 3.2 建模流程

**Thinking**：整个建模的流程是怎样的？

1. **样本定义**：设定目标变量（如：未来3个月资产是否达到100万+，1=是，0=否）。通过历史数据回溯，构建训练样本。
2. **数据准备与特征工程**：整合客户基础信息、资产、产品、行为等数据。选择与高净值成长相关的特征（当前资产、月收入、产品持有数、理财复购次数、活跃度等）。处理缺失值、异常值，进行特征编码和归一化。
3. **模型选择**：选择合适的分类算法，进行模型训练。
4. **模型训练与评估**：评估模型效果（AUC、准确率、召回率等），调优参数。

### 3.3 逻辑回归

> 帮我使用逻辑回归，预测客户未来3个月资产提升至100万+的概率，输出逻辑回归的系数，帮进行可视化（可以看出系数正负的），编写新Python：`logistic_regression_asset_prediction.py`

**回归系数结果**：

```
feature                           coef
lifecycle_stage_新客户            -7.472111
lifecycle_stage_成长客户          -3.936564
occupation_type_传统行业          -2.288765
monthly_income                     1.840650
lifecycle_stage_成熟客户          -1.603252
lifecycle_stage_忠诚客户           1.195508
occupation_type_事业单位          -1.073051
occupation_type_企业高管           0.721852
occupation_行政人员               -0.682615
occupation_事业单位职工           -0.676363
occupation_企业CFO                 0.584811
occupation_公务员                 -0.583112
occupation_type_私营业主           0.570253
occupation_律师                    0.549541
occupation_会计师                  0.515290
……
```

**Thinking**：如何理解逻辑回归的系数？

> 帮我对逻辑回归系数进行解释（正负项），哪些客户未来3个月资产容易提升至100万+，哪些客户不容易提升，以及后续决策建议，写入 `逻辑回归解释.md`

### 3.4 决策树

> 帮我使用决策树（depth=4），预测客户未来3个月资产是否能提升至100万+，不需要对特征进行归一化处理，对决策树进行可视化（文本打印及图片生成），编写新Python：`decision_tree_asset_prediction.py`

**决策树结构**：

```
|--- monthly_income <= 41036.85
|   |--- lifecycle_stage_忠诚客户 <= 0.50
|   |   |--- monthly_income <= 33563.26
|   |   |   |--- monthly_income <= 25130.65
|   |   |   |   |--- weights: [3507.00, 15.00] class: 0
|   |   |   |--- monthly_income > 25130.65
|   |   |   |   |--- weights: [1361.00, 87.00] class: 0
|   |   |--- monthly_income > 33563.26
|   |   |   |--- lifecycle_stage_成长客户 <= 0.50
|   |   |   |   |--- weights: [644.00, 172.00] class: 0
|   |   |   |--- lifecycle_stage_成长客户 > 0.50
|   |   |   |   |--- weights: [323.00, 0.00] class: 0
|   |--- lifecycle_stage_忠诚客户 > 0.50
|   |   |--- monthly_income <= 28820.59
|   |   |   |--- monthly_income <= 22169.09
|   |   |   |   |--- weights: [420.00, 14.00] class: 0
|   |   |   |--- monthly_income > 22169.09
|   |   |   |   |--- weights: [160.00, 63.00] class: 0
|   |   |--- monthly_income > 28820.59
|   |   |   |--- monthly_income <= 34880.59
|   |   |   |   |--- weights: [78.00, 77.00] class: 0
|   |   |   |--- monthly_income > 34880.59
|   |   |   |   |--- weights: [39.00, 119.00] class: 1
|--- monthly_income > 41036.85
|   |--- lifecycle_stage_新客户 <= 0.50
|   |   |--- lifecycle_stage_成长客户 <= 0.50
|   |   |   |--- monthly_income <= 59455.97
|   |   |   |   |--- weights: [455.00, 708.00] class: 1
|   |   |   |--- monthly_income > 59455.97
|   |   |   |   |--- weights: [41.00, 589.00] class: 1
|   |   |--- lifecycle_stage_成长客户 > 0.50
|   |   |   |--- monthly_income <= 64244.12
|   |   |   |   |--- weights: [440.00, 42.00] class: 0
|   |   |   |--- monthly_income > 64244.12
|   |   |   |   |--- weights: [110.00, 98.00] class: 0
|   |--- lifecycle_stage_新客户 > 0.50
|   |   |--- monthly_income <= 98082.99
|   |   |   |--- weights: [436.00, 0.00] class: 0
|   |   |--- monthly_income > 98082.99
|   |   |   |--- age <= 36.50
|   |   |   |   |--- weights: [0.00, 1.00] class: 1
|   |   |   |--- age > 36.50
|   |   |   |   |--- weights: [1.00, 0.00] class: 0
```

> 帮我对决策树进行解释，哪些客户未来3个月资产容易提升至100万+，哪些不容易，以及后续决策建议，写入 `决策树解释.md`

### 3.5 LightGBM

> 帮我使用LightGBM，预测客户未来3个月资产是否能提升至100万+，输出特征重要性排序（文本打印及图片生成），编写新Python：`lightgbm_asset_prediction.py`

**特征重要性排序**：

```
feature                        importance
monthly_income                       1018
age                                   611
gender_男                             130
lifecycle_stage_忠诚客户              117
lifecycle_stage_成熟客户              108
lifecycle_stage_成长客户              101
lifecycle_stage_新客户                 78
city_level_二线城市                    76
marriage_status_未婚                   61
occupation_type_私营业主               47
occupation_type_传统行业               46
occupation_type_金融从业者             40
……
```

> 帮我对LightGBM特征重要性进行解释，能看出来哪些客户未来3个月资产能提升至100万+，哪些不能，如果想基于LightGBM得出有效结论，还需要做什么？写入 `LightGBM解释.md`

### 3.6 SHAP 分析

**SHAP（SHapley Additive exPlanations）**：一种基于博弈论的模型可解释性方法，适用于任何分类模型，能量化每个特征对单个预测结果的贡献值。

| 模型 | 适用性 | 原因 |
|------|--------|------|
| 逻辑回归 | ✓ | 线性模型，SHAP可精确计算权重贡献（等同于系数符号和大小） |
| 决策树（depth=4） | ✓ | 树结构简单，SHAP能清晰展示分裂节点的特征重要性 |
| LightGBM | ✓✓ | 高性能树模型，SHAP能处理复杂交互效应，推荐使用 |

**Thinking**：SHAP在高价值客户预测中的作用？

1. **全局解释**：展示哪些特征整体上对"高价值客户"预测最重要
2. **局部解释**：针对单个客户，解释其被预测为"未来3个月资产能否提升至100万+"的原因，量化每个特征的正负影响

> 帮我使用SHAP分析，进行全局解释和局部解释，基于 @lightgbm_asset_prediction.py 编写新的Python代码：`shap_lightgbm_explain.py`

**全局特征重要性（均值绝对值排序）**：

```
feature                        mean_abs_shap
monthly_income                     2.267403
lifecycle_stage_新客户             1.223093
lifecycle_stage_成长客户           1.153598
lifecycle_stage_成熟客户           0.420187
occupation_type_传统行业           0.376689
lifecycle_stage_忠诚客户           0.333227
age                                0.269127
gender_男                          0.056825
occupation_type_私营业主           0.055909
occupation_type_互联网从业者       0.045576
occupation_type_企业高管           0.033654
……
```

**单个客户SHAP值**（按绝对值排序，正值=正向影响，负值=负向影响）：

```
feature                        shap_value    feature_value
lifecycle_stage_新客户           -5.640769          True
monthly_income                    1.342016      49458.85
lifecycle_stage_成长客户          0.509974         False
lifecycle_stage_成熟客户          0.228239         False
occupation_type_传统行业          0.164528         False
occupation_律师                   0.145225          True
……
```

---

## 四、聚类分析（客户分群）

> @项目说明.txt @数据表字段含义.md，我想使用聚类分析（客户分群）

**场景**：将客户分为高复购、中产家庭、年轻高消费等群组。

> 帮我使用聚类算法，编写新的Python

**聚类结果（各群组特征均值）**：

| cluster | age | monthly_income | total_assets | financial_repurchase_count | credit_card_monthly_expense | investment_monthly_count | app_login_count |
|---------|-----|----------------|--------------|----------------------------|----------------------------|-------------------------|-----------------|
| 0 | 37.76 | 40311.63 | 710325.8 | 0.06 | 10415.73 | 2.65 | 8.52 |
| 1 | 45.45 | 34566.36 | 689729.0 | 1.15 | 8627.05 | 1.56 | 5.60 |
| 2 | 53.62 | 30496.06 | 602270.0 | 0.00 | 7494.61 | 0.32 | 4.31 |
| 3 | 36.11 | 38694.57 | 534393.3 | 0.00 | 10363.29 | 0.11 | 8.81 |
| 4 | 48.95 | 65515.07 | 2010402.0 | 0.12 | 23146.09 | 0.61 | 5.33 |
| 5 | 40.07 | 20045.68 | 201767.1 | 0.00 | 4887.75 | 0.14 | 3.58 |

**每类客户数量**：

| cluster | 数量 |
|---------|------|
| 0 | 741 |
| 1 | 1233 |
| 2 | 2617 |
| 3 | 1548 |
| 4 | 1129 |
| 5 | 2732 |

> 帮我打印出来完整的特征均值，然后再做分析

> 帮我理解各群组特征均值，并说明这6个cluster分别代表什么特征？是属于高复购、中产家庭、年轻高消费等群组么？帮我理解并对聚类好的群体进行命名。

---

## 五、关联分析（产品组合推荐）

> @项目说明.txt @数据表字段含义.md，我想使用关联分析（产品组合推荐）

**场景**：挖掘存款/理财/基金/保险的频繁组合模式。

> 帮我使用Apriori算法，编写新的Python

**Thinking**：查看输出的频繁项集，以及产品关联规则，有什么问题么？

> 这里的lift都为1，帮我对原数据进行分析，是不是原数据中不能找到有效的关联规则？

**分析结论**：当时数据模拟的时候，没有考虑到关联规则的场景，产品购买相对独立了，没有进行关联。

---

## 六、时间序列分析（资产变动预测）

> @项目说明.txt @数据表字段含义.md，我想使用时间序列分析（资产变动预测）

**场景**：预测客户未来季度AUM增长趋势。

> 帮我使用ARIMA，编写新的Python

**未来4个季度AUM预测值**：

| 日期 | 预测值 |
|------|--------|
| 2024-03-31 | 1,218,434 |
| 2024-06-30 | 1,264,666 |
| 2024-09-30 | 1,309,756 |
| 2024-12-31 | 1,353,731 |

**Thinking**：这里做的是整体客户未来季度的AUM趋势分析和预测，能否改成个体用户的AUM趋势分析与预测？

---

## 七、替换模拟数据

将以下代码中的数据都换成二组模拟数据.csv：

- `logistic_regression_high_value.py`
- `decision_tree_high_value.py`
- `lightgbm_high_value.py`
- `clustering_customer_segmentation.py`
- `apriori_product_combination.py`
- `arima_asset_trend.py`

### 7.1 更新后的决策树结构

```
|--- total_assets <= 927967.56
|   |--- weights: [777.00, 0.00] class: 0
|--- total_assets > 927967.56
|   |--- total_assets <= 986557.41
|   |   |--- investment_monthly_count <= 2.48
|   |   |   |--- weights: [0.00, 2.00] class: 1
|   |   |--- investment_monthly_count > 2.48
|   |   |   |--- financial_repurchase_count <= 9.59
|   |   |   |   |--- weights: [2.00, 0.00] class: 0
|   |   |   |--- financial_repurchase_count > 9.59
|   |   |   |   |--- weights: [0.00, 1.00] class: 1
|   |--- total_assets > 986557.41
|   |   |--- weights: [0.00, 18.00] class: 1
```

### 7.2 更新后的LightGBM特征重要性

```
feature                        importance
total_assets                        417
monthly_income                      194
financial_repurchase_count          185
app_login_count                     117
product_count                         0
investment_monthly_count              0
```

### 7.3 更新后的ARIMA预测

**未来4个月AUM预测值**：

| 日期 | 预测值 |
|------|--------|
| 2025-05-31 | 182,389.51 |
| 2025-06-30 | 182,861.73 |
| 2025-07-31 | 182,841.59 |
| 2025-08-31 | 182,842.45 |

> @dashboard_app.py 这里的数据都换成二组模拟数据.csv

---

## 八、Summary

### 8.1 项目交付物

**一个可视化大屏**：`dashboard_app.py`

**6个模型及分析结果**：

| 模型 | 文件名 |
|------|--------|
| 逻辑回归 | `logistic_regression_high_value.py` |
| 决策树 | `decision_tree_high_value.py` |
| LightGBM | `lightgbm_high_value.py` |
| 聚类分析 | `clustering_customer_segmentation.py` |
| 关联分析 | `apriori_product_combination.py` |
| 时间序列 | `arima_asset_trend.py` |

### 8.2 模型洞察结果

- 哪些客户未来3个月资产可以达到100万+
- 哪些客户未来3个月资产会低于100万
- 后续的经营策略

### 8.3 延伸思考

**Thinking**：能否结合大模型，与可视化大屏进行互动？

**数据分析问题示例**：

- 我行目前有多少客户？总资产管理规模是多少？
- 客户的平均资产是多少？高净值客户的占比如何？
- 客户年龄分布情况如何？哪个年龄段客户最多？
- 不同客户等级（普通、潜力、临界、高净值）的分布情况怎样？
- 客户在不同城市等级（一线、二线、三线）的分布如何？
- 不同职业客户的产品偏好有什么差异？
- 客户的网银登录次数和网点访问次数分布情况如何？
- 年龄与手机银行使用频率有何关联？

**Thinking**：能否结合大模型，与6个预测模型进行互动？

**模型洞察与预测问题示例**：

- 客户"CUST000172"成为高价值客户的概率是多少？
- 影响客户价值的最重要因素有哪些？
- 基于客户"CUST000116"的现有产品持有情况，应该向其推荐什么产品？
- 在高净值客户中，最常见的产品组合是什么？
- 客户"CUST000055"的资产在未来可能呈现什么样的趋势？
- 未来6个月内，可能出现资产下降的客户有哪些？如何提前进行干预？

---

## 九、AI大模型结合

### 9.1 数据库配置

**TO DO**：使用AI大模型进行数据查询与分析

- 数据表：`enterprise_credit_clients`
- 连接：`bank123:bank321@rm-uf6z891lon6dxuqblqo.mysql.rds.aliyuncs.com:3306`
- 数据库：`bank2`

### 9.2 建表语句

> @assistant_tiket_bot-3.py 基于这个，改成对公授信客户助手，对应的建表语句也需要替换

```sql
CREATE TABLE customer_data (
    customer_id VARCHAR(10) PRIMARY KEY COMMENT '客户编号',
    gender CHAR(1) COMMENT '性别: M-男, F-女',
    age INT COMMENT '年龄',
    occupation VARCHAR(20) COMMENT '职业',
    marital_status VARCHAR(10) COMMENT '婚姻状况: 已婚、未婚、离异',
    city_level VARCHAR(10) COMMENT '城市等级: 一线、二线、三线',
    account_open_date VARCHAR(10) COMMENT '开户日期',
    total_aum DECIMAL(18, 2) COMMENT '总资产管理规模',
    deposit_balance DECIMAL(18, 2) COMMENT '存款余额',
    wealth_management_balance DECIMAL(18, 2) COMMENT '理财余额',
    fund_balance DECIMAL(18, 2) COMMENT '基金余额',
    insurance_balance DECIMAL(18, 2) COMMENT '保险余额',
    deposit_balance_monthly_avg DECIMAL(18, 2) COMMENT '存款月均余额',
    wealth_management_balance_monthly_avg DECIMAL(18, 2) COMMENT '理财月均余额',
    fund_balance_monthly_avg DECIMAL(18, 2) COMMENT '基金月均余额',
    insurance_balance_monthly_avg DECIMAL(18, 2) COMMENT '保险月均余额',
    monthly_transaction_count DECIMAL(10, 2) COMMENT '月均交易次数',
    monthly_transaction_amount DECIMAL(18, 2) COMMENT '月均交易金额',
    last_transaction_date VARCHAR(10) COMMENT '最近交易日期',
    mobile_bank_login_count INT COMMENT '手机银行登录次数',
    branch_visit_count INT COMMENT '网点访问次数',
    last_mobile_login VARCHAR(10) COMMENT '最近手机银行登录日期',
    last_branch_visit VARCHAR(10) COMMENT '最近网点访问日期',
    customer_tier VARCHAR(10) COMMENT '客户等级: 普通、潜力、临界、高净值'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='银行客户数据表';

-- 创建索引
CREATE INDEX idx_customer_tier ON customer_data(customer_tier);
CREATE INDEX idx_age ON customer_data(age);
CREATE INDEX idx_total_aum ON customer_data(total_aum);
CREATE INDEX idx_occupation ON customer_data(occupation);
CREATE INDEX idx_city_level ON customer_data(city_level);
CREATE INDEX idx_account_open_date ON customer_data(account_open_date);
CREATE INDEX idx_last_transaction_date ON customer_data(last_transaction_date);
```

> 使用qwen-agent，编写新的python

### 9.3 AI交互示例

| 问题 | 回答示例 |
|------|----------|
| 我行目前有多少客户？总资产管理规模是多少？ | - |
| 客户的平均资产是多少？高净值客户的占比如何？ | - |
| 客户年龄分布情况如何？哪个年龄段客户最多？ | - |
| 不同客户等级的分布情况怎样？ | - |
| 客户在不同城市等级的分布如何？ | - |
| 不同职业客户的产品偏好有什么差异？ | - |
| 客户的网银登录次数和网点访问次数分布情况如何？ | - |
| 年龄与手机银行使用频率有何关联？ | - |
| 多少客户在过去三个月内没有任何交易行为？ | 78 |

---

## 十、打卡作业：百万客群经营助手

开发完整的百万客群经营助手，提供：

- **数据查询与可视化**
- **模型洞察**：哪些客户未来3个月资产容易提升至100万+，哪些不容易，以及后续决策建议
- **SHAP分析**：全局解释（识别哪些特征整体上对"高价值客户"预测最重要）和局部解释
- **关联分析**
- **时间序列分析**
- ……

**核心理念**：通过交互式BI，让大模型与专业模型进行深度结合。

| 模块 | 职责 |
|------|------|
| **大模型** | 与用户交互，理解用户的问题并回答 |
| **专业模型** | 提供建模，对潜在高价值客户进行预测，关联推荐等 |

---

**Thank You**

*Using data to solve problems*
