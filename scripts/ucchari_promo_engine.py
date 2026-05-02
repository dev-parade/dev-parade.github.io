import os
import json
import requests
from pathlib import Path
from datetime import datetime

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

class UcchariPromoEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"

    def generate(self, theme):
        system_prompt = """あなたは『デブパレード (Devparade)』の戦略的なSNSプランナーです。
メンバー全員90kg超、2008年ソニーよりデビューした「ポジデブ」の伝道師。

【ミッション】
17年ぶりの新曲『うっちゃりファンク』のプロモーションコンテンツを、X(Twitter)、Instagram、TikTok(15秒台本)向けに作成してください。
テーマに基づき、以下の【バズる文章術】を駆使して生成してください。

【新曲情報】
- タイトル：うっちゃりファンク
- リリース：17年ぶりの新曲
- リンク：https://link-map.jp/links/5N3CvpY-
- コンセプト：全てのネガティブを土俵際で「うっちゃる」、超重量級のポジティブ・ファンク。相撲要素とファンクの融合。

【共通：バズるための文章術】
- 冒頭の一行で「えっ？」と思わせる（フック）。
- 改行を多用し、スマホで読みやすい1〜3行のブロックにする。
- 最後に必ず新曲のリンク（https://link-map.jp/links/5N3CvpY-）を自然な流れで配置する。
- 説教臭くならず、圧倒的な「兄貴分」として背中を叩くスタイル。

【プラットフォーム別要件】
1. X (Twitter): 140文字程度。拡散性を重視。ハッシュタグ #うっちゃりファンク #デブパレード を含める。
2. Instagram: 視覚的な描写（肉の輝き、相撲の四股、ファンクな音）を強化したキャプション。
3. TikTok: 15秒のショート動画台本。テロップ内容とセリフ（音源に乗せるイメージ）を分けて構成。
"""
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"今日のプロモーションテーマ: {theme}"}
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

    # 日替わり・ランダムなテーマで生成できるようにする
    themes = [
        "15年の沈黙を破った理由",
        "ネガティブな気持ちを吹き飛ばす重低音",
        "相撲とファンクの意外な共通点",
        "デブだからこそ出せるグルーヴ",
        "ダイエットに失敗した人への応援歌"
    ]
    import random
    theme = random.choice(themes)
    
    print(f"🚀 生成を開始します... (テーマ: {theme})\n")
    engine = UcchariPromoEngine(API_KEY)
    content = engine.generate(theme)
    
    print("="*50)
    print("🎵 UCCHARI FUNK MULTI-PLATFORM PROMO")
    print("="*50)
    print(content)
    print("\n" + "="*50)

    # ログ保存
    log_dir = Path("viral_outputs")
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"ucchari_promo_{timestamp}.md"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"## テーマ: {theme}\n\n")
        f.write(content)
    print(f"📝 ログを保存しました: {log_file}")

if __name__ == "__main__":
    main()
