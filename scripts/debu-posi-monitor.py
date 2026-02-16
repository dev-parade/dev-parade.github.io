#!/usr/bin/env python3
"""
PosiDev Monitor - ネガデブ発言を検知してポジデブ変換自動返信

方式1: メンションタイムライン監視（@dev_paradeへのリプライに自動返信）
方式2: 検索API（Basic以上のプランが必要）
方式3: フォールバック → Issue生成

Freeプランではメンションタイムライン + 自動投稿で対応。
"""

import os
import sys
import random
import time
import urllib.parse
from datetime import datetime, timezone, timedelta

try:
    import tweepy
except ImportError:
    print("tweepy not installed")
    sys.exit(1)

API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")
LAST_ID_FILE = "last_monitor_id.txt"

MEMBERS = [
    {"name": "ハンサム判治", "role": "Vo.", "weight": "100kg"},
    {"name": "COYASS", "role": "MC", "weight": "93kg"},
    {"name": "ugazin", "role": "Gt.", "weight": "135kg"},
    {"name": "ぺー", "role": "Ba.", "weight": "120kg"},
    {"name": "TAH", "role": "Dr.", "weight": "120kg"},
]

# ===== ポジデブ返信テンプレート =====
RESPONSES = {
    "デブ": [
        "デブ？ ありがとう！総体重570kg超バンドDEV PARADEから言わせてもらうと、それは最高の褒め言葉🍖 #ポジデブ",
        "「デブ」= Delightful Excellent Beautiful。知らなかった？🍖 by DEV PARADE #ポジデブ",
        "デブは才能。俺たち5人で570kg、全員メジャーデビュー済み。才能に体重は関係ない🍖 #ポジデブ",
        "デブをネガティブに捉えないで。俺たちバンド名にデブ入れて誇ってるから🍖 #ポジデブ",
        "デブって呼ばれた？ おめでとう、DEV PARADEの入団資格満たしてるぞ（条件:90kg以上）🍖 #ポジデブ",
    ],
    "太った": [
        "太った？ それは「成長した」って言うんだよ。細胞レベルで進化してる。おめでとう🎉🍖 #ポジデブ",
        "体重が増えた = 存在感が増した。DEV PARADEが保証する🍖 #ポジデブ",
        "太った分だけ地球がお前を離したくないってこと。モテてるぜ、地球に🌍🍖 #ポジデブ",
        "体重増えた？ それは「影響力」のメーター。デカい奴はデカいことができる🍖 #ポジデブ",
    ],
    "痩せ": [
        "痩せる必要？ ないね。俺たち570kgで武道館目指してる。痩せたら夢が軽くなる💪🍖 #ポジデブ",
        "「痩せたい」→「もっと愛されたい」に変換。大丈夫、そのままで最高🍖 #ポジデブ",
        "痩せなくていい。むしろDEV PARADE入らない？条件は90kg以上🍖 #ポジデブ",
        "ダイエットの語源は「生き方」。今の生き方、最高じゃん。変えなくていい🍖 #ポジデブ",
    ],
    "generic": [
        "大丈夫、お前は最高だ。570kg超のバンドが言ってるんだから間違いない🍖 #ポジデブ",
        "デブは個性。個性は武器。武器は磨け🍖 by DEV PARADE #ポジデブ",
        "この世に無駄な脂肪なんてない。全部お前という作品の一部だ🍖 #ポジデブ",
        "どんな悩みも、焼肉食ったら解決する。解決しなくても美味い。それでいい🍖 #ポジデブ",
        "ありがとう！DEV PARADEはあなたを全力で肯定します🍖 #ポジデブ",
        "リプありがとう！570kg超の愛であなたを包む🍖 by DEV PARADE #ポジデブ",
    ],
}

# 検索クエリ（Basic以上で使用）
SEARCH_QUERIES = [
    '"デブ" (辛い OR 悲しい OR 嫌 OR 傷つ OR つらい OR 泣) -is:retweet lang:ja',
    '"太った" (最悪 OR やばい OR ショック OR 泣 OR 嫌) -is:retweet lang:ja',
    '"痩せなきゃ" -is:retweet lang:ja',
    '"痩せろ" (言われ) -is:retweet lang:ja',
    '"デブ" "言われた" -is:retweet lang:ja',
]


