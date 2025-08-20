#!/usr/bin/env python3
"""
启动TokenData Web应用
"""
import subprocess
import sys
import os
import time

def check_dependencies():
    """检查依赖"""
    try:
        import dash
        import plotly
        print("✅ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def start_web_app():
    """启动Web应用"""
    print("🚀 启动TokenData Web应用...")
    print("=" * 50)
    
    if not check_dependencies():
        return
    
    try:
        # 启动Web应用
        subprocess.run([sys.executable, "web_app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Web应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    start_web_app()
