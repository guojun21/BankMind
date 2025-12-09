"""
产品关联分析模块
使用 Apriori 算法挖掘产品组合模式
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple
from mlxtend.frequent_patterns import apriori, association_rules

from ..config import settings
from ..data import FeatureEngineer


class ProductAssociationAnalyzer:
    """产品关联分析器"""
    
    PRODUCT_COLUMNS = [
        "deposit_flag", "financial_flag",
        "fund_flag", "insurance_flag"
    ]
    
    PRODUCT_NAMES = {
        "deposit_flag": "存款",
        "financial_flag": "理财",
        "fund_flag": "基金",
        "insurance_flag": "保险",
    }
    
    def __init__(
        self,
        min_support: float = None,
        min_lift: float = None
    ):
        self.min_support = min_support or settings.APRIORI_MIN_SUPPORT
        self.min_lift = min_lift or settings.APRIORI_MIN_LIFT
        self.feature_engineer = FeatureEngineer()
        self.frequent_itemsets: Optional[pd.DataFrame] = None
        self.rules: Optional[pd.DataFrame] = None
    
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        准备关联分析数据
        
        Args:
            df: 原始数据
        
        Returns:
            产品持有矩阵（0/1）
        """
        # 创建产品标志
        df = self.feature_engineer.create_product_flags(df)
        
        # 选择产品列
        available_cols = [col for col in self.PRODUCT_COLUMNS if col in df.columns]
        
        # 创建购物篮矩阵
        basket = df[available_cols].fillna(0).astype(int)
        basket = basket.drop_duplicates()
        
        return basket
    
    def find_frequent_itemsets(
        self,
        basket: pd.DataFrame,
        min_support: float = None
    ) -> pd.DataFrame:
        """
        挖掘频繁项集
        
        Args:
            basket: 产品持有矩阵
            min_support: 最小支持度
        
        Returns:
            频繁项集 DataFrame
        """
        min_support = min_support or self.min_support
        
        self.frequent_itemsets = apriori(
            basket,
            min_support=min_support,
            use_colnames=True
        )
        
        # 添加可读的产品名称
        self.frequent_itemsets["products"] = self.frequent_itemsets["itemsets"].apply(
            lambda x: ", ".join([self.PRODUCT_NAMES.get(item, item) for item in x])
        )
        
        return self.frequent_itemsets.sort_values("support", ascending=False)
    
    def generate_rules(
        self,
        frequent_itemsets: pd.DataFrame = None,
        metric: str = "lift",
        min_threshold: float = None
    ) -> pd.DataFrame:
        """
        生成关联规则
        
        Args:
            frequent_itemsets: 频繁项集，默认使用已计算的
            metric: 评估指标 ('lift', 'confidence', 'support')
            min_threshold: 最小阈值
        
        Returns:
            关联规则 DataFrame
        """
        if frequent_itemsets is None:
            if self.frequent_itemsets is None:
                raise ValueError("请先调用 find_frequent_itemsets()")
            frequent_itemsets = self.frequent_itemsets
        
        min_threshold = min_threshold or self.min_lift
        
        self.rules = association_rules(
            frequent_itemsets,
            metric=metric,
            min_threshold=min_threshold
        )
        
        # 添加可读的规则描述
        self.rules["rule"] = self.rules.apply(
            lambda row: f"{self._format_itemset(row['antecedents'])} → {self._format_itemset(row['consequents'])}",
            axis=1
        )
        
        return self.rules.sort_values("lift", ascending=False)
    
    def _format_itemset(self, itemset) -> str:
        """格式化项集为可读字符串"""
        return " + ".join([self.PRODUCT_NAMES.get(item, item) for item in itemset])
    
    def analyze(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        执行完整的关联分析
        
        Args:
            df: 原始数据
        
        Returns:
            (频繁项集, 关联规则)
        """
        basket = self.prepare_data(df)
        frequent_itemsets = self.find_frequent_itemsets(basket)
        rules = self.generate_rules(frequent_itemsets)
        
        return frequent_itemsets, rules
    
    def get_top_rules(self, n: int = 10, by: str = "lift") -> pd.DataFrame:
        """
        获取 Top N 关联规则
        
        Args:
            n: 返回数量
            by: 排序字段
        
        Returns:
            Top N 规则
        """
        if self.rules is None:
            raise ValueError("请先调用 analyze() 或 generate_rules()")
        
        return self.rules.nlargest(n, by)[
            ["rule", "support", "confidence", "lift"]
        ]
    
    def get_product_recommendations(
        self,
        current_products: List[str]
    ) -> List[Dict]:
        """
        根据当前持有产品推荐其他产品
        
        Args:
            current_products: 当前持有的产品标志列表
        
        Returns:
            推荐产品列表
        """
        if self.rules is None:
            raise ValueError("请先调用 analyze()")
        
        recommendations = []
        
        for _, rule in self.rules.iterrows():
            antecedents = set(rule["antecedents"])
            consequents = set(rule["consequents"])
            
            # 如果当前产品包含前件，且不包含后件
            if antecedents.issubset(set(current_products)):
                new_products = consequents - set(current_products)
                if new_products:
                    for product in new_products:
                        recommendations.append({
                            "product": self.PRODUCT_NAMES.get(product, product),
                            "confidence": rule["confidence"],
                            "lift": rule["lift"],
                            "reason": f"因为您持有 {self._format_itemset(antecedents)}"
                        })
        
        # 按置信度排序并去重
        seen = set()
        unique_recs = []
        for rec in sorted(recommendations, key=lambda x: -x["confidence"]):
            if rec["product"] not in seen:
                seen.add(rec["product"])
                unique_recs.append(rec)
        
        return unique_recs
    
    def save_results(
        self,
        output_dir: str = None,
        prefix: str = ""
    ) -> Tuple[str, str]:
        """
        保存分析结果
        
        Args:
            output_dir: 输出目录
            prefix: 文件名前缀
        
        Returns:
            (频繁项集文件路径, 规则文件路径)
        """
        from pathlib import Path
        
        output_dir = Path(output_dir) if output_dir else settings.OUTPUT_DIR / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        itemsets_path = output_dir / f"{prefix}frequent_itemsets.csv"
        rules_path = output_dir / f"{prefix}association_rules.csv"
        
        if self.frequent_itemsets is not None:
            self.frequent_itemsets.to_csv(itemsets_path, index=False, encoding="utf-8-sig")
        
        if self.rules is not None:
            self.rules.to_csv(rules_path, index=False, encoding="utf-8-sig")
        
        return str(itemsets_path), str(rules_path)

