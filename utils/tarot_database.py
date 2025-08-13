# utils/tarot_database.py
"""
塔罗牌数据库工具函数
提供完整的78张塔罗牌信息检索功能
"""

# 完整的78张塔罗牌数据库
TAROT_CARDS = {
    # 大阿卡纳 (Major Arcana) - 22张
    "愚者": {
        "number": 0,
        "suit": "major_arcana",
        "keywords": ["新开始", "纯真", "自发性", "冒险"],
        "upright": {
            "meaning": "新的开始，无限可能，纯真的心境，自由精神",
            "love": "新的恋情开始，充满可能性的关系",
            "career": "新的工作机会，创新的想法，勇于尝试",
            "health": "身心重新开始，摆脱旧的习惯"
        },
        "reversed": {
            "meaning": "鲁莽行为，缺乏计划，轻率决定，错失机会",
            "love": "不成熟的感情，缺乏责任感",
            "career": "缺乏经验，不切实际的想法",
            "health": "缺乏自律，不注意健康"
        }
    },
    "魔术师": {
        "number": 1,
        "suit": "major_arcana", 
        "keywords": ["力量", "技能", "专注", "行动"],
        "upright": {
            "meaning": "具备实现目标的所有工具和能力，专注力强",
            "love": "有能力创造理想的关系，主动追求",
            "career": "具备成功所需的技能，领导能力",
            "health": "恢复活力，身心平衡"
        },
        "reversed": {
            "meaning": "缺乏自信，滥用才能，操控他人，散乱的能量",
            "love": "操控欲强，不诚实的关系",
            "career": "才能被滥用，缺乏方向",
            "health": "能量失衡，压力过大"
        }
    },
    "女祭司": {
        "number": 2,
        "suit": "major_arcana",
        "keywords": ["直觉", "神秘", "智慧", "内在声音"],
        "upright": {
            "meaning": "倾听内在智慧，信任直觉，神秘的知识",
            "love": "精神层面的连接，深层的理解",
            "career": "需要运用直觉，研究型工作",
            "health": "关注身体的信号，内在平衡"
        },
        "reversed": {
            "meaning": "忽视直觉，缺乏内省，表面化，秘密暴露",
            "love": "缺乏深度，表面的关系",
            "career": "忽视内在声音，决策失误",
            "health": "忽视身体警告，内分泌失调"
        }
    },
    "皇后": {
        "number": 3,
        "suit": "major_arcana",
        "keywords": ["丰盛", "创造力", "母性", "自然"],
        "upright": {
            "meaning": "创造力丰富，丰盛富足，母性关怀，与自然和谐",
            "love": "充满爱的关系，可能怀孕生子",
            "career": "创意工作，团队和谐，丰收成果",
            "health": "生育力强，身体健康丰盛"
        },
        "reversed": {
            "meaning": "缺乏创造力，过度保护，依赖他人，不育",
            "love": "过分依赖，窒息的关爱",
            "career": "创意阻塞，缺乏成果",
            "health": "生育问题，缺乏活力"
        }
    },
    "皇帝": {
        "number": 4,
        "suit": "major_arcana",
        "keywords": ["权威", "结构", "控制", "父性"],
        "upright": {
            "meaning": "权威领导，建立秩序，稳定结构，父权保护",
            "love": "稳定的关系，承诺和责任",
            "career": "领导地位，权威认可，结构化成功",
            "health": "规律的生活，系统性康复"
        },
        "reversed": {
            "meaning": "滥用权力，过度控制，独裁专制，缺乏纪律",
            "love": "控制欲强，缺乏温情",
            "career": "权力斗争，缺乏领导力",
            "health": "压力过大，缺乏自律"
        }
    },
    "教皇": {
        "number": 5,
        "suit": "major_arcana",
        "keywords": ["传统", "教育", "精神指导", "道德"],
        "upright": {
            "meaning": "遵循传统，寻求精神指导，道德准则，传统教育",
            "love": "传统的关系价值，道德的考量",
            "career": "教育行业，传统机构，道德准则",
            "health": "传统疗法，精神健康"
        },
        "reversed": {
            "meaning": "反叛传统，质疑权威，非传统思维，道德混乱",
            "love": "非传统关系，挑战道德",
            "career": "质疑制度，创新思维",
            "health": "另类疗法，反叛旧习"
        }
    },
    "恋人": {
        "number": 6,
        "suit": "major_arcana",
        "keywords": ["爱情", "选择", "和谐", "结合"],
        "upright": {
            "meaning": "真挚的爱情，重要的选择，和谐关系，灵魂伴侣",
            "love": "深刻的感情连接，重要的感情决定",
            "career": "合作伙伴，重要选择，价值观统一",
            "health": "身心和谐，伴侣支持"
        },
        "reversed": {
            "meaning": "关系失衡，错误选择，价值观冲突，分离",
            "love": "感情危机，价值观不合",
            "career": "合作破裂，选择困难",
            "health": "身心不协调，缺乏支持"
        }
    },
    "战车": {
        "number": 7,
        "suit": "major_arcana",
        "keywords": ["意志力", "决心", "控制", "胜利"],
        "upright": {
            "meaning": "强大的意志力，控制局面，决心取得胜利，克服障碍",
            "love": "为感情努力，克服困难",
            "career": "意志坚定，克服挑战，获得成功",
            "health": "意志力强，战胜疾病"
        },
        "reversed": {
            "meaning": "缺乏控制，方向不明，意志薄弱，失败",
            "love": "缺乏方向，感情摇摆",
            "career": "缺乏决心，目标不明",
            "health": "意志薄弱，缺乏毅力"
        }
    },
    "力量": {
        "number": 8,
        "suit": "major_arcana",
        "keywords": ["内在力量", "勇气", "耐心", "温柔"],
        "upright": {
            "meaning": "内在力量，温柔的勇气，耐心克服困难，驯服内心野兽",
            "love": "温柔的力量，包容理解",
            "career": "内在实力，温和领导",
            "health": "内在康复力，耐心治疗"
        },
        "reversed": {
            "meaning": "缺乏自信，内在恐惧，暴力倾向，失去控制",
            "love": "缺乏安全感，情绪失控",
            "career": "缺乏自信，暴躁易怒",
            "health": "精神压力，缺乏耐心"
        }
    },
    "隐士": {
        "number": 9,
        "suit": "major_arcana",
        "keywords": ["内省", "寻找", "智慧", "引导"],
        "upright": {
            "meaning": "内在寻找，精神指导，智慧获得，独处思考",
            "love": "需要独处思考，寻找真爱",
            "career": "寻找人生方向，深度思考",
            "health": "内在康复，精神调养"
        },
        "reversed": {
            "meaning": "孤立无援，拒绝帮助，内在迷失，顽固不化",
            "love": "过度孤立，拒绝感情",
            "career": "闭门造车，拒绝建议",
            "health": "缺乏指导，盲目治疗"
        }
    },
    "命运之轮": {
        "number": 10,
        "suit": "major_arcana",
        "keywords": ["命运", "变化", "循环", "机会"],
        "upright": {
            "meaning": "命运转机，好运降临，生命循环，把握机会",
            "love": "感情转机，命运安排",
            "career": "事业转机，机会来临",
            "health": "健康好转，转机出现"
        },
        "reversed": {
            "meaning": "坏运气，失去控制，错失机会，停滞不前",
            "love": "感情低潮，错失良缘",
            "career": "事业阻滞，失去机会",
            "health": "健康下滑，治疗停滞"
        }
    },
    "正义": {
        "number": 11,
        "suit": "major_arcana",
        "keywords": ["公正", "平衡", "真相", "因果"],
        "upright": {
            "meaning": "公正裁决，寻求真相，平衡状态，因果报应",
            "love": "公平的关系，诚实相待",
            "career": "公正待遇，法律相关",
            "health": "身心平衡，公正对待身体"
        },
        "reversed": {
            "meaning": "不公正，偏见，逃避责任，不平衡",
            "love": "关系不平等，不诚实",
            "career": "不公待遇，偏见歧视",
            "health": "失衡状态，逃避治疗"
        }
    },
    "倒吊人": {
        "number": 12,
        "suit": "major_arcana",
        "keywords": ["牺牲", "等待", "新视角", "暂停"],
        "upright": {
            "meaning": "为了更大目标而牺牲，等待时机，换个角度看问题",
            "love": "为爱牺牲，等待时机",
            "career": "暂时的停顿，重新考虑",
            "health": "休息调养，改变生活方式"
        },
        "reversed": {
            "meaning": "无谓的牺牲，拒绝改变，固执己见，浪费时间",
            "love": "过度牺牲，固执不变",
            "career": "拒绝改变，浪费机会",
            "health": "拒绝治疗，固执己见"
        }
    },
    "死神": {
        "number": 13,
        "suit": "major_arcana",
        "keywords": ["结束", "转变", "重生", "释放"],
        "upright": {
            "meaning": "结束旧的开始新的，重大转变，释放过去，重生",
            "love": "关系结束或重大改变",
            "career": "工作变动，职业转型",
            "health": "康复转机，生活方式改变"
        },
        "reversed": {
            "meaning": "拒绝改变，恐惧结束，停滞不前，无法释怀",
            "love": "害怕分手，拒绝改变",
            "career": "害怕变动，固守现状",
            "health": "拒绝治疗，害怕改变"
        }
    },
    "节制": {
        "number": 14,
        "suit": "major_arcana",
        "keywords": ["平衡", "节制", "和谐", "治愈"],
        "upright": {
            "meaning": "平衡各方面，适度节制，和谐统一，治愈过程",
            "love": "关系和谐，互相平衡",
            "career": "工作生活平衡，团队合作",
            "health": "身心和谐，康复进展"
        },
        "reversed": {
            "meaning": "失去平衡，过度极端，缺乏自制，关系不和",
            "love": "关系失衡，缺乏沟通",
            "career": "工作过度，缺乏平衡",
            "health": "生活失调，缺乏节制"
        }
    },
    "恶魔": {
        "number": 15,
        "suit": "major_arcana",
        "keywords": ["束缚", "诱惑", "物质", "成瘾"],
        "upright": {
            "meaning": "受到束缚，物质诱惑，成瘾行为，恐惧支配",
            "love": "不健康的关系，占有欲",
            "career": "被工作束缚，金钱诱惑",
            "health": "不良习惯，成瘾问题"
        },
        "reversed": {
            "meaning": "摆脱束缚，克服诱惑，觉醒意识，获得自由",
            "love": "摆脱不良关系，获得自由",
            "career": "摆脱束缚，重获自主",
            "health": "戒除恶习，重获健康"
        }
    },
    "塔": {
        "number": 16,
        "suit": "major_arcana",
        "keywords": ["突变", "灾难", "觉醒", "解放"],
        "upright": {
            "meaning": "突然的变化，破坏重建，觉醒时刻，从假象中解脱",
            "love": "关系突然破裂，觉醒真相",
            "career": "突然的变化，职业震荡",
            "health": "突发疾病，身体警告"
        },
        "reversed": {
            "meaning": "避免灾难，渐进变化，拒绝觉醒，内在震荡",
            "love": "避免分手，内心震荡",
            "career": "避免失业，内在变化",
            "health": "预防疾病，内在调整"
        }
    },
    "星星": {
        "number": 17,
        "suit": "major_arcana",
        "keywords": ["希望", "信仰", "灵感", "治愈"],
        "upright": {
            "meaning": "希望重燃，精神信仰，灵感启发，心灵治愈",
            "love": "重燃希望，精神连接",
            "career": "前景光明，灵感创作",
            "health": "康复希望，精神治疗"
        },
        "reversed": {
            "meaning": "失去希望，信仰危机，缺乏灵感，绝望感",
            "love": "对爱绝望，失去信心",
            "career": "前景暗淡，缺乏动力",
            "health": "治疗无望，精神低落"
        }
    },
    "月亮": {
        "number": 18,
        "suit": "major_arcana",
        "keywords": ["幻象", "恐惧", "潜意识", "直觉"],
        "upright": {
            "meaning": "幻象迷惑，内在恐惧，潜意识影响，需要信任直觉",
            "love": "感情迷茫，不确定性",
            "career": "前路不明，需要直觉",
            "health": "心理问题，潜意识影响"
        },
        "reversed": {
            "meaning": "真相显现，恐惧消散，觉察幻象，理性回归",
            "love": "关系真相，理性思考",
            "career": "情况明朗，理性决策",
            "health": "症状明确，理性治疗"
        }
    },
    "太阳": {
        "number": 19,
        "suit": "major_arcana",
        "keywords": ["成功", "快乐", "活力", "正能量"],
        "upright": {
            "meaning": "成功喜悦，积极乐观，充满活力，正面能量",
            "love": "快乐的关系，阳光积极",
            "career": "事业成功，积极发展",
            "health": "身体健康，精力充沛"
        },
        "reversed": {
            "meaning": "缺乏自信，过度乐观，虚假快乐，能量不足",
            "love": "表面快乐，缺乏深度",
            "career": "过度自信，盲目乐观",
            "health": "虚弱无力，假性健康"
        }
    },
    "审判": {
        "number": 20,
        "suit": "major_arcana",
        "keywords": ["重生", "觉醒", "宽恕", "召唤"],
        "upright": {
            "meaning": "精神觉醒，重获新生，宽恕过去，听从召唤",
            "love": "关系重生，原谅过去",
            "career": "职业召唤，重新开始",
            "health": "康复重生，精神觉醒"
        },
        "reversed": {
            "meaning": "缺乏觉悟，拒绝宽恕，错失机会，自我怀疑",
            "love": "无法原谅，错失复合",
            "career": "自我怀疑，错失机会",
            "health": "拒绝康复，缺乏觉悟"
        }
    },
    "世界": {
        "number": 21,
        "suit": "major_arcana",
        "keywords": ["完成", "成功", "实现", "统一"],
        "upright": {
            "meaning": "目标完成，圆满成功，世界在手，完美统一",
            "love": "完美关系，灵魂伴侣",
            "career": "事业成功，目标达成",
            "health": "完全康复，身心统一"
        },
        "reversed": {
            "meaning": "缺乏完成，延迟成功，目标未达，内在空虚",
            "love": "关系未完善，缺乏满足",
            "career": "目标未达，需要努力",
            "health": "康复缓慢，需要坚持"
        }
    },

    # 小阿卡纳 - 权杖组 (Wands/Rods) - 14张
    "权杖王牌": {
        "number": 1,
        "suit": "wands",
        "keywords": ["新开始", "创造力", "灵感", "机会"],
        "upright": {
            "meaning": "新的创意项目，灵感涌现，充满热情的开始",
            "love": "新恋情的开始，充满激情",
            "career": "新的工作机会，创意项目",
            "health": "新的健康计划，精力恢复"
        },
        "reversed": {
            "meaning": "缺乏方向，创意阻滞，错失机会，能量分散",
            "love": "缺乏激情，机会错失",
            "career": "项目延迟，创意枯竭",
            "health": "缺乏动力，计划失败"
        }
    },
    "权杖二": {
        "number": 2,
        "suit": "wands",
        "keywords": ["计划", "决策", "个人力量", "等待"],
        "upright": {
            "meaning": "制定长期计划，等待时机，个人权力，未来规划",
            "love": "考虑感情的未来，做出决定",
            "career": "职业规划，等待机会",
            "health": "健康计划，长期目标"
        },
        "reversed": {
            "meaning": "缺乏计划，犹豫不决，害怕改变，目光短浅",
            "love": "无法决定感情方向",
            "career": "缺乏规划，犹豫不决",
            "health": "计划不当，缺乏远见"
        }
    },
    "权杖三": {
        "number": 3,
        "suit": "wands",
        "keywords": ["扩展", "远见", "领导", "贸易"],
        "upright": {
            "meaning": "扩展视野，领导能力，贸易机会，远见卓识",
            "love": "关系发展，远距离恋爱",
            "career": "业务扩展，领导机会",
            "health": "拓展治疗方式，远见规划"
        },
        "reversed": {
            "meaning": "缺乏远见，计划失败，延迟，个人局限",
            "love": "关系停滞，缺乏发展",
            "career": "扩展失败，缺乏领导力",
            "health": "计划受阻，视野狭窄"
        }
    },

    # 小阿卡纳 - 圣杯组 (Cups) - 14张
    "圣杯王牌": {
        "number": 1,
        "suit": "cups",
        "keywords": ["新感情", "爱", "直觉", "精神满足"],
        "upright": {
            "meaning": "新的感情开始，心灵满足，直觉敏锐，爱的礼物",
            "love": "新恋情，深层情感连接",
            "career": "工作满足感，团队和谐",
            "health": "情感康复，心理健康"
        },
        "reversed": {
            "meaning": "情感阻塞，爱的失落，直觉混乱，心灵空虚",
            "love": "感情受阻，缺乏连接",
            "career": "工作不满，人际关系差",
            "health": "情感问题，心理压力"
        }
    },
    "圣杯二": {
        "number": 2,
        "suit": "cups",
        "keywords": ["伙伴关系", "结合", "相互吸引", "和谐"],
        "upright": {
            "meaning": "和谐的伙伴关系，相互吸引，情感平衡，真诚连接",
            "love": "完美的情侣关系，婚姻",
            "career": "良好的合作关系",
            "health": "身心和谐，伴侣支持"
        },
        "reversed": {
            "meaning": "关系失衡，分离，缺乏沟通，自我保护",
            "love": "关系问题，沟通障碍",
            "career": "合作困难，缺乏协调",
            "health": "身心失调，缺乏支持"
        }
    },

    # 小阿卡纳 - 宝剑组 (Swords) - 14张  
    "宝剑王牌": {
        "number": 1,
        "suit": "swords",
        "keywords": ["新想法", "心智力量", "真相", "突破"],
        "upright": {
            "meaning": "新的想法和洞察，心智突破，真相显现，理性思考",
            "love": "理性看待感情，沟通重要",
            "career": "新的想法，智力挑战",
            "health": "心理突破，理性治疗"
        },
        "reversed": {
            "meaning": "混乱思维，误解，缺乏清晰，心智阻塞",
            "love": "误解和冲突，沟通不良",
            "career": "思路不清，决策困难",
            "health": "心理混乱，缺乏理性"
        }
    },
    "宝剑二": {
        "number": 2,
        "suit": "swords",
        "keywords": ["艰难选择", "平衡", "僵局", "决定"],
        "upright": {
            "meaning": "面临艰难选择，需要平衡，暂时的僵局，冷静决策",
            "love": "关系中的选择，理性分析",
            "career": "职业选择，权衡利弊",
            "health": "治疗选择，理性分析"
        },
        "reversed": {
            "meaning": "优柔寡断，逃避决定，信息过载，内心冲突",
            "love": "无法做出感情决定",
            "career": "逃避重要决策",
            "health": "拖延治疗，犹豫不决"
        }
    },

    # 小阿卡纳 - 星币组 (Pentacles/Coins) - 14张
    "星币王牌": {
        "number": 1,
        "suit": "pentacles",
        "keywords": ["新机会", "物质开始", "实用性", "安全"],
        "upright": {
            "meaning": "新的物质机会，财务开始，实用的礼物，安全基础",
            "love": "稳定的关系基础，实际的表达",
            "career": "新的工作机会，物质收获",
            "health": "身体健康改善，实际的治疗"
        },
        "reversed": {
            "meaning": "错失机会，财务问题，不实际，缺乏安全感",
            "love": "关系缺乏稳定，物质困扰",
            "career": "机会错失，财务不稳",
            "health": "忽视身体需求，不实际的期望"
        }
    },
    "星币二": {
        "number": 2,
        "suit": "pentacles",
        "keywords": ["平衡", "多任务", "适应性", "灵活性"],
        "upright": {
            "meaning": "平衡多个优先事项，适应性强，灵活处理，时间管理",
            "love": "平衡关系和其他责任",
            "career": "多任务处理，工作平衡",
            "health": "平衡各方面健康需求"
        },
        "reversed": {
            "meaning": "失去平衡，压力过大，缺乏组织，时间管理差",
            "love": "关系失衡，缺乏时间",
            "career": "工作过载，组织混乱",
            "health": "生活失衡，压力过大"
        }
    }
}

