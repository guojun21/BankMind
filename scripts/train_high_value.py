#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高价值客户预测模型训练脚本

使用示例:
    python scripts/train_high_value.py
    python scripts/train_high_value.py --data path/to/data.csv
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data import DataLoader
from src.models import HighValuePredictor
from src.visualization import ChartGenerator
from src.config import settings


def main():
    print("=" * 60)
    print("高价值客户预测模型训练")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n📊 加载数据...")
    loader = DataLoader()
    df = loader.load_merged_data()
    print(f"   数据量: {len(df)} 条记录")
    
    # 2. 初始化模型
    print("\n🔧 初始化模型...")
    predictor = HighValuePredictor(
        num_boost_round=100,
        params={
            "num_leaves": 31,
            "learning_rate": 0.05,
        }
    )
    
    # 3. 准备数据
    print("\n🔄 准备训练数据...")
    X, y = predictor.prepare_data(df)
    print(f"   特征数: {len(predictor.feature_names)}")
    print(f"   正样本比例: {y.mean():.2%}")
    
    # 4. 训练模型
    print("\n🚀 开始训练...")
    metrics = predictor.fit(X, y, test_size=0.2)
    
    # 5. 输出评估结果
    print("\n📈 模型评估结果:")
    print("-" * 40)
    for metric, value in metrics.items():
        print(f"   {metric:15s}: {value:.4f}")
    
    # 6. 特征重要性
    print("\n🎯 特征重要性排序:")
    print("-" * 40)
    importance = predictor.get_feature_importance()
    for _, row in importance.iterrows():
        print(f"   {row['feature']:25s}: {row['importance']:.0f}")
    
    # 7. 保存模型
    print("\n💾 保存模型...")
    model_path = predictor.save_model()
    print(f"   模型文件: {model_path}")
    
    # 8. 生成特征重要性图表
    print("\n📊 生成可视化图表...")
    chart = ChartGenerator()
    _, chart_path = chart.feature_importance_chart(
        importance,
        title="高价值客户预测 - 特征重要性",
        top_n=10
    )
    print(f"   图表文件: {chart_path}")
    
    print("\n✅ 训练完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

