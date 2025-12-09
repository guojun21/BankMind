#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BankMind - 银行零售客户经营智能分析系统

主入口文件，提供命令行接口
"""

import argparse
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent))


def run_assistant(mode: str = "gui", port: int = 7860):
    """运行 AI 助手"""
    from src.assistant import BankCustomerAssistant
    
    assistant = BankCustomerAssistant()
    if mode == "tui":
        assistant.run_tui()
    else:
        assistant.run_gui(port=port)


def run_dashboard(host: str = "0.0.0.0", port: int = 5001, debug: bool = True):
    """运行可视化大屏"""
    from src.web.app import run_server
    run_server(host=host, port=port, debug=debug)


def run_training(model_type: str = "high_value"):
    """运行模型训练"""
    from src.data import DataLoader
    from src.models import HighValuePredictor, CustomerClustering
    
    print(f"开始训练 {model_type} 模型...")
    
    loader = DataLoader()
    
    if model_type == "high_value":
        # 高价值客户预测模型
        predictor = HighValuePredictor()
        df = loader.load_merged_data()
        X, y = predictor.prepare_data(df)
        metrics = predictor.fit(X, y)
        
        print("\n训练完成！评估指标:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")
        
        # 保存模型
        path = predictor.save_model()
        print(f"\n模型已保存到: {path}")
        
    elif model_type == "clustering":
        # 客户分群模型
        clustering = CustomerClustering()
        df = loader.load_merged_data()
        X = clustering.prepare_data(df)
        metrics = clustering.fit(X)
        
        print("\n训练完成！评估指标:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")
        
        # 保存模型
        path = clustering.save()
        print(f"\n模型已保存到: {path}")


def run_analysis(analysis_type: str = "association"):
    """运行数据分析"""
    from src.data import DataLoader
    from src.analysis import ProductAssociationAnalyzer, AssetTrendAnalyzer
    
    print(f"开始执行 {analysis_type} 分析...")
    
    loader = DataLoader()
    df = loader.load_merged_data()
    
    if analysis_type == "association":
        # 产品关联分析
        analyzer = ProductAssociationAnalyzer()
        itemsets, rules = analyzer.analyze(df)
        
        print("\n频繁产品组合:")
        print(itemsets[["products", "support"]].head(10).to_string())
        
        print("\n关联规则 Top 10:")
        print(analyzer.get_top_rules(10).to_string())
        
        # 保存结果
        paths = analyzer.save_results()
        print(f"\n结果已保存到: {paths}")
        
    elif analysis_type == "trend":
        # 资产趋势分析
        analyzer = AssetTrendAnalyzer()
        result = analyzer.analyze(df)
        
        print("\n趋势分析结果:")
        for k, v in result["trend"].items():
            print(f"  {k}: {v}")
        
        print("\n未来预测值:")
        print(result["forecast"])
        
        # 保存结果
        path = analyzer.save_results()
        print(f"\n结果已保存到: {path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="BankMind - 银行零售客户经营智能分析系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py assistant --mode gui      # 启动 AI 助手 Web 界面
  python main.py assistant --mode tui      # 启动 AI 助手终端模式
  python main.py dashboard                 # 启动可视化大屏
  python main.py train --model high_value  # 训练高价值预测模型
  python main.py train --model clustering  # 训练客户分群模型
  python main.py analyze --type association # 执行产品关联分析
  python main.py analyze --type trend       # 执行资产趋势分析
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # AI 助手命令
    assistant_parser = subparsers.add_parser("assistant", help="运行 AI 助手")
    assistant_parser.add_argument(
        "--mode", choices=["gui", "tui"], default="gui",
        help="运行模式: gui(Web界面) 或 tui(终端)"
    )
    assistant_parser.add_argument(
        "--port", type=int, default=7860,
        help="Web 界面端口号"
    )
    
    # 可视化大屏命令
    dashboard_parser = subparsers.add_parser("dashboard", help="运行可视化大屏")
    dashboard_parser.add_argument(
        "--host", default="0.0.0.0",
        help="服务主机地址"
    )
    dashboard_parser.add_argument(
        "--port", type=int, default=5001,
        help="服务端口号"
    )
    dashboard_parser.add_argument(
        "--no-debug", action="store_true",
        help="关闭调试模式"
    )
    
    # 模型训练命令
    train_parser = subparsers.add_parser("train", help="训练模型")
    train_parser.add_argument(
        "--model", choices=["high_value", "clustering"], default="high_value",
        help="模型类型"
    )
    
    # 数据分析命令
    analyze_parser = subparsers.add_parser("analyze", help="执行数据分析")
    analyze_parser.add_argument(
        "--type", choices=["association", "trend"], default="association",
        help="分析类型"
    )
    
    args = parser.parse_args()
    
    if args.command == "assistant":
        run_assistant(mode=args.mode, port=args.port)
    elif args.command == "dashboard":
        run_dashboard(host=args.host, port=args.port, debug=not args.no_debug)
    elif args.command == "train":
        run_training(model_type=args.model)
    elif args.command == "analyze":
        run_analysis(analysis_type=args.type)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

