# main.py
"""
塔罗牌占卜师应用主程序
提供命令行界面和API接口
"""

import argparse
import json
from datetime import datetime
from flow import run_tarot_reading, demo_reading, run_batch_readings
from utils.reading_storage import get_reading_statistics, load_all_readings, get_readings_by_question_type
from utils.spread_config import get_all_spreads, get_spread_config
from utils.tarot_database import get_all_cards, get_cards_by_suit, search_cards_by_keyword

def interactive_reading():
    """交互式占卜模式"""
    print("🔮 欢迎来到神秘塔罗牌占卜师 🔮")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 进行塔罗牌占卜")
        print("2. 查看占卜历史")
        print("3. 学习塔罗牌")
        print("4. 查看统计信息")
        print("5. 演示模式")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == "0":
            print("感谢使用塔罗牌占卜师，愿智慧与你同在！ ✨")
            break
        elif choice == "1":
            perform_reading()
        elif choice == "2":
            view_reading_history()
        elif choice == "3":
            learn_tarot()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            demo_reading()
        else:
            print("无效选择，请重新输入。")

def perform_reading():
    """执行占卜"""
    print("\n🌟 开始新的占卜 🌟")
    print("-" * 30)
    
    # 获取用户问题
    question = input("请输入你想要占卜的问题: ").strip()
    if not question:
        print("问题不能为空，请重新输入。")
        return
    
    # 选择牌阵
    print("\n可用的牌阵:")
    spreads = get_all_spreads()
    for i, spread_name in enumerate(spreads, 1):
        config = get_spread_config(spread_name)
        print(f"{i}. {config['name']} ({config['card_count']}张牌) - {config['description']}")
    
    spread_choice = input(f"\n请选择牌阵 (1-{len(spreads)}) 或按回车自动推荐: ").strip()
    
    if spread_choice.isdigit() and 1 <= int(spread_choice) <= len(spreads):
        spread_type = spreads[int(spread_choice) - 1]
    else:
        spread_type = None  # 让系统自动推荐
    
    # 执行占卜
    print("\n🎴 正在为你抽牌... 🎴")
    result = run_tarot_reading(question, spread_type, save_result=True)
    
    if result["success"]:
        display_reading_result(result)
    else:
        print(f"❌ 占卜失败: {result.get('error', '未知错误')}")

def display_reading_result(result):
    """显示占卜结果"""
    print("\n" + "="*60)
    print("🔮 占卜结果 🔮")
    print("="*60)
    
    print(f"📝 问题: {result['question']}")
    print(f"🏷️  类型: {result['question_category']}")
    print(f"🎴 牌阵: {result['spread_name']}")
    print(f"💾 保存: {'成功' if result.get('save_success') else '失败'}")
    
    print(f"\n🎲 抽到的牌:")
    for card in result["drawn_cards"]:
        orientation = "逆位 🔄" if card["reversed"] else "正位 ⬆️"
        print(f"   位置 {card['position']}: {card['name']} ({orientation})")
    
    if result.get("individual_readings"):
        print(f"\n📖 各牌解读:")
        for reading in result["individual_readings"]:
            orientation = "逆位" if reading["reversed"] else "正位"
            print(f"\n   【{reading['position_name']}】{reading['card_name']} ({orientation})")
            print(f"   {reading['reading']}")
    
    print(f"\n🌟 综合解读:")
    print(f"{result['combined_reading']}")
    
    print(f"\n💫 核心信息:")
    print(f"{result['reading_summary']}")
    
    print("\n" + "="*60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="神秘塔罗牌占卜师")
    parser.add_argument("--demo", action="store_true", help="运行演示模式")
    parser.add_argument("--question", "-q", type=str, help="直接进行占卜")
    parser.add_argument("--spread", "-s", type=str, help="指定牌阵类型")
    
    args = parser.parse_args()
    
    if args.demo:
        demo_reading()
    elif args.question:
        result = run_tarot_reading(args.question, args.spread)
        if result["success"]:
            display_reading_result(result)
        else:
            print(f"占卜失败: {result.get('error')}")
    else:
        interactive_reading()

if __name__ == "__main__":
    main()