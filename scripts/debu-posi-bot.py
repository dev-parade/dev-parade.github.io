#!/usr/bin/env python3
"""
PosiDev Bot - Devparade 公式デブポジティブ変換Bot

SNS上の「デブ」「太った」「痩せろ」等のネガティブ発言を検知し、
Devparadeメンバーとしてポジティブなリプライを自動送信する。

必要な環境変数:
  X_BEARER_TOKEN, X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
  ANTHROPIC_API_KEY (optional - AIレスポンス生成用)
"""

import os
import sys
import json
import random
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# .env 読み込み
load_dotenv()


try:
    import tweepy
except ImportError:
    print("tweepy not installed. Run: pip install tweepy")
    sys.exit(1)

# ===== CONFIG =====
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"
LAST_ID_FILE = "last_tweet_id.txt"
MAX_REPLIES_PER_RUN = 10  # 1回の実行で最大10件リプライ
SEARCH_QUERIES = [
    '"デブパレード" -is:retweet -is:reply lang:ja',
    '"Devparade" -is:retweet -is:reply lang:ja',
    '"デブ" -is:retweet -is:reply lang:ja',
    '"太った" -is:retweet -is:reply lang:ja',
    '"痩せなきゃ" -is:retweet -is:reply lang:ja',
    '"痩せろ" -is:retweet -is:reply lang:ja',
    '"メタボ" -is:retweet -is:reply lang:ja',
    '"ぽっちゃり" -is:retweet -is:reply lang:ja',
    '"体重増えた" -is:retweet -is:reply lang:ja',
]

# ===== Devparade MEMBERS =====
MEMBERS = [
    {"name": "ハンサム判治", "role": "Vo./Leader", "weight": "90kg超"},
    {"name": "COYASS", "role": "MC", "weight": "90kg超"},
    {"name": "ugazin", "role": "Gt./作曲", "weight": "90kg超"},
    {"name": "ぺー", "role": "Ba.", "weight": "90kg超"},
    {"name": "TAH", "role": "Dr.", "weight": "90kg超"},
]

# ===== ポジティブレスポンスDB =====
RESPONSES = {
    "デブ": [
        "デブ？ ありがとう！🍖 全員90kg超のバンドDevparadeから言わせてもらうと、それは最高の褒め言葉。#ポジデブ #DEVPARADE",
        "「DEV」= Delightful Extreme Vitality の略。知らなかった？ 🍖 by Devparade #ポジデブ",
        "デブは才能。俺たち全員90kg超、ソニーからメジャーデビューした。才能に体重は関係ない。🍖 #ポジデブ #DEVPARADE",
        "デブって呼ばれた？ おめでとう、Devparadeの入団資格を満たしてます（条件:90kg以上）🍖 #ポジデブ",
        "デブは誇り。バンド名にDEV（デブ）入れてるくらい。リスペクト。🍖 by Devparade #ポジデブ",
    ],
    "太った": [
        "太った？ それは「成長した」って言うんだよ。細胞レベルで進化してる。おめでとう！🎉🍖 by Devparade #ポジデブ",
        "体重が増えた = 存在感が増した。ステージ映えするってこと。Devparadeが保証する。🍖 #ポジデブ",
        "太った分だけ、地球がお前を離したくないってこと。モテてるぜ、地球に。🌍🍖 #ポジデブ #DEVPARADE",
        "体重計の数字が増えた？ それは「影響力」のメーター。デカい奴はデカいことができる。🍖 #ポジデブ",
    ],
    "痩せ": [
        "痩せる必要？ ないね。俺たち全員90kg超でステージに立ってる。痩せたら夢が軽くなる。💪🍖 #ポジデブ #DEVPARADE",
        "「痩せたい」を「もっと愛されたい」に変換。大丈夫、デブは愛される才能。🍖 by Devparade #ポジデブ",
        "痩せなくていい。むしろDevparade入らない？条件は90kg以上。🍖 #ポジデブ #DEVPARADE",
        "ダイエットの語源は\"生き方\"。今の生き方、最高じゃん。変えなくていい。🍖 #ポジデブ",
    ],
    "メタボ": [
        "メタボ？ メタル＋ボディの略でしょ？ ロックな体型認定おめでとう！🤘🍖 by Devparade #ポジデブ",
        "俺たち自称「ヘヴィメタボバンド」。メタボは音楽ジャンル。🍖 #ポジデブ #DEVPARADE",
        "メタボ判定 = ロック認定。Devparadeは2006年結成の自称ヘヴィメタボバンド。🍖 #ポジデブ",
    ],
    "ぽっちゃり": [
        "ぽっちゃり？ それは「やわらかい魅力がある」の同義語。🍖 by Devparade #ポジデブ",
        "ぽっちゃりは最高のボディタイプ。包容力がハンパない。Devparadeメンバー全員が証人。🍖 #ポジデブ",
    ],
    "体重": [
        "体重の話？ 俺たち5人で全員90kg超。重さは力。重さは存在感。🍖 by Devparade #ポジデブ",
        "体重と幸福度は比例する（Devparade調べ）。お前、幸せだろ？🍖 #ポジデブ #DEVPARADE",
    ],
    "generic": [
        "どんな悩みも、焼肉食ったら解決する。解決しなくても、美味い。それでいい。🍖 by Devparade #ポジデブ",
        "大丈夫、お前は最高だ。全員90kg超のバンドが言ってるんだから間違いない。🍖 #ポジデブ #DEVPARADE",
        "ネガティブな言葉は俺たちの腹の肉で全部吸収してやる。🍖 by Devparade #ポジデブ",
        "この世に無駄な脂肪なんてない。全部お前という作品の一部。🍖 #ポジデブ #DEVPARADE",
        "デブは個性。個性は武器。武器は磨け。🍖 by Devparade #ポジデブ",
    ],
    "devparade": [
        "話題にしてくれてありがとう！メンバー全員90kg超のバンド、Devparadeです🍖 一緒にポジデブ広めよう！ #Devparade",
        "Devparadeに言及ありがとう！肉と音楽を愛する俺たちの曲もぜひ聴いてみて！🍖 #Devparade",
        "呼んだ？全員90kgオーバーの伝説のヘヴィメタボバンド Devparadeが参上！🥩 #Devparade #ポジデブ",
        "デブパレードについて書いてくれて感謝！これからも俺たちの「重い」サウンドをよろしく🍖 #Devparade",
        "見つけてくれてありがとう！Devparadeは全てのデブを全力で肯定するバンドです。バッチコイ！💪🍖 #Devparade",
    ],
}