# 牌阵位置含义
POSITION_MEANINGS = {
    "single": {
        1: "整体指导"
    },
    "three_card": {
        1: "过去/根源",
        2: "现在/当前状况", 
        3: "未来/结果"
    },
    "celtic_cross": {
        1: "当前状况",
        2: "挑战/阻碍",
        3: "遥远的过去/根基",
        4: "近期的过去",
        5: "可能的未来",
        6: "近期的未来",
        7: "你的方法",
        8: "外在影响",
        9: "希望和恐惧",
        10: "最终结果"
    }
}

def get_card_info(card_name: str, position: str = None) -> dict:
    """
    获取塔罗牌信息
    
    Args:
        card_name: 塔罗牌名称
        position: 牌的位置信息（可选）
        
    Returns:
        包含牌意、关键词、正逆位解释等信息的字典
    """
    if card_name not in TAROT_CARDS:
        return {"error": f"未找到牌名: {card_name}"}
    
    card_info = TAROT_CARDS[card_name].copy()
    
    # 如果提供了位置信息，添加位置含义
    if position:
        card_info["position_meaning"] = position
    
    return card_info

def get_all_cards() -> list:
    """获取所有塔罗牌名称列表"""
    return list(TAROT_CARDS.keys())

def get_cards_by_suit(suit: str) -> list:
    """根据牌组获取牌名列表"""
    return [name for name, info in TAROT_CARDS.items() if info["suit"] == suit]

