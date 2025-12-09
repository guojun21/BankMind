#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
客户分群分析脚本

使用示例:
    python scripts/run_clustering.py
    python scripts/run_clustering.py --n-clusters 5
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data import DataLoader
from src.models import CustomerClustering
from src.visualization import ChartGenerator
from src.config import settings


def main():
    parser = argparse.ArgumentParser(description="客户分群分析")
    parser.add_argument("--n-clusters", type=int, default=3, help="聚类数量")
    args = parser.parse_args()
    
    print("=" * 60)
    print("客户分群分析")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n📊 加载数据...")
    loader = DataLoader()
    df = loader.load_merged_data()
    print(f"   数据量: {len(df)} 条记录")
    
    # 2. 初始化模型
    print(f"\n🔧 初始化聚类模型 (K={args.n_clusters})...")
    clustering = CustomerClustering(n_clusters=args.n_clusters)
    
    # 3. 准备数据
    print("\n🔄 准备聚类数据...")
    X = clustering.prepare_data(df)
    print(f"   使用特征: {clustering.features}")
    
    # 4. 训练模型
    print("\n🚀 执行聚类...")
    metrics = clustering.fit(X)
    
    # 5. 预测并添加标签
    df["cluster"] = clustering.predict(X)
    
    # 6. 输出评估结果
    print("\n📈 聚类评估结果:")
    print("-" * 40)
    for metric, value in metrics.items():
        print(f"   {metric:25s}: {value:.4f}")
    
    # 7. 各群组统计
    print("\n👥 各群组客户数:")
    print("-" * 40)
    for cluster_id in range(args.n_clusters):
        count = (df["cluster"] == cluster_id).sum()
        pct = count / len(df) * 100
        label = clustering.CLUSTER_LABELS.get(cluster_id, f"群组{cluster_id}")
        print(f"   {label}: {count} ({pct:.1f}%)")
    
    # 8. 各群组特征均值
    print("\n📊 各群组特征均值:")
    print("-" * 40)
    summary = df.groupby("cluster")[clustering.features].mean()
    print(summary.round(2).to_string())
    
    # 9. 保存结果
    print("\n💾 保存结果...")
    output_path = settings.OUTPUT_DIR / "reports" / "customer_clusters.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df[["customer_id"] + clustering.features + ["cluster"]].to_csv(
        output_path, index=False, encoding="utf-8-sig"
    )
    print(f"   结果文件: {output_path}")
    
    # 10. 生成可视化图表
    print("\n📊 生成可视化图表...")
    chart = ChartGenerator()
    
    # PCA 降维可视化
    X_pca = clustering.get_pca_coordinates(X)
    df["pca_1"] = X_pca[:, 0]
    df["pca_2"] = X_pca[:, 1]
    
    _, chart_path = chart.cluster_scatter(
        df, "pca_1", "pca_2",
        cluster_col="cluster",
        title="客户聚类分布 (PCA降维)"
    )
    print(f"   图表文件: {chart_path}")
    
    print("\n✅ 分析完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

