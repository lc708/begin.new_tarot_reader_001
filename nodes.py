# nodes.py
"""
塔罗牌占卜应用的节点实现
包含处理占卜流程的所有节点类
"""

from macore import Node
from utils.call_llm import call_llm
from utils.tarot_database import get_card_info
from utils.card_drawer import draw_cards
from utils.spread_config import get_spread_config, recommend_spread_for_question
from utils.reading_storage import save_reading
import json
from datetime import datetime

class QuestionInputNode(Node):
    """问题接收节点 - 接收并分析用户问题，确定问题类型和推荐牌阵"""
    
    def prep(self, shared):
        """从shared store读取用户输入的问题"""
        return {
            "question": shared.get("user_question", ""),
            "selected_spread": shared.get("spread_type", "")
        }
    
    def exec(self, prep_res):
        """简化问题分析，减少LLM调用以提高响应速度"""
        question = prep_res["question"]
        
        if not question.strip():
            return {
                "question_category": "general",
                "recommended_spread": "single",
                "analysis": "未提供具体问题，建议进行日常指导占卜"
            }
        
        # 使用关键词匹配简化分类，避免LLM调用
        question_lower = question.lower()
        
        # 关键词匹配
        if any(word in question_lower for word in ['爱情', '恋爱', '感情', '婚姻', '喜欢', '爱', '分手', '复合']):
            question_category = "love"
            complexity = "medium"
        elif any(word in question_lower for word in ['工作', '事业', '职业', '升职', '跳槽', '同事', '老板', '学习', '考试']):
            question_category = "career"
            complexity = "medium"
        elif any(word in question_lower for word in ['健康', '身体', '病', '心理', '压力', '焦虑', '抑郁']):
            question_category = "health"
            complexity = "medium"
        elif any(word in question_lower for word in ['选择', '决定', '该不该', '要不要', '怎么办', '如何']):
            question_category = "decision"
            complexity = "medium"
        else:
            question_category = "general"
            complexity = "simple"
        
        # 根据分析结果推荐牌阵
        if complexity == "complex":
            recommended_spread = "celtic_cross"
        elif question_category in ["love", "career", "decision"]:
            recommended_spread = "three_card"
        else:
            recommended_spread = "single"
        
        return {
            "question_category": question_category,
            "recommended_spread": recommended_spread,
            "analysis": f"根据问题关键词分析为{question_category}类型",
            "complexity": complexity
        }
    
    def post(self, shared, prep_res, exec_res):
        """将分析结果写入shared store"""
        shared["question_category"] = exec_res["question_category"]
        shared["recommended_spread"] = exec_res["recommended_spread"]
        shared["question_analysis"] = exec_res["analysis"]
        
        # 如果用户没有选择牌阵，使用推荐的
        if not shared.get("spread_type"):
            shared["spread_type"] = exec_res["recommended_spread"]
        
        return "default"

class SpreadSetupNode(Node):
    """牌阵初始化节点 - 根据选择的牌阵类型设置配置信息"""
    
    def prep(self, shared):
        """读取选择的牌阵类型"""
        return shared.get("spread_type", "single")
    
    def exec(self, spread_type):
        """获取牌阵配置信息"""
        spread_config = get_spread_config(spread_type)
        
        if "error" in spread_config:
            # 如果牌阵不存在，使用默认的单张牌
            spread_config = get_spread_config("single")
            spread_type = "single"
        
        return {
            "spread_type": spread_type,
            "config": spread_config
        }
    
    def post(self, shared, prep_res, exec_res):
        """将牌阵配置写入shared store"""
        shared["spread_type"] = exec_res["spread_type"]
        shared["spread_config"] = exec_res["config"]
        return "default"

class CardDrawingNode(Node):
    """随机抽牌节点 - 根据牌阵要求随机抽取塔罗牌"""
    
    def prep(self, shared):
        """读取牌阵配置中的牌数要求"""
        spread_config = shared.get("spread_config", {})
        card_count = spread_config.get("card_count", 1)
        exclude_cards = shared.get("exclude_cards", [])
        
        return {
            "card_count": card_count,
            "exclude_cards": exclude_cards
        }
    
    def exec(self, prep_res):
        """调用随机抽牌工具函数"""
        drawn_cards = draw_cards(
            num_cards=prep_res["card_count"],
            exclude_cards=prep_res["exclude_cards"]
        )
        return drawn_cards
    
    def post(self, shared, prep_res, exec_res):
        """将抽取的牌信息写入shared store"""
        shared["drawn_cards"] = exec_res
        return "default"

