# utils/spread_config.py
"""
牌阵配置工具函数
定义不同塔罗牌阵的配置信息和布局
"""

from typing import Dict, List, Optional

# 牌阵配置数据库
SPREAD_CONFIGS = {
    "single": {
        "name": "单张牌占卜",
        "description": "最简单的占卜方式，适合日常指导和是/否问题",
        "card_count": 1,
        "positions": {
            1: {
                "name": "指导",
                "description": "今日指导或对你问题的直接回答",
                "significance": "整体建议和方向"
            }
        },
        "usage": "适合快速获得指导，日常决策，简单问题",
        "difficulty": "初级"
    },
    
    "three_card": {
        "name": "三张牌占卜",
        "description": "经典的过去-现在-未来布局，适合了解事情发展脉络",
        "card_count": 3,
        "positions": {
            1: {
                "name": "过去",
                "description": "影响当前情况的过去因素或根源",
                "significance": "历史因素，根本原因，已经发生的影响"
            },
            2: {
                "name": "现在",
                "description": "当前的状况、挑战或机会",
                "significance": "目前的状态，需要面对的现实"
            },
            3: {
                "name": "未来",
                "description": "可能的结果或发展趋势",
                "significance": "潜在结果，发展方向，需要注意的趋势"
            }
        },
        "usage": "适合了解情况发展，分析问题全貌，中期规划",
        "difficulty": "初级"
    },
    
    "love_spread": {
        "name": "恋爱牌阵",
        "description": "专门用于感情问题的五张牌布局",
        "card_count": 5,
        "positions": {
            1: {
                "name": "你的感受",
                "description": "你在这段关系中的真实感受和内心状态",
                "significance": "内心情感，真实想法"
            },
            2: {
                "name": "对方的感受",
                "description": "对方对你和这段关系的感受",
                "significance": "对方的内心世界，他们的观点"
            },
            3: {
                "name": "关系现状",
                "description": "你们关系的当前状况和动态",
                "significance": "关系质量，相处模式"
            },
            4: {
                "name": "阻碍因素",
                "description": "阻碍关系发展的因素或需要克服的挑战",
                "significance": "问题所在，需要改善的方面"
            },
            5: {
                "name": "关系前景",
                "description": "这段关系的发展潜力和可能的未来",
                "significance": "发展趋势，长期前景"
            }
        },
        "usage": "专门用于感情咨询，了解关系动态，感情决策",
        "difficulty": "中级"
    },
    
    "career_spread": {
        "name": "事业牌阵",
        "description": "专门用于事业和工作问题的六张牌布局",
        "card_count": 6,
        "positions": {
            1: {
                "name": "当前状况",
                "description": "你目前的工作或事业状况",
                "significance": "现状分析"
            },
            2: {
                "name": "你的优势",
                "description": "在事业方面你拥有的优势和能力",
                "significance": "个人长处，可利用的资源"
            },
            3: {
                "name": "面临挑战",
                "description": "事业发展中需要面对的挑战或阻碍",
                "significance": "困难和障碍"
            },
            4: {
                "name": "外在机会",
                "description": "环境中存在的机会和有利因素",
                "significance": "外部机遇，可把握的机会"
            },
            5: {
                "name": "行动建议",
                "description": "为了事业发展应该采取的行动",
                "significance": "具体建议，行动方向"
            },
            6: {
                "name": "未来发展",
                "description": "事业的发展趋势和可能的结果",
                "significance": "长期前景，发展方向"
            }
        },
        "usage": "职业规划，工作决策，事业发展咨询",
        "difficulty": "中级"
    },
    
    "celtic_cross": {
        "name": "凯尔特十字牌阵",
        "description": "最经典和全面的牌阵，提供详细深入的分析",
        "card_count": 10,
        "positions": {
            1: {
                "name": "当前状况",
                "description": "你目前所处的状况和环境",
                "significance": "问题的核心，当前现实"
            },
            2: {
                "name": "挑战/阻碍",
                "description": "横亘在你面前的挑战或需要克服的阻碍",
                "significance": "主要困难，需要面对的挑战"
            },
            3: {
                "name": "遥远的过去",
                "description": "影响当前情况的深层根源或遥远的过去",
                "significance": "根本原因，深层背景"
            },
            4: {
                "name": "近期的过去",
                "description": "最近发生的影响当前状况的事件",
                "significance": "近期影响因素"
            },
            5: {
                "name": "可能的未来",
                "description": "如果按当前趋势发展可能出现的结果",
                "significance": "潜在结果，可能性"
            },
            6: {
                "name": "近期的未来",
                "description": "即将到来的影响或短期内的发展",
                "significance": "短期趋势，即将发生的事"
            },
            7: {
                "name": "你的方法",
                "description": "你处理这个问题的方式和态度",
                "significance": "个人方法，处理方式"
            },
            8: {
                "name": "外在影响",
                "description": "外部环境和他人对你的影响",
                "significance": "外部因素，他人观点"
            },
            9: {
                "name": "希望和恐惧",
                "description": "你内心深处的希望和恐惧",
                "significance": "内心期待和担忧"
            },
            10: {
                "name": "最终结果",
                "description": "整个情况的最终结果和结局",
                "significance": "最终结果，整体结论"
            }
        },
        "usage": "复杂问题分析，人生重大决策，全面深入了解",
        "difficulty": "高级"
    },
    
    "decision_spread": {
        "name": "决策牌阵",
        "description": "帮助在两个选择之间做决定的七张牌布局",
        "card_count": 7,
        "positions": {
            1: {
                "name": "当前状况",
                "description": "你面临决策时的当前状况",
                "significance": "决策背景"
            },
            2: {
                "name": "选择A的优势",
                "description": "第一个选择可能带来的好处",
                "significance": "选择A的正面影响"
            },
            3: {
                "name": "选择A的劣势",
                "description": "第一个选择可能带来的问题",
                "significance": "选择A的负面影响"
            },
            4: {
                "name": "选择B的优势",
                "description": "第二个选择可能带来的好处",
                "significance": "选择B的正面影响"
            },
            5: {
                "name": "选择B的劣势",
                "description": "第二个选择可能带来的问题",
                "significance": "选择B的负面影响"
            },
            6: {
                "name": "潜在结果",
                "description": "你的决策可能带来的长远影响",
                "significance": "长期后果"
            },
            7: {
                "name": "最佳行动",
                "description": "面对这个决策的最佳行动建议",
                "significance": "行动指导"
            }
        },
        "usage": "二选一决策，重要选择，优劣分析",
        "difficulty": "中级"
    }
}

