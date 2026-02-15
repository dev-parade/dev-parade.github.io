#!/usr/bin/env python3
"""
DebuPosi Bot - DEV PARADE 公式デブポジティブ変換Bot

SNS上の「デブ」「太った」「痩せろ」等のネガティブ発言を検知し、
DEV PARADEメンバーとしてポジティブなリプライを自動送信する。

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
    '"デブ" -is:retweet -is:reply lang:ja',
    '"太った" -is:retweet -is:reply lang:ja',
    '"痩せなきゃ" -is:retweet -is:reply lang:ja',
    '"痩せろ" -is:retweet -is:reply lang:ja',
    '"メタボ" -is:retweet -is:reply lang:ja',
    '"ぽっちゃり" -is:retweet -is:reply lang:ja',
    '"体重増えた" -is:retweet -is:reply lang:ja',
]

# ===== DEV PARADE MEMBERS =====
MEMBERS = [
    {"name": "ハンサム判治", "role": "Vo.", "weight": "100kg"},
    {"name": "COYASS", "role": "MC", "weight": "93kg"},
    {"name": "ugazin", "role": "Gt.", "weight": "135kg"},
    {"name": "ぺー", "role": "Ba.", "weight": "120kg"},
    {"name": "TAH", "role": "Dr.", "weight": "120kg"},
]

# ===== ポジティブレスポンスDB =====
RESPONSES = {
    "デブ": [
        "デブ？ ありがとう！🍖 総体重570kg超のバンドDEV PARADEから言わせてもらうと、それは最高の褒め言葉。#デブポジ #DEVPARADE",
        "「デブ」= Delightful Excellent Beautiful の略。知らなかった？ 🍖 by DEV PARADE #デブポジ",
        "デブは才能。俺たち5人で570kg、全員メジャーデビュー済み。才能に体重は関係ない。🍖 #デブポジ #DEVPARADE",
        "デブって呼ばれた？ おめでとう、DEV PARADEの入団資格を満たしてます（条件:90kg以上）🍖 #デブポジ",
        "デブは誇り。バンド名にDEV（デブ）入れてるくらい。リスペクト。🍖 by DEV PARADE #デブポジ",
    ],
    "太った": [
        "太った？ それは「成長した」って言うんだよ。細胞レベルで進化してる。おめでとう！🎉🍖 by DEV PARADE #デブポジ",
        "体重が増えた = 存在感が増した。ステージ映えするってこと。DEV PARADEが保証する。🍖 #デブポジ",
        "太った分だけ、地球がお前を離したくないってこと。モテてるぜ、地球に。🌍🍖 #デブポジ #DEVPARADE",
        "体重計の数字が増えた？ それは「影響力」のメーター。デカい奴はデカいことができる。🍖 #デブポジ",
    ],
    "痩せ": [
        "痩せる必要？ ないね。俺たち570kgで武道館目指してる。痩せたら夢が軽くなる。💪🍖 #デブポジ #DEVPARADE",
        "「痩せたい」を「もっと愛されたい」に変換。大丈夫、デブは愛される才能。🍖 by DEV PARADE #デブポジ",
        "痩せなくていい。むしろDEV PARADE入らない？条件は90kg以上。🍖 #デブポジ #DEVPARADE",
        "ダイエットの語源は\"生き方\"。今の生き方、最高じゃん。変えなくていい。🍖 #デブポジ",
    ],
    "メタボ": [
        "メタボ？ メタル＋ボディの略でしょ？ ロックな体型認定おめでとう！🤘🍖 by DEV PARADE #デブポジ",
        "俺たち自称「ヘヴィメタボバンド」。メタボは音楽ジャンル。🍖 #デブポジ #DEVPARADE",
        "メタボ判定 = ロック認定。DEV PARADEはメタボバンドとして15年やってます。🍖 #デブポジ",
    ],
    "ぽっちゃり": [
        "ぽっちゃり？ それは「やわらかい魅力がある」の同義語。🍖 by DEV PARADE #デブポジ",
        "ぽっちゃりは最高のボディタイプ。包容力がハンパない。DEV PARADEメンバー全員が証人。🍖 #デブポジ",
    ],
    "体重": [
        "体重の話？ 俺たち5人で570kg超。重さは力。重さは存在感。🍖 by DEV PARADE #デブポジ",
        "体重と幸福度は比例する（DEV PARADE調べ）。お前、幸せだろ？🍖 #デブポジ #DEVPARADE",
    ],
    "generic": [
        "どんな悩みも、焼肉食ったら解決する。解決しなくても、美味い。それでいい。🍖 by DEV PARADE #デブポジ",
        "大丈夫、お前は最高だ。570kg超のバンドが言ってるんだから間違いない。🍖 #デブポジ #DEVPARADE",
        "ネガティブな言葉は俺たちの腹の肉で全部吸収してやる。🍖 by DEV PARADE #デブポジ",
        "この世に無駄な脂肪なんてない。全部お前という作品の一部。🍖 #デブポジ #DEVPARADE",
        "デブは個性。個性は武器。武器は磨け。🍖 by DEV PARADE #デブポジ",
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


def get_ai_response(tweet_text):
    """Claude APIでカスタムレスポンスを生成（オプション）"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=280,
            messages=[{
                "role": "user",
                "content": f"""あなたはDEV PARADE（デブパレード）の公式Botです。総体重570kg超のヘヴィメタボバンド。
メンバー全員90kg以上で、デブをポジティブに捉えています。

以下のツイートに対して、デブをポジティブに肯定するリプライを1つだけ書いてください。

条件:
- 280文字以内（日本語）
- ユーモアと温かさを込める
- 「デブは才能」「脂肪は努力の結晶」的なポジティブ変換
- 最後に 🍖 と #デブポジ #DEVPARADE を付ける
- 相手を傷つけない、上から目線にならない
- 押し付けがましくない

ツイート: {tweet_text}"""
            }],
        )
        return message.content[0].text
    except Exception as e:
        print(f"AI response failed: {e}")
        return None


def select_response(tweet_text):
    """ツイートの内容に基づいてレスポンスを選択"""
    # まずAIレスポンスを試す
    ai_resp = get_ai_response(tweet_text)
    if ai_resp:
        return ai_resp

    # キーワードマッチでレスポンス選択
    text_lower = tweet_text.lower()
    for keyword, resps in RESPONSES.items():
        if keyword == "generic":
            continue
        if keyword in text_lower:
            return random.choice(resps)

    return random.choice(RESPONSES["generic"])


def select_member():
    """ランダムにメンバーを選択"""
    return random.choice(MEMBERS)


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
    print("🍖 DebuPosi Bot - DEV PARADE")
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
    log = """## 🍖 DebuPosi Bot 実行ログ

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
| デブって言われた | デブは才能。俺たち570kgで全員メジャーデビュー済み。🍖 | ハンサム判治 |
| 痩せなきゃ... | 痩せる必要？ ないね。痩せたら夢が軽くなる。🍖 | ugazin |
"""
    with open("bot_log.md", "w") as f:
        f.write(log)


def generate_log(entries, count):
    """実行ログをMarkdownで生成"""
    mode = "DRY RUN" if DRY_RUN else "LIVE"
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")

    lines = [
        f"## 🍖 DebuPosi Bot 実行ログ",
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
    lines.append(f"Powered by DEV PARADE デブポジBot 🍖")

    with open("bot_log.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
