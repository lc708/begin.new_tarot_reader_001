# index.py - Vercel Python Function Entry Point
"""
Vercel部署的Python函数入口点
将Flask应用适配为Vercel Functions
"""

import sys
import os

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入Flask应用
from api_server import app

# Vercel Function handler
def handler(request, context):
    return app(request, context)

# 导出应用供Vercel使用
application = app

if __name__ == "__main__":
    # 本地开发时运行
    app.run(debug=True)
