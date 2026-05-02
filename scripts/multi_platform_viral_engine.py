import os
import json
import requests
from pathlib import Path

# .env読み込み
def load_env():
    paths = [Path(".env"), Path("blog-x/.env")]
    for p in paths:
        if p.exists():
            with open(p, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value

load_env()
API_KEY = os.getenv("OPENAI_API_KEY")

class ViralEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"

    def generate(self, topic):
        system_prompt = """あなたは『デブパレード (Devparade)』の戦略的なSNSプランナーです。
メンバー全員90kg超、2008年ソニーよりデビューした「ポジデブ」の伝道師。

【ミッション】
提供されたトピックに基づき、X, Instagram, TikTok(15秒台本)の3つのプラットフォーム向けに、
以下の【バズる文章術】を駆使してコンテンツを生成してください。

【共通：バズるための文章術】
- 冒頭の一行で「えっ？」と思わせる（フック）。
- 改行を多用し、スマホで読みやすい1〜3行のブロックにする。
- 「正論」よりも「強烈な肯定」と「意外な比喩」。
- 最後に肉への情熱やライブの熱量を爆発させる。
- 説教臭くならず、圧倒的な「兄貴分」として背中を叩く。

【プラットフォーム別要件】
1. X (Twitter): 140文字程度。拡散性を重視。
2. Instagram: 視覚的な描写（肉の輝き、音）を強化したキャプション。
3. TikTok: 15秒のショート動画台本。テロップ内容とセリフを分けて構成。
"""
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"トピック: {topic}"}
            ]
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = requests.post(self.url, headers=headers, json=data)
        
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        return f"Error: {resp.status_code}\n{resp.text}"

def main():
    if not API_KEY:
        print("Error: OPENAI_API_KEY not found.")
        return

    topic = input("コンテンツのトピックを入力してください（例：夏と汗、深夜のラーメン、椅子が軋む音）: ")
    engine = ViralEngine(API_KEY)
    
    print("\n🚀 生成を開始します...\n")
    content = engine.generate(topic)
    
    print("="*50)
    print("🍖 DEVPARADE MULTI-PLATFORM VIRAL CONTENT")
    print("="*50)
    print(content)
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
