import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# .env を読み込み
load_dotenv(Path.cwd() / "blog-x" / ".env")


# blog-x ディレクトリをパスに追加
sys.path.append(str(Path.cwd() / "blog-x"))

from src.content.generator import ContentGenerator
import yaml

def test_persona_separation():
    with open("blog-x/config/settings.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    generator = ContentGenerator(config)
    
    roles = ["doctor", "artist", "personal"]
    
    print("--- Persona Separation Test ---")
    for role in roles:
        print(f"\n[Testing Role: {role}]")
        # X投稿のテスト生成
        post = generator.generate_x_post(category="daily_doc", role=role)
        if post:
            print(f"Generated text: {post['text']}")
            print(f"Used Role: {post['role']}")
        else:
            print("Failed to generate post.")

if __name__ == "__main__":
    test_persona_separation()
