import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

# プロジェクトルートを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.content.generator import ContentGenerator
from src.publishers.x_publisher import XPublisher
from dotenv import load_dotenv

def main():
    # .env読み込み（ローカル実行用）
    load_dotenv()
    
    # プロジェクトルートからのパス
    config_path = Path(__file__).parent.parent / "config/settings.yaml"
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 1. コンポーネント初期化
    generator = ContentGenerator(config)
    x_pub = XPublisher(config)
    x_pub.initialize()
    
    # 2. カテゴリの決定（基本は posidev）
    category = "posidev"
    role = "artist"
    
    # 現在の日本時間を取得（GitHub ActionsはUTCなので+9）
    # (または UTC hour に基づいて判定)
    
    print(f"🚀 [Action] Generating content for category: {category}...")
    
    # 3. コンテンツ生成
    post = generator.generate_x_post(category=category, role=role)
    
    if not post:
        print("❌ Generation failed.")
        return

    print(f"📝 Generated Text:\n{post['text']}")
    
    # 4. ドライランチェック
    if os.getenv("DRY_RUN", "true").lower() == "true":
        print("🏃 [DRY RUN] Skipping actual post.")
        return
        
    # 5. X 投稿
    result = x_pub.post_tweet(text=post["text"])
    
    if result:
        print(f"✅ Successfully posted: {result['url']}")
        # 履歴をマーク
        if "hash" in post:
            generator.mark_as_posted(post["hash"])
    else:
        print("❌ Post failed.")

if __name__ == "__main__":
    main()