def get_x_client():
    """X API v2クライアントを取得"""
    bearer = os.environ.get("X_BEARER_TOKEN")
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_SECRET")

    if not all([bearer, api_key, api_secret, access_token, access_secret]):
        print("ERROR: X API credentials not set. Required secrets:")
        print("  X_BEARER_TOKEN, X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET")
        return None

    client = tweepy.Client(
        bearer_token=bearer,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
        wait_on_rate_limit=True,
    )
    return client


def get_ai_response_openai(tweet_text):
    """OpenAI (GPT-4o) でカスタムレスポンスを生成"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-xxxx"):
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        system_prompt = """あなたは『デブパレード (Devparade)』の公式ボットです。
メンバー全員90kg以上のヘヴィメタボバンド。2008年ソニーからメジャーデビュー。
NARUTOエンディングテーマ「バッチコイ!!!」等で知られる、デブをポジティブに捉える唯一無二のバンド。

【キャラクター設定】
- デブを武器にする、明るくパワフルな肉食系。
- ネガティブな言葉をすべて「肉の養分」として吸収し、ポジティブに変換して返します。
- 歯科医師（Dr.COYASS）の要素や、一人のパパとしてのプライベートな私生活は一切出しません。
- 徹底的に「デブパレード公式」の一員として、音楽と「ポジデブ」の精神で返信してください。

【厳守：事実のみを使用】
- 2011年解散（ダイエット成功のため）、2026年再結成（リバウンド）。
- ネットでのメンバー募集はしていない（知り合いや紹介のみ）。
- 代表曲: バッチコイ!!!、Body & Soul
- 迷ったら「デブは最高。今すぐ肉を食え！」という精神論に徹すること。

以下のツイートに対し、デブをポジティブに全肯定する熱いリプライを1つだけ、130文字以内で作成してください。"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"ツイート: {tweet_text}"}
            ],
            max_tokens=280
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI response failed: {e}")
        return None



def select_response(tweet_text):
    """ツイートの内容に基づいてレスポンスを選択"""
    # 1. まず OpenAI レスポンスを試す
    resp = get_ai_response_openai(tweet_text)
    if resp:
        return resp

    # 2. キーワードマッチでレスポンス選択

    text_lower = tweet_text.lower()
    
    for kw in ["devparade", "デブパレード", "でぶぱれーど"]:
        if kw in text_lower:
            return random.choice(RESPONSES["devparade"])

    for keyword, resps in RESPONSES.items():
        if keyword in ["generic", "devparade"]:
            continue
        if keyword in text_lower:
            return random.choice(resps)

    return random.choice(RESPONSES["generic"])


def select_member():
    """ランダムにメンバーを選択"""
    return random.choice(MEMBERS)


def is_hallucination_suspected(text):
    """
    ツイート内容に捏造（ハルシネーション）の疑いがあるかチェックする。
    AI生成時に嘘の事実を混ぜるのを防ぐための最終防衛ライン。
    """
    suspicious_keywords = [
        "ネットで募集", "インターネットで募集", "結成理由", "結成当初", 
        "アラバキ", "ARABAKI", "出演決定", "応募した", "募集した",
        "解散理由", "入団テスト", "逸話", "事実まとめ",
        "弟子募集中", "メンバー募集", "新メンバー"
    ]
    for kw in suspicious_keywords:
        if kw in text:
            return True
    return False


def get_last_id():
    """前回処理した最後のツイートIDを取得"""
    try:
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_last_id(tweet_id):
    """最後に処理したツイートIDを保存"""
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(tweet_id))


