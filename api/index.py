from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# 确保项目根目录在Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from flow import run_tarot_reading
from utils.reading_storage import get_reading_statistics, load_all_readings
from utils.spread_config import get_all_spreads, get_spread_config
from utils.tarot_database import get_all_cards, search_cards_by_keyword

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_cors_headers()
        
        if self.path == '/api/health':
            self.send_json_response({
                "status": "healthy",
                "message": "塔罗牌占卜API服务正常运行"
            })
        
        elif self.path == '/api/spreads':
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
            
            self.send_json_response({
                "success": True,
                "spreads": spread_details
            })
        
        elif self.path == '/api/cards':
            cards = get_all_cards()
            self.send_json_response({
                "success": True,
                "cards": cards,
                "total": len(cards)
            })
        
        elif self.path == '/api/history':
            all_readings = load_all_readings()
            self.send_json_response({
                "success": True,
                "readings": all_readings,
                "total": len(all_readings)
            })
        
        elif self.path == '/api/statistics':
            stats = get_reading_statistics()
            self.send_json_response({
                "success": True,
                "statistics": stats
            })
        
        else:
            self.send_error_response(404, "API endpoint not found")
    
    def do_POST(self):
        self.send_cors_headers()
        
        if self.path == '/api/reading':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                body = json.loads(post_data.decode('utf-8'))
                
                question = body['question']
                spread_type = body.get('spread_type')
                save_result = body.get('save_result', True)
                
                result = run_tarot_reading(
                    user_question=question,
                    spread_type=spread_type,
                    save_result=save_result
                )
                
                self.send_json_response(result)
                
            except Exception as e:
                self.send_error_response(500, f"Server error: {str(e)}")
        
        else:
            self.send_error_response(404, "API endpoint not found")
    
    def send_cors_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    
    def send_json_response(self, data):
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.wfile.write(json_data)
    
    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_data = {
            "success": False,
            "error": message
        }
        json_data = json.dumps(error_data, ensure_ascii=False).encode('utf-8')
        self.wfile.write(json_data)