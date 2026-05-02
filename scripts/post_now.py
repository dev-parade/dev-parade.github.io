import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートなどをパスに追加
blog_x_path = Path(__file__).parent.parent / "blog-x"
sys.path.insert(0, str(blog_x_path))

from src.content.generator import ContentGenerator
from src.publishers.x_publisher import XPublisher

async def main():
    load_dotenv()
    
    config_path = blog_x_path / "config/settings.yaml"
    import yaml
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 認証情報の取得（フォールバック付き）
    api_key = os.getenv("X_API_KEY") or os.getenv("API_KEY")
    api_secret = os.getenv("X_API_SECRET") or os.getenv("API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN") or os.getenv("ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_TOKEN_SECRET") or os.getenv("X_ACCESS_SECRET") or os.getenv("ACCESS_SECRET")

    # 本番モード（dry_runを無視して投稿）
    config["app"]["dry_run"] = False
    
    generator = ContentGenerator(config)
    x_pub = XPublisher(config)
    
    if not x_pub.initialize():
        print("❌ X API initialization failed.")
        sys.exit(1)
    
    category = "posidev"
    # --- 誤投稿防止ロック (再度確認) ---
    if x_pub.username.lower() == "coyass":
        print("❌ ERROR: Safety lock triggered! These keys belong to @COYASS.")
        print("❌ Aborting to prevent personal account posting.")
        sys.exit(1)
    
    print(f"👤 Authenticated as: @{x_pub.username}")

    print(f"🚀 Generating and posting for category: {category}...")
    
    post = generator.generate_x_post(category=category)
    
    # 投稿前のクリーンアップ（メタデータヘッダーを徹底的に削除）
    # 最後の '---' より後の部分を本文として採用する
    full_text = post['text']
    if "---" in full_text:
        post_text = full_text.split("---")[-1].strip()
    else:
        # '---' がない場合は 'category:' 行を削除
        post_text = "\n".join([line for line in full_text.splitlines() if not line.startswith("category:")]).strip()
    
    if post:
        print(f"📝 Post Content: \n{post_text}\n")
        result = x_pub.post_tweet(text=post_text)
        if result:
            print(f"✅ Successfully posted to X: {result['url']}")
            # 履歴を更新（重複防止用）
            if "hash" in post:
                generator.mark_as_posted(post["hash"])
        else:
            print("❌ Failed to post to X.")
    else:
        print("❌ Failed to generate content.")

if __name__ == "__main__":
    asyncio.run(main())
