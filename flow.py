# flow.py
"""
塔罗牌占卜应用的流程实现
定义和创建完整的占卜流程
"""

from macore import Flow
from nodes import (
    QuestionInputNode, SpreadSetupNode, CardDrawingNode,
    CardMeaningNode, IndividualReadingNode, CombinedReadingNode,
    SaveReadingNode
)

def create_tarot_reading_flow():
    """
    创建完整的塔罗牌占卜流程
    
    Returns:
        配置好的Flow对象
    """
    # 创建所有节点实例
    question_input = QuestionInputNode()
    spread_setup = SpreadSetupNode()
    card_drawing = CardDrawingNode()
    card_meaning = CardMeaningNode()
    individual_reading = IndividualReadingNode()
    combined_reading = CombinedReadingNode()
    save_reading = SaveReadingNode()
    
    # 连接节点形成流程
    # 线性流程：问题输入 -> 牌阵设置 -> 抽牌 -> 获取牌意 -> 个体解读 -> 综合解读 -> 保存结果
    question_input >> spread_setup
    spread_setup >> card_drawing
    card_drawing >> card_meaning
    card_meaning >> individual_reading
    individual_reading >> combined_reading
    combined_reading >> save_reading
    
    # 创建并返回流程
    flow = Flow(start=question_input)
    return flow

def create_quick_reading_flow():
    """
    创建快速占卜流程（跳过保存步骤和部分LLM调用）
    适用于演示或临时占卜，响应更快
    
    Returns:
        配置好的Flow对象
    """
    # 创建节点实例（使用简化版本）
    question_input = QuestionInputNode()
    spread_setup = SpreadSetupNode()
    card_drawing = CardDrawingNode()
    card_meaning = CardMeaningNode()
    # 跳过individual_reading以减少LLM调用
    combined_reading = CombinedReadingNode()
    
    # 连接节点形成简化流程
    question_input >> spread_setup
    spread_setup >> card_drawing
    card_drawing >> card_meaning
    card_meaning >> combined_reading  # 直接跳到综合解读
    
    # 创建并返回流程
    flow = Flow(start=question_input)
    return flow

def create_simple_reading_flow():
    """
    创建简化的占卜流程（仅用于单张牌快速占卜）
    
    Returns:
        配置好的Flow对象
    """
    # 创建必要的节点
    question_input = QuestionInputNode()
    spread_setup = SpreadSetupNode()
    card_drawing = CardDrawingNode()
    card_meaning = CardMeaningNode()
    combined_reading = CombinedReadingNode()
    
    # 连接节点（跳过个体解读，直接进行综合解读）
    question_input >> spread_setup
    spread_setup >> card_drawing
    card_drawing >> card_meaning
    card_meaning >> combined_reading
    
    flow = Flow(start=question_input)
    return flow

def run_tarot_reading(user_question: str, spread_type: str = None, save_result: bool = True):
    """
    运行完整的塔罗牌占卜流程
    
    Args:
        user_question: 用户的问题
        spread_type: 指定的牌阵类型（可选，如果不指定会自动推荐）
        save_result: 是否保存结果
        
    Returns:
        包含占卜结果的字典
    """
    # 准备shared store
    shared = {
        "user_question": user_question,
        "spread_type": spread_type,
        "ui_spec": {},  # 前端UI规范（预留）
        "style_spec": {}  # 样式规范（预留）
    }
    
    # 选择合适的流程 - 使用优化后的完整流程
    if save_result:
        # 使用完整流程（已优化批量LLM调用）
        flow = create_tarot_reading_flow()
    else:
        # 演示模式使用快速流程
        flow = create_quick_reading_flow()
    
    # 运行流程
    try:
        flow.run(shared)
        
        # 整理返回结果
        result = {
            "success": True,
            "question": shared.get("user_question", ""),
            "question_category": shared.get("question_category", ""),
            "spread_type": shared.get("spread_type", ""),
            "spread_name": shared.get("spread_config", {}).get("name", ""),
            "drawn_cards": shared.get("drawn_cards", []),
            "individual_readings": shared.get("individual_readings", []),
            "combined_reading": shared.get("combined_reading", ""),
            "reading_summary": shared.get("reading_summary", ""),
            "save_success": shared.get("save_success", False) if save_result else None,
            "timestamp": shared.get("timestamp", "")
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "question": user_question
        }

def run_batch_readings(questions_list: list, spread_type: str = "single"):
    """
    批量运行多个占卜问题
    
    Args:
        questions_list: 问题列表
        spread_type: 统一使用的牌阵类型
        
    Returns:
        所有占卜结果的列表
    """
    results = []
    
    for question in questions_list:
        result = run_tarot_reading(question, spread_type, save_result=False)
        results.append(result)
    
    return results

def demo_reading():
    """
    演示占卜功能
    
    Returns:
        演示结果
    """
    demo_questions = [
        "我今天的运势如何？",
        "我的感情状况会有什么发展？",
        "我应该接受这个新的工作机会吗？"
    ]
    
    print("=== 塔罗牌占卜演示 ===\n")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"【演示 {i}】{question}")
        print("-" * 50)
        
        result = run_tarot_reading(question, save_result=False)
        
        if result["success"]:
            print(f"问题类型: {result['question_category']}")
            print(f"使用牌阵: {result['spread_name']}")
            print(f"抽到的牌:")
            
            for card in result["drawn_cards"]:
                orientation = "逆位" if card["reversed"] else "正位"
                print(f"  • {card['name']} ({orientation})")
            
            print(f"\n综合解读:")
            print(result["combined_reading"])
            print(f"\n核心信息: {result['reading_summary']}")
        else:
            print(f"占卜失败: {result.get('error', '未知错误')}")
        
        print("\n" + "="*60 + "\n")
    
    return "演示完成"

if __name__ == "__main__":
    # 测试流程功能
    print("测试塔罗牌占卜流程:")
    
    # 测试单个占卜
    print("\n1. 测试单个占卜:")
    test_question = "我最近的工作状况如何？"
    result = run_tarot_reading(test_question, spread_type="three_card", save_result=False)
    
    if result["success"]:
        print(f"✓ 占卜成功")
        print(f"问题: {result['question']}")
        print(f"类型: {result['question_category']}")
        print(f"牌阵: {result['spread_name']}")
        print(f"抽到 {len(result['drawn_cards'])} 张牌")
        print(f"解读长度: {len(result['combined_reading'])} 字符")
    else:
        print(f"✗ 占卜失败: {result.get('error')}")
    
    # 测试批量占卜
    print("\n2. 测试批量占卜:")
    test_questions = [
        "今日运势",
        "感情状况",
        "工作机会"
    ]
    batch_results = run_batch_readings(test_questions)
    print(f"✓ 批量处理 {len(batch_results)} 个问题")
    successful = sum(1 for r in batch_results if r["success"])
    print(f"成功率: {successful}/{len(batch_results)}")
    
    print("\n流程测试完成！")