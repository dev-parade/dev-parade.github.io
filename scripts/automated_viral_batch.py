import os
import json
import time
from multi_platform_viral_engine import ViralEngine, load_env

def run_automated_viral():
    print("🚀 Auto-Viral Multi-Platform Engine 起動")
    
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEYが見つかりません。")
        return
        
    engine = ViralEngine(api_key)
    
    topics_file = os.path.join(os.path.dirname(__file__), "bridged_topics.json")
    if not os.path.exists(topics_file):
        print("❌ bridged_topics.json がありません。先に cross_pollination_sync.py を実行してください。")
        return
        
    with open(topics_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    topics = data.get("note_topics", [])
    if not topics:
        print("⚠️ トピックが空です。")
        return
        
    # 毎日ランダムに1つのトピックを選ぶ（または最新のもの）
    # ここではテストとして最新記事（インデックス0）を使用する
    target_topic = topics[0]
    print(f"🎯 今日の抽出トピック: {target_topic}")
    
    content = engine.generate(target_topic)
    
    # 結果をファイルに保存する
    out_dir = "/Users/coyass/kaihatsu/dev-parade-site/viral_outputs"
    os.makedirs(out_dir, exist_ok=True)
    
    filename = f"viral_draft_{int(time.time())}.txt"
    out_path = os.path.join(out_dir, filename)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ 生成完了: {out_path}")
    print("=" * 50)
    print(content)
    print("=" * 50)

if __name__ == "__main__":
    run_automated_viral()
