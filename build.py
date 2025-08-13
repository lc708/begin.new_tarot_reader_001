#!/usr/bin/env python3
"""
Vercel构建脚本
确保所有Python依赖都能正确安装
"""

import subprocess
import sys
import os

def install_dependencies():
    """安装Python依赖"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Python依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ Python依赖安装失败: {e}")
        return False
    return True

def verify_imports():
    """验证关键模块导入"""
    try:
        import flask
        import flask_cors
        print("✅ Flask相关模块导入成功")
        
        # 验证自定义模块
        from utils import tarot_database, card_drawer, spread_config
        print("✅ 工具模块导入成功")
        
        from flow import run_tarot_reading
        print("✅ 流程模块导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

if __name__ == "__main__":
    print("🔧 开始Vercel构建准备...")
    
    if install_dependencies() and verify_imports():
        print("🎉 构建准备完成！")
        sys.exit(0)
    else:
        print("💥 构建准备失败！")
        sys.exit(1)