def get_spread_config(spread_name: str) -> Dict:
    """
    获取指定牌阵的配置信息
    
    Args:
        spread_name: 牌阵名称
        
    Returns:
        牌阵配置信息字典
    """
    if spread_name not in SPREAD_CONFIGS:
        return {"error": f"未找到牌阵: {spread_name}"}
    
    return SPREAD_CONFIGS[spread_name].copy()

def get_all_spreads() -> List[str]:
    """获取所有可用的牌阵名称"""
    return list(SPREAD_CONFIGS.keys())

def get_spreads_by_difficulty(difficulty: str) -> List[str]:
    """根据难度级别获取牌阵列表"""
    return [
        name for name, config in SPREAD_CONFIGS.items() 
        if config["difficulty"] == difficulty
    ]

def get_position_meaning(spread_name: str, position: int) -> Dict:
    """
    获取特定牌阵中特定位置的含义
    
    Args:
        spread_name: 牌阵名称
        position: 位置编号
        
    Returns:
        位置含义信息
    """
    spread_config = get_spread_config(spread_name)
    if "error" in spread_config:
        return spread_config
    
    if position not in spread_config["positions"]:
        return {"error": f"位置 {position} 在牌阵 {spread_name} 中不存在"}
    
    return spread_config["positions"][position]