class CardMeaningNode(Node):
    """牌意检索节点 - 检索每张牌的详细含义信息"""
    
    def prep(self, shared):
        """读取抽取的牌列表和牌阵配置"""
        drawn_cards = shared.get("drawn_cards", [])
        spread_config = shared.get("spread_config", {})
        positions = spread_config.get("positions", {})
        
        return {
            "drawn_cards": drawn_cards,
            "positions": positions
        }
    
    def exec(self, prep_res):
        """批量获取每张牌的含义信息"""
        card_meanings = []
        
        for card in prep_res["drawn_cards"]:
            card_name = card["name"]
            position = card["position"]
            
            # 获取牌的基本信息
            card_info = get_card_info(card_name)
            
            # 添加位置含义
            position_info = prep_res["positions"].get(position, {})
            card_info["position_info"] = position_info
            card_info["card_state"] = card
            
            card_meanings.append(card_info)
        
        return card_meanings
    
    def post(self, shared, prep_res, exec_res):
        """将牌意信息写入shared store"""
        shared["card_meanings"] = exec_res
        return "default"

class IndividualReadingNode(Node):
    """个体解读节点 - 为每张牌在其位置上生成个性化解读"""
    
    def prep(self, shared):
        """读取牌信息、位置含义和用户问题"""
        return {
            "card_meanings": shared.get("card_meanings", []),
            "user_question": shared.get("user_question", ""),
            "question_category": shared.get("question_category", "general"),
            "spread_type": shared.get("spread_type", "single")
        }
    
    def exec(self, prep_res):
        """使用批量LLM调用为所有牌生成个性化解读（性能优化）"""
        if not prep_res["card_meanings"]:
            return []
        
        # 准备所有牌的信息
        cards_info = []
        for card_meaning in prep_res["card_meanings"]:
            card_state = card_meaning["card_state"]
            card_name = card_state["name"]
            is_reversed = card_state["reversed"]
            position = card_state["position"]
            
            # 获取牌意
            if is_reversed:
                meaning_text = card_meaning.get("reversed", {}).get("meaning", "")
                specific_meaning = card_meaning.get("reversed", {}).get(prep_res["question_category"], "")
            else:
                meaning_text = card_meaning.get("upright", {}).get("meaning", "")
                specific_meaning = card_meaning.get("upright", {}).get(prep_res["question_category"], "")
            
            # 位置含义
            position_info = card_meaning.get("position_info", {})
            position_name = position_info.get("name", f"位置{position}")
            position_description = position_info.get("description", "")
            
            cards_info.append({
                "card_name": card_name,
                "position": position,
                "position_name": position_name,
                "position_description": position_description,
                "is_reversed": is_reversed,
                "meaning_text": meaning_text,
                "specific_meaning": specific_meaning
            })
        
        # 构建批量解读的prompt
        cards_details = []
        for i, card_info in enumerate(cards_info, 1):
            card_detail = f"""
牌{i}: {card_info['card_name']} ({'逆位' if card_info['is_reversed'] else '正位'})
位置: {card_info['position_name']} - {card_info['position_description']}
基础含义: {card_info['meaning_text']}
特定含义: {card_info['specific_meaning']}"""
            cards_details.append(card_detail)
        
        batch_prompt = f"""
作为专业的塔罗牌占卜师，请为以下占卜提供每张牌的详细解读：

用户问题: "{prep_res['user_question']}"
问题类型: {prep_res['question_category']}
牌阵类型: {prep_res['spread_type']}

抽到的牌:
{chr(10).join(cards_details)}

请为每张牌提供个性化解读，每个解读应该：
1. 直接回应用户的问题
2. 考虑牌在当前位置的特殊含义  
3. 提供实用的建议和指导
4. 语言温暖而专业，150-200字

请按以下格式回答（严格按照格式，每张牌用"---"分隔）：

牌1解读:
[第一张牌的详细解读]

---

牌2解读:
[第二张牌的详细解读]

---

[依此类推...]
"""
        
        try:
            # 一次性获取所有牌的解读
            batch_reading = call_llm(batch_prompt)
            
            # 解析批量解读结果
            individual_readings = []
            
            # 按"---"分割解读
            readings_parts = batch_reading.split("---")
            
            for i, card_info in enumerate(cards_info):
                if i < len(readings_parts):
                    # 提取对应的解读文本
                    reading_text = readings_parts[i].strip()
                    # 移除"牌X解读:"前缀
                    if "解读:" in reading_text:
                        reading_text = reading_text.split("解读:", 1)[1].strip()
                    
                    individual_readings.append({
                        "card_name": card_info["card_name"],
                        "position": card_info["position"],
                        "position_name": card_info["position_name"],
                        "reversed": card_info["is_reversed"],
                        "reading": reading_text
                    })
                else:
                    # 备用解读
                    fallback_reading = f"{card_info['card_name']}{'逆位' if card_info['is_reversed'] else '正位'}在{card_info['position_name']}位置出现，{card_info['meaning_text']}"
                    individual_readings.append({
                        "card_name": card_info["card_name"],
                        "position": card_info["position"],
                        "position_name": card_info["position_name"],
                        "reversed": card_info["is_reversed"],
                        "reading": fallback_reading
                    })
            
            return individual_readings
            
        except Exception as e:
            print(f"批量生成解读失败: {e}")
            # 提供所有牌的备用解读
            individual_readings = []
            for card_info in cards_info:
                fallback_reading = f"{card_info['card_name']}{'逆位' if card_info['is_reversed'] else '正位'}在{card_info['position_name']}位置出现，{card_info['meaning_text']}"
                individual_readings.append({
                    "card_name": card_info["card_name"],
                    "position": card_info["position"],
                    "position_name": card_info["position_name"],
                    "reversed": card_info["is_reversed"],
                    "reading": fallback_reading
                })
            return individual_readings
    
    def post(self, shared, prep_res, exec_res):
        """将单张牌解读写入shared store"""
        shared["individual_readings"] = exec_res
        return "default"

