# utils/reading_storage.py
"""
占卜记录存储工具函数
保存和检索用户的占卜历史记录
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import uuid

# 存储文件路径
STORAGE_DIR = "data"
READINGS_FILE = os.path.join(STORAGE_DIR, "tarot_readings.json")

def ensure_storage_directory():
    """确保存储目录存在"""
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

def generate_reading_id() -> str:
    """生成唯一的占卜记录ID"""
    return str(uuid.uuid4())

def save_reading(reading_data: Dict) -> bool:
    """
    保存占卜记录
    
    Args:
        reading_data: 占卜数据字典
        
    Returns:
        保存是否成功
    """
    try:
        ensure_storage_directory()
        
        # 添加元数据
        reading_data["id"] = generate_reading_id()
        reading_data["timestamp"] = datetime.now().isoformat()
        reading_data["version"] = "1.0"
        
        # 加载现有记录
        existing_readings = load_all_readings()
        
        # 添加新记录
        existing_readings.append(reading_data)
        
        # 保存到文件
        with open(READINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_readings, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        print(f"保存占卜记录失败: {str(e)}")
        return False

def load_all_readings() -> List[Dict]:
    """
    加载所有占卜记录
    
    Returns:
        所有占卜记录的列表
    """
    try:
        if not os.path.exists(READINGS_FILE):
            return []
        
        with open(READINGS_FILE, 'r', encoding='utf-8') as f:
            readings = json.load(f)
            
        # 按时间倒序排列（最新的在前）
        readings.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return readings
        
    except Exception as e:
        print(f"加载占卜记录失败: {str(e)}")
        return []

def get_reading_by_id(reading_id: str) -> Optional[Dict]:
    """
    根据ID获取特定的占卜记录
    
    Args:
        reading_id: 占卜记录ID
        
    Returns:
        占卜记录字典或None
    """
    readings = load_all_readings()
    for reading in readings:
        if reading.get('id') == reading_id:
            return reading
    return None

def get_readings_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    获取指定日期范围内的占卜记录
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD 格式)
        end_date: 结束日期 (YYYY-MM-DD 格式)
        
    Returns:
        日期范围内的占卜记录列表
    """
    readings = load_all_readings()
    filtered_readings = []
    
    for reading in readings:
        reading_date = reading.get('timestamp', '')[:10]  # 取日期部分
        if start_date <= reading_date <= end_date:
            filtered_readings.append(reading)
    
    return filtered_readings

def get_readings_by_question_type(question_type: str) -> List[Dict]:
    """
    根据问题类型筛选占卜记录
    
    Args:
        question_type: 问题类型 (love, career, health, general)
        
    Returns:
        指定类型的占卜记录列表
    """
    readings = load_all_readings()
    return [r for r in readings if r.get('question_category') == question_type]

def get_readings_by_spread(spread_type: str) -> List[Dict]:
    """
    根据牌阵类型筛选占卜记录
    
    Args:
        spread_type: 牌阵类型
        
    Returns:
        指定牌阵的占卜记录列表
    """
    readings = load_all_readings()
    return [r for r in readings if r.get('spread_type') == spread_type]

def delete_reading(reading_id: str) -> bool:
    """
    删除指定的占卜记录
    
    Args:
        reading_id: 要删除的记录ID
        
    Returns:
        删除是否成功
    """
    try:
        readings = load_all_readings()
        original_count = len(readings)
        
        # 过滤掉要删除的记录
        readings = [r for r in readings if r.get('id') != reading_id]
        
        if len(readings) == original_count:
            # 没有找到要删除的记录
            return False
        
        # 保存更新后的记录
        with open(READINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(readings, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        print(f"删除占卜记录失败: {str(e)}")
        return False

def get_reading_statistics() -> Dict:
    """
    获取占卜记录统计信息
    
    Returns:
        统计信息字典
    """
    readings = load_all_readings()
    
    if not readings:
        return {
            "total_readings": 0,
            "question_types": {},
            "spread_types": {},
            "most_recent": None,
            "oldest": None
        }
    
    # 统计问题类型
    question_types = {}
    spread_types = {}
    
    for reading in readings:
        # 问题类型统计
        q_type = reading.get('question_category', 'unknown')
        question_types[q_type] = question_types.get(q_type, 0) + 1
        
        # 牌阵类型统计
        s_type = reading.get('spread_type', 'unknown')
        spread_types[s_type] = spread_types.get(s_type, 0) + 1
    
    return {
        "total_readings": len(readings),
        "question_types": question_types,
        "spread_types": spread_types,
        "most_recent": readings[0].get('timestamp') if readings else None,
        "oldest": readings[-1].get('timestamp') if readings else None,
        "average_per_month": len(readings) / max(1, len(set(r.get('timestamp', '')[:7] for r in readings)))
    }

def export_readings_to_json(output_file: str = None) -> str:
    """
    导出所有占卜记录到JSON文件
    
    Args:
        output_file: 输出文件路径（可选）
        
    Returns:
        导出文件的路径
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"tarot_export_{timestamp}.json"
    
    readings = load_all_readings()
    
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_readings": len(readings),
        "readings": readings
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return output_file
        
    except Exception as e:
        print(f"导出失败: {str(e)}")
        return ""

def create_sample_reading() -> Dict:
    """
    创建示例占卜记录（用于测试）
    
    Returns:
        示例占卜记录
    """
    return {
        "user_question": "我今天的运势如何？",
        "question_category": "general",
        "spread_type": "single",
        "spread_config": {
            "name": "单张牌占卜",
            "card_count": 1
        },
        "drawn_cards": [
            {
                "name": "太阳",
                "reversed": False,
                "position": 1,
                "orientation": "upright"
            }
        ],
        "individual_readings": [
            "太阳牌在正位出现，预示着今天将是充满正能量和成功的一天。你会感到自信满满，各种事情都会顺利进行。"
        ],
        "combined_reading": "太阳牌的出现是一个非常积极的信号。今天你将体验到生活的美好，工作和人际关系都会带来愉快的惊喜。保持乐观的心态，好运将会伴随你。",
        "reading_summary": "今日运势极佳，充满正能量和成功机会。"
    }

if __name__ == "__main__":
    # 测试存储功能
    print("测试占卜记录存储功能:")
    
    # 创建并保存示例记录
    print("\n1. 保存示例占卜记录:")
    sample_reading = create_sample_reading()
    success = save_reading(sample_reading)
    print(f"保存{'成功' if success else '失败'}")
    
    # 加载所有记录
    print("\n2. 加载所有记录:")
    all_readings = load_all_readings()
    print(f"总共有 {len(all_readings)} 条记录")
    
    if all_readings:
        latest = all_readings[0]
        print(f"最新记录: {latest['user_question']} ({latest['timestamp'][:19]})")
    
    # 获取统计信息
    print("\n3. 统计信息:")
    stats = get_reading_statistics()
    print(f"总记录数: {stats['total_readings']}")
    print(f"问题类型分布: {stats['question_types']}")
    print(f"牌阵类型分布: {stats['spread_types']}")
    
    # 测试筛选功能
    print("\n4. 按类型筛选:")
    general_readings = get_readings_by_question_type("general")
    print(f"一般性问题记录: {len(general_readings)} 条")
    
    single_spread_readings = get_readings_by_spread("single")
    print(f"单张牌占卜记录: {len(single_spread_readings)} 条")
    
    # 测试导出功能
    print("\n5. 导出测试:")
    export_file = export_readings_to_json()
    if export_file:
        print(f"导出成功，文件: {export_file}")
        # 清理测试文件
        if os.path.exists(export_file):
            os.remove(export_file)
            print("测试文件已清理")