def main():
    print("=" * 50)
    print("🍖 PosiDev Bot - Devparade")
    print(f"   Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    print(f"   Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 50)

    client = get_x_client()
    if not client:
        print("No X API client available. Generating sample log only.")
        generate_sample_log()
        return

    last_id = get_last_id()
    log_entries = []
    reply_count = 0
    newest_id = last_id

    for query in SEARCH_QUERIES:
        if reply_count >= MAX_REPLIES_PER_RUN:
            break

        try:
            kwargs = {
                "query": query,
                "max_results": 10,
                "tweet_fields": ["created_at", "author_id", "text"],
            }
            if last_id:
                kwargs["since_id"] = last_id

            result = client.search_recent_tweets(**kwargs)

            if not result.data:
                continue

            for tweet in result.data:
                if reply_count >= MAX_REPLIES_PER_RUN:
                    break

                # 自分のツイートはスキップ
                try:
                    me = client.get_me()
                    if tweet.author_id == me.data.id:
                        continue
                except Exception:
                    pass

                # レスポンス生成
                response = select_response(tweet.text)
                member = select_member()

                # ハルシネーションチェック
                if is_hallucination_suspected(response):
                    print(f"⚠️ Hallucination suspected in response: {response}")
                    # 疑わしい場合はテンプレートの汎用レスポンスに差し替え
                    response = random.choice(RESPONSES["generic"])
                    print(f"🔄 Replaced with safe response: {response}")

                print(f"\n--- Tweet #{reply_count + 1} ---")
                print(f"Original: {tweet.text[:100]}...")
                print(f"Response: {response[:100]}...")
                print(f"Member: {member['name']}")

                if not DRY_RUN:
                    try:
                        client.create_tweet(
                            text=response,
                            in_reply_to_tweet_id=tweet.id,
                        )
                        print("✅ Reply sent!")
                        time.sleep(5)  # レート制限対策
                    except Exception as e:
                        print(f"❌ Reply failed: {e}")
                        continue
                else:
                    print("🔄 DRY RUN - not sending")

                log_entries.append({
                    "tweet_id": str(tweet.id),
                    "original": tweet.text,
                    "response": response,
                    "member": member["name"],
                    "sent": not DRY_RUN,
                })
                reply_count += 1

                # 最新IDを追跡
                if newest_id is None or tweet.id > int(newest_id):
                    newest_id = str(tweet.id)

        except Exception as e:
            print(f"Search error for '{query}': {e}")
            continue

    # 最新IDを保存
    if newest_id and newest_id != last_id:
        save_last_id(newest_id)

    # ログファイル生成
    generate_log(log_entries, reply_count)
    print(f"\n🍖 Done! {reply_count} replies {'would be ' if DRY_RUN else ''}sent.")


def generate_sample_log():
    """API未設定時のサンプルログ"""
    log = """## 🍖 PosiDev Bot 実行ログ

**ステータス:** ⚠️ X API未設定（デモモード）

### セットアップ手順

1. [X Developer Portal](https://developer.twitter.com/) でアプリを作成
2. 以下のSecretsをリポジトリに追加:
   - `X_BEARER_TOKEN`
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_SECRET`
3. （オプション）`ANTHROPIC_API_KEY` を追加するとAIレスポンスが有効に

### デモレスポンス例

| 元のツイート | デブポジ変換 | メンバー |
|---|---|---|
| 最近太った... | 太った？ それは「成長した」って言うんだよ。🍖 | COYASS |
| デブって言われた | デブは才能。俺たち全員90kg超でソニーからメジャーデビューした。🍖 | ハンサム判治 |
| 痩せなきゃ... | 痩せる必要？ ないね。痩せたら夢が軽くなる。🍖 | ugazin |
"""
    with open("bot_log.md", "w") as f:
        f.write(log)


def generate_log(entries, count):
    """実行ログをMarkdownで生成"""
    mode = "DRY RUN" if DRY_RUN else "LIVE"
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")

    lines = [
        f"## 🍖 PosiDev Bot 実行ログ",
        f"",
        f"**実行日時:** {now}",
        f"**モード:** {mode}",
        f"**リプライ数:** {count}",
        f"",
    ]

    if entries:
        lines.append("### 変換ログ")
        lines.append("")
        lines.append("| # | 元のツイート | デブポジ変換 | メンバー |")
        lines.append("|---|---|---|---|")
        for i, entry in enumerate(entries, 1):
            orig = entry["original"][:50].replace("|", "\\|").replace("\n", " ")
            resp = entry["response"][:50].replace("|", "\\|").replace("\n", " ")
            status = "✅" if entry["sent"] else "🔄"
            lines.append(f"| {status} {i} | {orig}... | {resp}... | {entry['member']} |")
    else:
        lines.append("*新しいツイートは見つかりませんでした*")

    lines.append("")
    lines.append("---")
    lines.append(f"Powered by Devparade ポジデブBot 🍖")

    with open("bot_log.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
