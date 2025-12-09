"""
AI 助手主模块
基于 Qwen Agent 框架的银行客户智能助手
"""

import os
import dashscope
from typing import List, Optional

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

from ..config import settings
from .prompts import SYSTEM_PROMPT, SUGGESTED_QUESTIONS
from .tools import SQLQueryTool  # 确保工具被注册


class BankCustomerAssistant:
    """银行客户智能助手"""
    
    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        timeout: int = None
    ):
        """
        初始化助手
        
        Args:
            model: 模型名称
            api_key: DashScope API Key
            timeout: 请求超时时间
        """
        self.model = model or settings.LLM_MODEL
        self.api_key = api_key or settings.DASHSCOPE_API_KEY
        self.timeout = timeout or settings.DASHSCOPE_TIMEOUT
        
        # 配置 DashScope
        dashscope.api_key = self.api_key
        dashscope.timeout = self.timeout
        
        self._bot: Optional[Assistant] = None
    
    @property
    def bot(self) -> Assistant:
        """懒加载 Assistant"""
        if self._bot is None:
            self._bot = self._create_assistant()
        return self._bot
    
    def _create_assistant(self) -> Assistant:
        """创建 Assistant 实例"""
        llm_cfg = {
            "model": self.model,
            "timeout": self.timeout,
            "retry_count": settings.LLM_RETRY_COUNT,
        }
        
        try:
            bot = Assistant(
                llm=llm_cfg,
                name="百万客群经营助手",
                description="银行客户数据查询与分析",
                system_message=SYSTEM_PROMPT,
                function_list=["exc_sql"],
            )
            print("✅ 助手初始化成功！")
            return bot
        except Exception as e:
            print(f"❌ 助手初始化失败: {str(e)}")
            raise
    
    def chat(self, query: str, history: List = None) -> str:
        """
        单轮对话
        
        Args:
            query: 用户问题
            history: 对话历史
        
        Returns:
            助手回复
        """
        messages = history or []
        messages.append({"role": "user", "content": query})
        
        response = []
        for resp in self.bot.run(messages):
            response = resp
        
        if response:
            return response[-1].get("content", "")
        return ""
    
    def run_tui(self) -> None:
        """
        运行终端交互模式
        """
        print("=" * 50)
        print("百万客群经营助手 - 终端模式")
        print("输入 'quit' 或 'exit' 退出")
        print("=" * 50)
        
        messages = []
        
        while True:
            try:
                query = input("\n👤 用户: ").strip()
                
                if query.lower() in ["quit", "exit", "q"]:
                    print("👋 再见！")
                    break
                
                if not query:
                    print("⚠️  请输入问题")
                    continue
                
                messages.append({"role": "user", "content": query})
                
                print("\n🤖 助手: ", end="", flush=True)
                
                response = []
                for resp in self.bot.run(messages):
                    response = resp
                
                if response:
                    assistant_msg = response[-1].get("content", "")
                    print(assistant_msg)
                    messages.extend(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}")
                print("请重试...")
    
    def run_gui(self, port: int = 7860) -> None:
        """
        运行 Web 图形界面
        
        Args:
            port: 服务端口
        """
        print("=" * 50)
        print("百万客群经营助手 - Web 界面")
        print(f"访问地址: http://localhost:{port}")
        print("=" * 50)
        
        chatbot_config = {
            "prompt.suggestions": SUGGESTED_QUESTIONS
        }
        
        try:
            WebUI(
                self.bot,
                chatbot_config=chatbot_config,
            ).run(server_port=port)
        except Exception as e:
            print(f"❌ Web 界面启动失败: {str(e)}")
            print("请检查网络连接和 API Key 配置")
    
    @classmethod
    def quick_start(cls, mode: str = "gui") -> None:
        """
        快速启动助手
        
        Args:
            mode: 运行模式 ('gui' 或 'tui')
        """
        assistant = cls()
        
        if mode == "tui":
            assistant.run_tui()
        else:
            assistant.run_gui()