class CombinedReadingNode(Node):
    """综合解读节点 - 整合所有牌的含义生成完整的占卜解读"""
    
    def prep(self, shared):
        """读取所有单张牌解读和相关信息"""
        return {
            "individual_readings": shared.get("individual_readings", []),
            "card_meanings": shared.get("card_meanings", []),  # 备用数据
            "drawn_cards": shared.get("drawn_cards", []),      # 备用数据
            "user_question": shared.get("user_question", ""),
            "question_category": shared.get("question_category", "general"),
            "spread_type": shared.get("spread_type", "single"),
            "spread_config": shared.get("spread_config", {})
        }
    
    def exec(self, prep_res):
        """使用LLM生成综合性的占卜解读和建议"""
        # 检查是否有个体解读结果
        if prep_res["individual_readings"]:
            # 完整模式：整理所有单张牌的解读
            cards_summary = []
            for reading in prep_res["individual_readings"]:
                card_info = f"{reading['position_name']}: {reading['card_name']}{'(逆位)' if reading['reversed'] else ''} - {reading['reading']}"
                cards_summary.append(card_info)
            cards_text = "\n\n".join(cards_summary)
        else:
            # 快速模式：使用基本牌信息
            cards_summary = []
            for card in prep_res["drawn_cards"]:
                card_name = card["name"]
                is_reversed = card.get("reversed", False)
                position = card.get("position", 1)
                
                # 获取基本牌意
                card_meaning = None
                for meaning in prep_res["card_meanings"]:
                    if meaning.get("card_state", {}).get("name") == card_name:
                        card_meaning = meaning
                        break
                
                if card_meaning:
                    if is_reversed:
                        basic_meaning = card_meaning.get("reversed", {}).get("meaning", "")
                    else:
                        basic_meaning = card_meaning.get("upright", {}).get("meaning", "")
                    
                    card_info = f"位置{position}: {card_name}{'(逆位)' if is_reversed else ''} - {basic_meaning}"
                else:
                    card_info = f"位置{position}: {card_name}{'(逆位)' if is_reversed else ''}"
                
                cards_summary.append(card_info)
            cards_text = "\n\n".join(cards_summary)
        
        prompt = f"""
作为资深塔罗牌占卜师，请基于以下信息提供一个综合性的占卜解读：

用户问题: "{prep_res['user_question']}"
问题类型: {prep_res['question_category']}
使用牌阵: {prep_res['spread_config'].get('name', '未知牌阵')}

各张牌的解读:
{cards_text}

请提供一个整体性的解读，包括：
1. 对用户问题的综合回答
2. 各张牌之间的联系和整体信息
3. 实用的建议和行动指导
4. 对未来趋势的展望
5. 温暖的鼓励和支持

请用温暖、专业且富有洞察力的语言，提供一个完整而深入的解读。字数控制在300-400字。
"""
        
        try:
            combined_reading = call_llm(prompt)
            
            # 从解读中提取简短总结，而不是再次调用LLM
            lines = combined_reading.strip().split('\n')
            summary = "塔罗牌为你的问题提供了重要的指导和洞察。"
            
            # 尝试提取第一段作为总结
            if lines:
                first_line = lines[0].strip()
                if len(first_line) > 10 and len(first_line) < 50:
                    summary = first_line
                elif len(combined_reading) > 0:
                    # 取前30个字符作为简要总结
                    summary = combined_reading[:30].strip() + "..."
            
            return {
                "combined_reading": combined_reading.strip(),
                "reading_summary": summary
            }
            
        except Exception as e:
            print(f"生成综合解读失败: {e}")
            # 提供备用解读
            fallback_reading = f"根据抽取的{len(prep_res['individual_readings'])}张牌，塔罗牌为你的问题提供了多层面的指导。每张牌都代表着不同的能量和信息，建议你仔细思考每张牌的含义，并将它们作为你决策的参考。"
            return {
                "combined_reading": fallback_reading,
                "reading_summary": "塔罗牌为你提供了重要的指导。"
            }
    
    def post(self, shared, prep_res, exec_res):
        """将最终解读写入shared store"""
        shared["combined_reading"] = exec_res["combined_reading"]
        shared["reading_summary"] = exec_res["reading_summary"]
        return "default"

