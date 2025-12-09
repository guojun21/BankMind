"""
Flask Web 应用
"""

from flask import Flask, render_template
from pathlib import Path

from .api import api_bp


def create_app(config: dict = None) -> Flask:
    """
    创建 Flask 应用
    
    Args:
        config: 应用配置
    
    Returns:
        Flask 应用实例
    """
    # 确定模板和静态文件目录
    base_dir = Path(__file__).parent
    template_dir = base_dir / "templates"
    static_dir = base_dir / "static"
    
    # 创建目录（如果不存在）
    template_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    
    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir),
    )
    
    # 应用配置
    app.config["JSON_AS_ASCII"] = False  # 支持中文 JSON
    if config:
        app.config.update(config)
    
    # 注册蓝图
    app.register_blueprint(api_bp)
    
    # 注册路由
    @app.route("/")
    def index():
        """主页"""
        return render_template("dashboard.html")
    
    @app.route("/health")
    def health():
        """健康检查"""
        return {"status": "healthy"}
    
    return app


def run_server(host: str = "0.0.0.0", port: int = 5001, debug: bool = True):
    """
    运行 Web 服务器
    
    Args:
        host: 主机地址
        port: 端口号
        debug: 是否开启调试模式
    """
    app = create_app()
    
    print("=" * 50)
    print("BankMind Dashboard 服务")
    print(f"访问地址: http://localhost:{port}")
    print("=" * 50)
    
    app.run(host=host, port=port, debug=debug)

