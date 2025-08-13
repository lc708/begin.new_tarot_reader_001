# utils/card_drawer.py
"""
随机抽牌工具函数
实现塔罗牌的随机抽取逻辑，确保不重复
"""

import random
from typing import List, Dict, Optional
try:
    from .tarot_database import get_all_cards
except ImportError:
    from tarot_database import get_all_cards

def draw_cards(num_cards: int, exclude_cards: Optional[List[str]] = None) -> List[Dict[str, any]]:
    """
    随机抽取指定数量的塔罗牌
    
    Args:
        num_cards: 需要抽取的牌数
        exclude_cards: 要排除的牌名列表（可选）
        
    Returns:
        包含牌名、正逆位状态和位置的字典列表
    """
    if exclude_cards is None:
        exclude_cards = []
    
    # 获取所有可用的牌
    all_cards = get_all_cards()
    available_cards = [card for card in all_cards if card not in exclude_cards]
    
    if num_cards > len(available_cards):
        raise ValueError(f"请求的牌数 ({num_cards}) 超过了可用牌数 ({len(available_cards)})")
    
    # 随机选择牌
    selected_cards = random.sample(available_cards, num_cards)
    
    # 为每张牌生成信息
    drawn_cards = []
    for i, card_name in enumerate(selected_cards):
        # 随机决定正逆位 (30%概率为逆位)
        is_reversed = random.random() < 0.3
        
        card_info = {
            "name": card_name,
            "reversed": is_reversed,
            "position": i + 1,
            "orientation": "reversed" if is_reversed else "upright"
        }
        drawn_cards.append(card_info)
    
    return drawn_cards

def shuffle_deck() -> List[str]:
    """
    洗牌功能 - 返回打乱顺序的完整牌组
    
    Returns:
        打乱顺序的所有塔罗牌列表
    """
    all_cards = get_all_cards()
    shuffled_cards = all_cards.copy()
    random.shuffle(shuffled_cards)
    return shuffled_cards

def draw_single_card(exclude_cards: Optional[List[str]] = None) -> Dict[str, any]:
    """
    抽取单张牌的便捷函数
    
    Args:
        exclude_cards: 要排除的牌名列表（可选）
        
    Returns:
        单张牌的信息字典
    """
    cards = draw_cards(1, exclude_cards)
    return cards[0]

def draw_three_cards(exclude_cards: Optional[List[str]] = None) -> List[Dict[str, any]]:
    """
    抽取三张牌的便捷函数（过去-现在-未来）
    
    Args:
        exclude_cards: 要排除的牌名列表（可选）
        
    Returns:
        三张牌的信息列表
    """
    return draw_cards(3, exclude_cards)

def draw_celtic_cross(exclude_cards: Optional[List[str]] = None) -> List[Dict[str, any]]:
    """
    抽取凯尔特十字牌阵的十张牌
    
    Args:
        exclude_cards: 要排除的牌名列表（可选）
        
    Returns:
        十张牌的信息列表
    """
    return draw_cards(10, exclude_cards)

def get_card_probability_info() -> Dict[str, any]:
    """
    获取抽牌概率信息
    
    Returns:
        包含概率信息的字典
    """
    total_cards = len(get_all_cards())
    return {
        "total_cards": total_cards,
        "upright_probability": 0.7,  # 70%概率正位
        "reversed_probability": 0.3,  # 30%概率逆位
        "major_arcana_count": 22,
        "minor_arcana_count": 56
    }

def simulate_card_draw(num_simulations: int = 1000) -> Dict[str, any]:
    """
    模拟抽牌统计，用于测试随机性
    
    Args:
        num_simulations: 模拟次数
        
    Returns:
        统计信息字典
    """
    upright_count = 0
    reversed_count = 0
    card_frequency = {}
    
    for _ in range(num_simulations):
        card = draw_single_card()
        
        # 统计正逆位
        if card["reversed"]:
            reversed_count += 1
        else:
            upright_count += 1
            
        # 统计每张牌的出现频率
        card_name = card["name"]
        card_frequency[card_name] = card_frequency.get(card_name, 0) + 1
    
    return {
        "simulations": num_simulations,
        "upright_percentage": (upright_count / num_simulations) * 100,
        "reversed_percentage": (reversed_count / num_simulations) * 100,
        "most_frequent_card": max(card_frequency, key=card_frequency.get),
        "card_frequency": card_frequency
    }

if __name__ == "__main__":
    # 测试抽牌功能
    print("测试随机抽牌功能:")
    
    # 测试单张牌
    print("\n1. 测试单张牌抽取:")
    single_card = draw_single_card()
    print(f"抽到的牌: {single_card}")
    
    # 测试三张牌
    print("\n2. 测试三张牌抽取:")
    three_cards = draw_three_cards()
    for i, card in enumerate(three_cards, 1):
        position = ["过去", "现在", "未来"][i-1]
        orientation = "逆位" if card["reversed"] else "正位"
        print(f"{position}: {card['name']} ({orientation})")
    
    # 测试十张牌
    print("\n3. 测试凯尔特十字牌阵:")
    celtic_cards = draw_celtic_cross()
    positions = ["当前状况", "挑战", "遥远过去", "近期过去", "可能未来", 
                "近期未来", "你的方法", "外在影响", "希望恐惧", "最终结果"]
    for i, card in enumerate(celtic_cards):
        orientation = "逆位" if card["reversed"] else "正位"
        print(f"{positions[i]}: {card['name']} ({orientation})")
    
    # 测试概率信息
    print("\n4. 抽牌概率信息:")
    prob_info = get_card_probability_info()
    print(f"总牌数: {prob_info['total_cards']}")
    print(f"正位概率: {prob_info['upright_probability']*100}%")
    print(f"逆位概率: {prob_info['reversed_probability']*100}%")
    
    # 测试随机性
    print("\n5. 随机性测试 (100次模拟):")
    stats = simulate_card_draw(100)
    print(f"正位: {stats['upright_percentage']:.1f}%")
    print(f"逆位: {stats['reversed_percentage']:.1f}%")
    print(f"最常出现的牌: {stats['most_frequent_card']}")