def select_response(tweet_text):
    """ツイートの内容に基づいてレスポンスを選択"""
    for kw in ["デブ", "でぶ"]:
        if kw in tweet_text:
            return random.choice(RESPONSES["デブ"])
    for kw in ["太った", "ふとった", "太り"]:
        if kw in tweet_text:
            return random.choice(RESPONSES["太った"])
    for kw in ["痩せ", "やせ"]:
        if kw in tweet_text:
            return random.choice(RESPONSES["痩せ"])
    return random.choice(RESPONSES["generic"])


def get_client():
    """OAuth 1.0a クライアント（読み書き両方）"""
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
        return None
    return tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET,
        wait_on_rate_limit=True,
    )


def get_last_id():
    try:
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_last_id(tweet_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(tweet_id))


def monitor_mentions(client):
    """メンションタイムラインを監視して自動返信"""
    print("\n📡 メンション監視モード")

    try:
        me = client.get_me()
        if not me.data:
            print("❌ ユーザー情報取得失敗")
            return []
        my_id = me.data.id
        my_username = me.data.username
        print(f"   アカウント: @{my_username} (ID: {my_id})")
    except Exception as e:
        print(f"❌ get_me失敗: {e}")
        return []

    last_id = get_last_id()
    found_tweets = []
    auto_replies = []
    newest_id = last_id

    try:
        kwargs = {
            "id": my_id,
            "max_results": 20,
            "tweet_fields": ["created_at", "author_id", "text", "in_reply_to_user_id"],
            "user_fields": ["username"],
            "expansions": ["author_id"],
        }
        if last_id:
            kwargs["since_id"] = last_id

        result = client.get_users_mentions(**kwargs)

        if not result.data:
            print("   新しいメンションなし")
            return []

        users = {}
        if result.includes and "users" in result.includes:
            for user in result.includes["users"]:
                users[user.id] = user.username

        for tweet in result.data:
            username = users.get(tweet.author_id, "unknown")

            # 自分自身のツイートはスキップ
            if username == my_username:
                continue

            response = select_response(tweet.text)
            member = random.choice(MEMBERS)
            reply_text = f"@{username} {response}"

            tweet_data = {
                "id": str(tweet.id),
                "username": username,
                "text": tweet.text,
                "response": response,
                "reply_text": reply_text,
                "member": member,
                "status": "pending",
            }

            # 自動返信
            if len(auto_replies) < 10:
                try:
                    client.create_tweet(
                        text=reply_text,
                        in_reply_to_tweet_id=tweet.id,
                    )
                    tweet_data["status"] = "sent"
                    print(f"   ✅ 自動返信 → @{username}: {response[:50]}...")
                    auto_replies.append(tweet_data)
                    time.sleep(3)
                except Exception as e:
                    print(f"   ❌ 返信失敗: {e}")
                    tweet_data["status"] = f"failed: {e}"

            found_tweets.append(tweet_data)

            # 最新IDを追跡
            if newest_id is None or int(tweet.id) > int(newest_id or 0):
                newest_id = str(tweet.id)

    except tweepy.errors.Forbidden as e:
        print(f"   ⚠️ メンション取得403: {e}")
        print("   → Freeプランではメンション取得も制限される場合があります")
    except Exception as e:
        print(f"   ❌ メンション取得エラー: {e}")

    if newest_id and newest_id != last_id:
        save_last_id(newest_id)

    return found_tweets