class SaveReadingNode(Node):
    """结果保存节点 - 保存完整的占卜记录"""
    
    def prep(self, shared):
        """读取完整的占卜数据"""
        return {
            "reading_data": {
                "user_question": shared.get("user_question", ""),
                "question_category": shared.get("question_category", ""),
                "spread_type": shared.get("spread_type", ""),
                "spread_config": shared.get("spread_config", {}),
                "drawn_cards": shared.get("drawn_cards", []),
                "card_meanings": shared.get("card_meanings", []),
                "individual_readings": shared.get("individual_readings", []),
                "combined_reading": shared.get("combined_reading", ""),
                "reading_summary": shared.get("reading_summary", ""),
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def exec(self, prep_res):
        """调用存储工具函数保存数据"""
        success = save_reading(prep_res["reading_data"])
        return {"success": success}
    
    def post(self, shared, prep_res, exec_res):
        """更新保存状态"""
        shared["save_success"] = exec_res["success"]
        if exec_res["success"]:
            shared["save_message"] = "占卜记录已成功保存"
        else:
            shared["save_message"] = "占卜记录保存失败"
        
        return "default"

if __name__ == "__main__":
    # 测试节点功能
    print("测试塔罗牌占卜节点:")
    
    # 创建测试用的shared store
    test_shared = {
        "user_question": "我今天的工作运势如何？",
        "spread_type": "three_card"
    }
    
    print(f"\n测试问题: {test_shared['user_question']}")
    print(f"选择牌阵: {test_shared['spread_type']}")
    
    # 测试问题输入节点
    print("\n1. 测试问题分析节点:")
    question_node = QuestionInputNode()
    result = question_node.run(test_shared)
    print(f"问题类型: {test_shared.get('question_category')}")
    print(f"推荐牌阵: {test_shared.get('recommended_spread')}")
    
    # 测试牌阵设置节点
    print("\n2. 测试牌阵设置节点:")
    spread_node = SpreadSetupNode()
    spread_node.run(test_shared)
    print(f"牌阵名称: {test_shared['spread_config']['name']}")
    print(f"需要抽牌: {test_shared['spread_config']['card_count']}张")
    
    # 测试抽牌节点
    print("\n3. 测试抽牌节点:")
    draw_node = CardDrawingNode()
    draw_node.run(test_shared)
    print("抽到的牌:")
    for card in test_shared['drawn_cards']:
        orientation = "逆位" if card['reversed'] else "正位"
        print(f"  位置{card['position']}: {card['name']} ({orientation})")
    
    print("\n节点测试完成！")