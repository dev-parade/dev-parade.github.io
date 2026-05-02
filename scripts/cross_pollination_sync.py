import os
import json
import random
from pathlib import Path

def sync_note_topics():
    print("🔄 クロスポリネーション同期（Note → DevParade）を開始します...")
    
    # Note自動化システムのPIPELINE_STATE.jsonパス
    note_pipeline_path = "/Users/coyass/kaihatsu/note jidou/PIPELINE_STATE.json"
    
    if not os.path.exists(note_pipeline_path):
        print(f"❌ Error: {note_pipeline_path} が見つかりません。")
        return
        
    with open(note_pipeline_path, "r", encoding="utf-8") as f:
        pipeline = json.load(f)
        
    posted_articles = pipeline.get("posted_articles", [])
    if not posted_articles:
        print("⚠️ 投稿済みの記事がありません。")
        return
        
    # 最新の無料・有料記事のタイトルを抽出
    topics = []
    for article in reversed(posted_articles[-30:]):  # 最新30件から
        title = article.get("title", "")
        # シンプルなトピックテキストに変換
        topic_text = f"歯科医師・バイオハッカーDr.COYASSが提唱する「{title}」について"
        topics.append(topic_text)
        
    # 現在のスクリプトディレクトリ（dev-parade-site/scripts）
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(out_dir, "bridged_topics.json")
    
    # 取得した最新トピックリストを保存
    output_data = {
        "sync_date": "2026-04-23", # 現行稼働日の記録として
        "note_topics": topics
    }
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ 同期完了! {len(topics)}件のトピックを bridged_topics.json に保存しました。")

if __name__ == "__main__":
    sync_note_topics()