def recommend_spread_for_question(question: str, question_type: str = "general") -> Dict:
    """
    根据问题类型推荐合适的牌阵
    
    Args:
        question: 用户问题
        question_type: 问题类型 (love, career, decision, general)
        
    Returns:
        推荐的牌阵信息
    """
    recommendations = {
        "love": ["love_spread", "three_card"],
        "career": ["career_spread", "three_card", "celtic_cross"],
        "decision": ["decision_spread", "three_card"],
        "general": ["three_card", "single", "celtic_cross"],
        "complex": ["celtic_cross", "career_spread"],
        "simple": ["single", "three_card"]
    }
    
    # 根据问题长度和复杂度调整推荐
    if len(question) < 20:
        recommended_spreads = recommendations.get("simple", ["single"])
    elif question_type in recommendations:
        recommended_spreads = recommendations[question_type]
    else:
        recommended_spreads = recommendations["general"]
    
    # 返回第一个推荐的牌阵配置
    primary_recommendation = recommended_spreads[0]
    config = get_spread_config(primary_recommendation)
    
    return {
        "recommended_spread": primary_recommendation,
        "config": config,
        "alternatives": recommended_spreads[1:] if len(recommended_spreads) > 1 else [],
        "reason": f"基于问题类型 '{question_type}' 的推荐"
    }

def validate_spread_selection(spread_name: str, user_experience: str = "beginner") -> Dict:
    """
    验证用户选择的牌阵是否适合其经验水平
    
    Args:
        spread_name: 选择的牌阵名称
        user_experience: 用户经验水平 (beginner, intermediate, advanced)
        
    Returns:
        验证结果和建议
    """
    spread_config = get_spread_config(spread_name)
    if "error" in spread_config:
        return spread_config
    
    experience_mapping = {
        "beginner": ["初级"],
        "intermediate": ["初级", "中级"],
        "advanced": ["初级", "中级", "高级"]
    }
    
    suitable_difficulties = experience_mapping.get(user_experience, ["初级"])
    spread_difficulty = spread_config["difficulty"]
    
    is_suitable = spread_difficulty in suitable_difficulties
    
    result = {
        "spread_name": spread_name,
        "is_suitable": is_suitable,
        "spread_difficulty": spread_difficulty,
        "user_experience": user_experience
    }
    
    if not is_suitable:
        if user_experience == "beginner":
            result["suggestion"] = "建议初学者从单张牌或三张牌开始"
            result["recommended_alternatives"] = ["single", "three_card"]
        else:
            result["warning"] = f"这个牌阵难度为 {spread_difficulty}，可能对你的经验水平有些挑战"
    
    return result

if __name__ == "__main__":
    # 测试牌阵配置功能
    print("测试牌阵配置功能:")
    
    # 测试获取所有牌阵
    print("\n1. 所有可用牌阵:")
    all_spreads = get_all_spreads()
    for spread in all_spreads:
        config = get_spread_config(spread)
        print(f"- {config['name']} ({config['card_count']}张牌, {config['difficulty']})")
    
    # 测试获取具体牌阵配置
    print("\n2. 三张牌牌阵详细信息:")
    three_card_config = get_spread_config("three_card")
    print(f"名称: {three_card_config['name']}")
    print(f"描述: {three_card_config['description']}")
    print("位置含义:")
    for pos, info in three_card_config['positions'].items():
        print(f"  {pos}. {info['name']}: {info['description']}")
    
    # 测试问题推荐
    print("\n3. 根据问题类型推荐牌阵:")
    love_question = "我和男朋友的关系会有结果吗？"
    recommendation = recommend_spread_for_question(love_question, "love")
    print(f"问题: {love_question}")
    print(f"推荐牌阵: {recommendation['recommended_spread']}")
    print(f"推荐理由: {recommendation['reason']}")
    
    # 测试经验验证
    print("\n4. 验证牌阵选择:")
    validation = validate_spread_selection("celtic_cross", "beginner")
    print(f"新手选择凯尔特十字: {'适合' if validation['is_suitable'] else '不适合'}")
    if 'suggestion' in validation:
        print(f"建议: {validation['suggestion']}")
    
    # 测试按难度获取
    print("\n5. 按难度分类:")
    for difficulty in ["初级", "中级", "高级"]:
        spreads = get_spreads_by_difficulty(difficulty)
        print(f"{difficulty}: {spreads}")