def search_cards_by_keyword(keyword: str) -> list:
    """根据关键词搜索相关塔罗牌"""
    results = []
    keyword_lower = keyword.lower()
    
    for name, info in TAROT_CARDS.items():
        # 检查牌名
        if keyword_lower in name.lower():
            results.append(name)
            continue
            
        # 检查关键词
        if any(keyword_lower in kw.lower() for kw in info["keywords"]):
            results.append(name)
            continue
            
        # 检查正位含义
        upright_text = " ".join(str(v) for v in info["upright"].values())
        if keyword_lower in upright_text.lower():
            results.append(name)
    
    return results

if __name__ == "__main__":
    # 测试功能
    print("测试塔罗牌数据库功能:")
    
    # 测试获取单张牌信息
    card_info = get_card_info("愚者")
    print(f"\n愚者牌信息: {card_info}")
    
    # 测试获取所有牌
    all_cards = get_all_cards()
    print(f"\n总共有 {len(all_cards)} 张牌")
    
    # 测试按牌组获取
    major_arcana = get_cards_by_suit("major_arcana")
    print(f"\n大阿卡纳有 {len(major_arcana)} 张牌")
    
    # 测试关键词搜索
    love_cards = search_cards_by_keyword("爱情")
    print(f"\n包含'爱情'关键词的牌: {love_cards}")

