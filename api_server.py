# api_server.py
"""
塔罗牌占卜应用API服务器
为前端提供RESTful API接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from flow import run_tarot_reading
from utils.reading_storage import get_reading_statistics, load_all_readings
from utils.spread_config import get_all_spreads, get_spread_config
from utils.tarot_database import get_all_cards, search_cards_by_keyword

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "message": "塔罗牌占卜API服务正常运行"
    })

@app.route('/api/reading', methods=['POST'])
def create_reading():
    """创建新的塔罗牌占卜"""
    try:
        data = request.get_json()
        
        # 验证必需参数
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必需的参数：question"
            }), 400
        
        question = data['question']
        spread_type = data.get('spread_type')
        save_result = data.get('save_result', True)
        
        print(f"🔮 收到占卜请求: question='{question}', spread_type='{spread_type}'")
        
        # 调用后端占卜流程
        result = run_tarot_reading(
            user_question=question,
            spread_type=spread_type,
            save_result=save_result
        )
        
        print(f"✅ 占卜流程完成: success={result.get('success', False)}, keys={list(result.keys())}")
        
        # 如果后端失败但返回了结构化错误，检查是否是LLM相关错误
        if not result.get('success', False) and 'API_KEY' in str(result.get('error', '')):
            # 提供fallback响应
            from utils.card_drawer import draw_cards
            from utils.spread_config import get_spread_config
            
            # 获取基本牌阵信息
            spread_config = get_spread_config(spread_type or 'single')
            card_count = spread_config.get('card_count', 1)
            
            # 抽取卡牌
            cards = draw_cards(card_count)
            
            # 创建简化的占卜结果
            fallback_result = {
                "success": True,
                "question": question,
                "question_category": "general",
                "spread_type": spread_type or 'single',
                "spread_name": spread_config.get('name', '单张牌占卜'),
                "drawn_cards": cards,
                "individual_readings": [],
                "combined_reading": f"🔮 由于AI占卜师暂时无法连接，为您提供了基础的塔罗指引。您抽到了{len(cards)}张牌，每张牌都承载着古老的智慧。请静心感受这些牌带给您的直觉启发，相信内心的声音会为您指明方向。",
                "reading_summary": "相信直觉，静心感受牌的指引。",
                "timestamp": datetime.now().isoformat(),
                "fallback_mode": True  # 标识这是fallback模式
            }
            return jsonify(fallback_result)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"占卜过程中发生错误: {str(e)}"
        }), 500

@app.route('/api/spreads', methods=['GET'])
def get_spreads():
    """获取所有可用的牌阵"""
    try:
        spreads = get_all_spreads()
        spread_details = []
        
        for spread_name in spreads:
            config = get_spread_config(spread_name)
            if 'error' not in config:
                spread_details.append({
                    "id": spread_name,
                    "name": config['name'],
                    "description": config['description'],
                    "card_count": config['card_count'],
                    "difficulty": config['difficulty'],
                    "usage": config['usage']
                })
        
        return jsonify({
            "success": True,
            "spreads": spread_details
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取牌阵信息失败: {str(e)}"
        }), 500

@app.route('/api/spreads/<spread_id>', methods=['GET'])
def get_spread_detail(spread_id):
    """获取特定牌阵的详细信息"""
    try:
        config = get_spread_config(spread_id)
        
        if 'error' in config:
            return jsonify({
                "success": False,
                "error": config['error']
            }), 404
        
        return jsonify({
            "success": True,
            "spread": config
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取牌阵详情失败: {str(e)}"
        }), 500

@app.route('/api/cards', methods=['GET'])
def get_cards():
    """获取所有塔罗牌信息"""
    try:
        cards = get_all_cards()
        
        # 可选的搜索功能
        search_term = request.args.get('search')
        if search_term:
            cards = search_cards_by_keyword(search_term)
        
        return jsonify({
            "success": True,
            "cards": cards,
            "total": len(cards)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取塔罗牌信息失败: {str(e)}"
        }), 500

@app.route('/api/history', methods=['GET'])
def get_reading_history():
    """获取占卜历史记录"""
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        all_readings = load_all_readings()
        
        # 分页处理
        total = len(all_readings)
        readings = all_readings[offset:offset + limit]
        
        return jsonify({
            "success": True,
            "readings": readings,
            "total": total,
            "limit": limit,
            "offset": offset
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取历史记录失败: {str(e)}"
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取占卜统计信息"""
    try:
        stats = get_reading_statistics()
        
        return jsonify({
            "success": True,
            "statistics": stats
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取统计信息失败: {str(e)}"
        }), 500

@app.route('/api/recommend-spread', methods=['POST'])
def recommend_spread():
    """根据问题推荐合适的牌阵"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必需的参数：question"
            }), 400
        
        question = data['question']
        
        # 简单的推荐逻辑
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['爱情', '感情', '恋爱', '婚姻', '伴侣']):
            recommended = "love_spread"
        elif any(word in question_lower for word in ['工作', '事业', '职业', '职场', '升职']):
            recommended = "career_spread"
        elif any(word in question_lower for word in ['选择', '决定', '应该', '还是']):
            recommended = "decision_spread"
        elif len(question) > 30:
            recommended = "celtic_cross"
        elif len(question) < 10:
            recommended = "single"
        else:
            recommended = "three_card"
        
        config = get_spread_config(recommended)
        
        return jsonify({
            "success": True,
            "recommended_spread": recommended,
            "spread_info": config,
            "reason": f"根据您的问题类型和复杂度，推荐使用{config['name']}"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"推荐牌阵失败: {str(e)}"
        }), 500

# For Vercel deployment
import os
if os.environ.get('VERCEL'):
    # Vercel serverless function handler
    app.wsgi_app = app

if __name__ == '__main__':
    print("🔮 启动塔罗牌占卜API服务器...")
    print("📡 API地址: http://localhost:8011")
    print("🌐 支持的接口:")
    print("   GET  /api/health - 健康检查")
    print("   POST /api/reading - 创建占卜")
    print("   GET  /api/spreads - 获取牌阵列表")
    print("   GET  /api/cards - 获取塔罗牌信息")
    print("   GET  /api/history - 获取占卜历史")
    print("   GET  /api/statistics - 获取统计信息")
    print("   POST /api/recommend-spread - 推荐牌阵")
    
    app.run(
        host='0.0.0.0',
        port=8011,
        debug=True
    )
