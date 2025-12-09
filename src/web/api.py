"""
Web API 路由
提供 RESTful API 接口
"""

from flask import Blueprint, jsonify, request

from ..visualization import DashboardGenerator

api_bp = Blueprint("api", __name__, url_prefix="/api")

# 全局 Dashboard 生成器
_dashboard: DashboardGenerator = None


def get_dashboard() -> DashboardGenerator:
    """获取 Dashboard 生成器实例"""
    global _dashboard
    if _dashboard is None:
        _dashboard = DashboardGenerator()
    return _dashboard


@api_bp.route("/indicators")
def api_indicators():
    """核心指标卡片数据接口"""
    try:
        data = get_dashboard().get_key_indicators()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/lifecycle")
def api_lifecycle():
    """客户生命周期分布接口"""
    try:
        data = get_dashboard().get_customer_lifecycle()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/asset_level")
def api_asset_level():
    """资产等级分布接口"""
    try:
        data = get_dashboard().get_asset_level_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/product_holdings")
def api_product_holdings():
    """产品持有情况接口"""
    try:
        data = get_dashboard().get_product_holdings()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/app_active_trend")
def api_app_active_trend():
    """APP 活跃度趋势接口"""
    try:
        data = get_dashboard().get_app_activity_trend()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/risk")
def api_risk():
    """风险分布接口"""
    try:
        data = get_dashboard().get_risk_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/age_distribution")
def api_age_distribution():
    """年龄分布接口"""
    try:
        data = get_dashboard().get_age_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/occupation")
def api_occupation():
    """职业分布接口"""
    try:
        data = get_dashboard().get_occupation_distribution()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/dashboard")
def api_dashboard():
    """获取所有 Dashboard 数据"""
    try:
        data = get_dashboard().get_all_dashboard_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/reload", methods=["POST"])
def api_reload():
    """重新加载数据"""
    try:
        get_dashboard().reload_data()
        return jsonify({"status": "success", "message": "数据已重新加载"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

