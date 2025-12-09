#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
产品关联分析脚本

使用示例:
    python scripts/run_association.py
    python scripts/run_association.py --min-support 0.1
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data import DataLoader
from src.analysis import ProductAssociationAnalyzer
from src.config import settings


def main():
    parser = argparse.ArgumentParser(description="产品关联分析")
    parser.add_argument("--min-support", type=float, default=0.05, help="最小支持度")
    parser.add_argument("--min-lift", type=float, default=1.0, help="最小提升度")
    args = parser.parse_args()
    
    print("=" * 60)
    print("产品关联分析 (Apriori)")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n📊 加载数据...")
    loader = DataLoader()
    df = loader.load_merged_data()
    print(f"   数据量: {len(df)} 条记录")
    
    # 2. 初始化分析器
    print(f"\n🔧 初始化分析器...")
    print(f"   最小支持度: {args.min_support}")
    print(f"   最小提升度: {args.min_lift}")
    analyzer = ProductAssociationAnalyzer(
        min_support=args.min_support,
        min_lift=args.min_lift
    )
    
    # 3. 执行分析
    print("\n🚀 执行关联分析...")
    itemsets, rules = analyzer.analyze(df)
    
    # 4. 输出频繁项集
    print("\n📦 频繁产品组合:")
    print("-" * 50)
    for _, row in itemsets.head(10).iterrows():
        print(f"   {row['products']:30s} 支持度: {row['support']:.2%}")
    
    # 5. 输出关联规则
    print("\n🔗 关联规则 Top 10:")
    print("-" * 70)
    top_rules = analyzer.get_top_rules(10)
    for _, row in top_rules.iterrows():
        print(f"   {row['rule']:40s}")
        print(f"      置信度: {row['confidence']:.2%}  提升度: {row['lift']:.2f}")
    
    # 6. 产品推荐示例
    print("\n💡 产品推荐示例:")
    print("-" * 50)
    
    # 示例：持有存款的客户
    current_products = ["deposit_flag"]
    recommendations = analyzer.get_product_recommendations(current_products)
    print("   当前持有: 存款")
    print("   推荐产品:")
    for rec in recommendations[:3]:
        print(f"      - {rec['product']} (置信度: {rec['confidence']:.2%})")
    
    # 7. 保存结果
    print("\n💾 保存结果...")
    paths = analyzer.save_results()
    print(f"   频繁项集: {paths[0]}")
    print(f"   关联规则: {paths[1]}")
    
    print("\n✅ 分析完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