def monitor_search(client):
    """検索APIでネガデブ発言を検索（Basic以上のプランが必要）"""
    print("\n🔍 検索監視モード")

    last_id = get_last_id()
    found_tweets = []
    auto_replies = []
    seen_ids = set()
    newest_id = last_id

    for query in SEARCH_QUERIES:
        try:
            kwargs = {
                "query": query,
                "max_results": 10,
                "tweet_fields": ["created_at", "author_id", "text"],
                "user_fields": ["username"],
                "expansions": ["author_id"],
            }
            if last_id:
                kwargs["since_id"] = last_id

            result = client.search_recent_tweets(**kwargs)
            if not result.data:
                continue

            users = {}
            if result.includes and "users" in result.includes:
                for user in result.includes["users"]:
                    users[user.id] = user.username

            for tweet in result.data:
                if tweet.id in seen_ids:
                    continue
                seen_ids.add(tweet.id)

                username = users.get(tweet.author_id, "unknown")
                if username == "dev_parade":
                    continue

                response = select_response(tweet.text)
                member = random.choice(MEMBERS)
                reply_text = f"@{username} {response}"

                tweet_data = {
                    "id": str(tweet.id),
                    "username": username,
                    "text": tweet.text,
                    "response": response,
                    "reply_text": reply_text,
                    "member": member,
                    "status": "pending",
                }

                if len(auto_replies) < 10:
                    try:
                        client.create_tweet(
                            text=reply_text,
                            in_reply_to_tweet_id=tweet.id,
                        )
                        tweet_data["status"] = "sent"
                        print(f"   ✅ 自動返信 → @{username}")
                        auto_replies.append(tweet_data)
                        time.sleep(5)
                    except Exception as e:
                        print(f"   ❌ 返信失敗: {e}")
                        tweet_data["status"] = f"failed: {e}"

                found_tweets.append(tweet_data)

                if newest_id is None or int(tweet.id) > int(newest_id or 0):
                    newest_id = str(tweet.id)

                if len(found_tweets) >= 15:
                    break

        except (tweepy.errors.Forbidden, tweepy.errors.Unauthorized):
            print(f"   ⚠️ 検索API 401/403 → Freeプランでは利用不可。メンション監視に切替。")
            return None  # Noneを返して呼び出し元でメンション監視にフォールバック
        except Exception as e:
            print(f"   検索エラー: {e}")
            return None  # その他エラーもメンション監視にフォールバック

        if len(found_tweets) >= 15:
            break

    if newest_id and newest_id != last_id:
        save_last_id(newest_id)

    return found_tweets


def main():
    print("=" * 50)
    print("🍖 PosiDev Monitor - ネガデブ → ポジデブ変換")
    print("=" * 50)

    client = get_client()
    if not client:
        print("⚠️ API credentials not set")
        generate_sample_issue()
        return

    # まず検索APIを試す → 403なら メンション監視にフォールバック
    found_tweets = monitor_search(client)

    if found_tweets is None:
        # 検索APIが403 → メンション監視で代替
        found_tweets = monitor_mentions(client)

    sent_count = sum(1 for t in found_tweets if t["status"] == "sent")
    print(f"\n📊 結果: {len(found_tweets)}件検知, {sent_count}件自動返信")

    generate_issue(found_tweets, sent_count)
    print("✅ Monitor run complete!")


def generate_issue(tweets, sent_count):
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")

    lines = [
        "## 🍖 ポジデブ変換レポート",
        "",
        f"**検知日時:** {now}",
        f"**検知数:** {len(tweets)}件",
        f"**自動返信:** {sent_count}件",
        "",
        "---",
        "",
    ]

    if not tweets:
        lines.append("*新しいメンション・ネガデブ発言はありませんでした。平和！🍖*")
    else:
        for i, t in enumerate(tweets, 1):
            intent_url = f"https://twitter.com/intent/tweet?in_reply_to={t['id']}&text={urllib.parse.quote(t['reply_text'])}"
            tweet_url = f"https://twitter.com/{t['username']}/status/{t['id']}"

            status_emoji = "✅" if t["status"] == "sent" else "👉"
            status_text = "自動返信済み" if t["status"] == "sent" else "未返信"

            lines.append(f"### #{i} {status_emoji} {status_text}")
            lines.append(f"**元ツイート** by @{t['username']}:")
            lines.append(f"> {t['text'][:200]}")
            lines.append(f"")
            lines.append(f"**ポジデブ返信** ({t['member']['name']} {t['member']['role']}):")
            lines.append(f"```")
            lines.append(f"{t['reply_text']}")
            lines.append(f"```")

            if t["status"] != "sent":
                lines.append(f"")
                lines.append(f"**[👉 ワンクリック返信]({intent_url})** | [元ツイート]({tweet_url})")

            lines.append(f"")
            lines.append(f"---")
            lines.append(f"")

    lines.append("*Powered by DEV PARADE ポジデブBot 🍖*")

    with open("monitor_issue.md", "w") as f:
        f.write("\n".join(lines))

    print("✅ Issue markdown generated!")


def generate_sample_issue():
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")
    sample = f"""## 🍖 ポジデブ変換レポート

**検知日時:** {now}
**ステータス:** ⚠️ API credentials未設定

GitHub Secretsに以下を設定してください:
- `X_API_KEY` / `X_API_SECRET`
- `X_ACCESS_TOKEN` / `X_ACCESS_SECRET`

---
*Powered by DEV PARADE ポジデブBot 🍖*
"""
    with open("monitor_issue.md", "w") as f:
        f.write(sample)


if __name__ == "__main__":
    main()
