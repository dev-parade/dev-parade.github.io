#!/usr/bin/env python3
"""
PosiDev Free Search - 無料でネガデブツイートを検索 & ポジデブ自動返信

X API Freeプランでは検索APIが使えない（$100/月のBasicが必要）。
そこで以下の無料手法でネガデブツイートを発見し、X APIで自動返信する:

方式1: Google検索 (site:x.com "デブ" "辛い") → ツイートURL取得 → 返信
方式2: メンション監視 (@dev_paradeへの返信を自動返信)
方式3: ハッシュタグ監視 (#ポジデブ / #デブ / #太った)

※ X APIの投稿機能はFreeプランでも使える
"""

import os
import sys
import re
import json
import random
import time
import urllib.parse
from datetime import datetime, timezone, timedelta

try:
    import tweepy
except ImportError:
    print("tweepy not installed")
    sys.exit(1)

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False

API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")

FOUND_IDS_FILE = "replied_tweet_ids.json"
LAST_MENTION_ID_FILE = "last_monitor_id.txt"

MEMBERS = [
    {"name": "ハンサム判治", "role": "Vo.", "weight": "100kg"},
    {"name": "COYASS", "role": "MC", "weight": "93kg"},
    {"name": "ugazin", "role": "Gt.", "weight": "135kg"},
    {"name": "ぺー", "role": "Ba.", "weight": "120kg"},
    {"name": "TAH", "role": "Dr.", "weight": "120kg"},
]

# キーワードDBをインポート
from posideb_keywords import ALL_GOOGLE_QUERIES as GOOGLE_QUERIES_ALL
from posideb_keywords import select_response


def get_write_client():
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
        return None
    return tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET,
        wait_on_rate_limit=True,
    )


def get_read_client():
    if BEARER_TOKEN:
        return tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
    return get_write_client()


def load_replied_ids():
    try:
        with open(FOUND_IDS_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_replied_ids(ids):
    # 最新500件のみ保持
    ids_list = list(ids)[-500:]
    with open(FOUND_IDS_FILE, "w") as f:
        json.dump(ids_list, f)


def get_last_mention_id():
    try:
        with open(LAST_MENTION_ID_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_last_mention_id(tweet_id):
    with open(LAST_MENTION_ID_FILE, "w") as f:
        f.write(str(tweet_id))


# ===== 方式1: Google検索でツイートを発見 =====
def search_google_for_tweets():
    """Google検索でネガデブツイートのURLを取得"""
    if not HAS_SCRAPER:
        print("   ⚠️ requests/beautifulsoup4 未インストール")
        return []

    found_tweet_ids = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ja,en;q=0.9",
    }

    # ランダムに2クエリだけ実行（レート制限回避）
    queries = random.sample(GOOGLE_QUERIES_ALL, min(2, len(GOOGLE_QUERIES_ALL)))

    for query in queries:
        try:
            # Google検索（直近24時間: tbs=qdr:d）
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbs=qdr:d&num=10"
            print(f"   🔍 Google: {query[:50]}...")

            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                print(f"   ⚠️ Google応答: {resp.status_code}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # Google検索結果からx.com/twitter.comのURLを抽出
            for link in soup.find_all("a", href=True):
                href = link["href"]
                # Google結果のURLパターン
                match = re.search(r'(?:x\.com|twitter\.com)/(\w+)/status/(\d+)', href)
                if match:
                    username = match.group(1)
                    tweet_id = match.group(2)
                    if username not in ("dev_parade", "i", "search", "hashtag"):
                        found_tweet_ids.append({
                            "id": tweet_id,
                            "username": username,
                            "source": "google",
                        })
                        print(f"   📌 発見: @{username}/status/{tweet_id}")

            time.sleep(2)  # Google レート制限回避

        except Exception as e:
            print(f"   ❌ Google検索エラー: {e}")
            continue

    return found_tweet_ids


# ===== 方式2: メンション監視 =====
def check_mentions(read_client, write_client):
    """@dev_paradeへのメンションを監視"""
    results = []

    try:
        me = write_client.get_me()
        if not me.data:
            return []
        my_id = me.data.id
        my_username = me.data.username

        last_id = get_last_mention_id()
        kwargs = {
            "id": my_id,
            "max_results": 20,
            "tweet_fields": ["created_at", "author_id", "text"],
            "user_fields": ["username"],
            "expansions": ["author_id"],
        }
        if last_id:
            kwargs["since_id"] = last_id

        result = read_client.get_users_mentions(**kwargs)
        if not result.data:
            print("   メンションなし")
            return []

        users = {}
        if result.includes and "users" in result.includes:
            for user in result.includes["users"]:
                users[user.id] = user.username

        newest_id = last_id
        for tweet in result.data:
            username = users.get(tweet.author_id, "unknown")
            if username == my_username:
                continue

            results.append({
                "id": str(tweet.id),
                "username": username,
                "text": tweet.text,
                "source": "mention",
            })
            print(f"   📩 メンション: @{username}")

            if newest_id is None or int(tweet.id) > int(newest_id or 0):
                newest_id = str(tweet.id)

        if newest_id and newest_id != last_id:
            save_last_mention_id(newest_id)

    except Exception as e:
        print(f"   ⚠️ メンション取得: {e}")

    return results


# ===== ツイート詳細取得 & 返信 =====
def reply_to_tweets(write_client, read_client, tweet_targets, replied_ids):
    """発見したツイートにポジデブ返信"""
    results = []
    reply_count = 0

    for target in tweet_targets:
        if reply_count >= 5:  # 1回の実行で最大5件
            break

        tweet_id = target["id"]
        if tweet_id in replied_ids:
            print(f"   ⏭️ 返信済みスキップ: {tweet_id}")
            continue

        username = target["username"]
        tweet_text = target.get("text", "")

        # Google経由の場合、ツイート本文がないのでAPIで取得を試みる
        if not tweet_text and read_client:
            try:
                tweet_data = read_client.get_tweet(tweet_id, tweet_fields=["text"])
                if tweet_data.data:
                    tweet_text = tweet_data.data.text
            except Exception:
                tweet_text = ""

        response = select_response(tweet_text or "デブ")
        member = random.choice(MEMBERS)
        reply_text = f"@{username} {response}"

        result = {
            "id": tweet_id,
            "username": username,
            "text": tweet_text[:100] if tweet_text else "(Google検索で発見)",
            "response": response,
            "member": member,
            "status": "pending",
            "source": target.get("source", "unknown"),
        }

        try:
            write_client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet_id,
            )
            result["status"] = "sent"
            replied_ids.add(tweet_id)
            reply_count += 1
            print(f"   ✅ ポジデブ返信 → @{username}: {response[:40]}...")
            time.sleep(3)
        except tweepy.errors.Forbidden as e:
            error_msg = str(e)
            if "duplicate" in error_msg.lower():
                print(f"   ⏭️ 重複スキップ: @{username}")
                replied_ids.add(tweet_id)
            else:
                print(f"   ❌ 返信失敗(403): {e}")
            result["status"] = f"failed: {e}"
        except tweepy.errors.NotFound:
            print(f"   ⏭️ ツイート削除済み: {tweet_id}")
            replied_ids.add(tweet_id)
            result["status"] = "deleted"
        except Exception as e:
            print(f"   ❌ 返信失敗: {e}")
            result["status"] = f"failed: {e}"

        results.append(result)

    return results


def main():
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    hour = now.hour

    # 時間帯に応じたメッセージ
    if 6 <= hour < 10:
        time_label = "🌅 朝のポジデブ"
    elif 11 <= hour < 14:
        time_label = "☀️ 昼のポジデブ"
    else:
        time_label = "🌙 夜のポジデブ"

    print("=" * 50)
    print(f"🍖 PosiDev Free Search - {time_label}")
    print(f"   {now.strftime('%Y-%m-%d %H:%M JST')}")
    print("=" * 50)

    write_client = get_write_client()
    read_client = get_read_client()

    if not write_client:
        print("❌ X API credentials not set")
        return

    replied_ids = load_replied_ids()
    all_targets = []
    all_results = []

    # 方式1: Google検索
    print("\n📡 方式1: Google検索")
    google_tweets = search_google_for_tweets()
    all_targets.extend(google_tweets)
    print(f"   Google発見: {len(google_tweets)}件")

    # 方式2: メンション監視
    print("\n📩 方式2: メンション監視")
    if read_client:
        mention_tweets = check_mentions(read_client, write_client)
        all_targets.extend(mention_tweets)
        print(f"   メンション: {len(mention_tweets)}件")
    else:
        print("   ⚠️ Bearer Token未設定")

    # 重複除去
    seen = set()
    unique_targets = []
    for t in all_targets:
        if t["id"] not in seen:
            seen.add(t["id"])
            unique_targets.append(t)

    print(f"\n🎯 ユニークターゲット: {len(unique_targets)}件")

    # 返信実行
    if unique_targets:
        all_results = reply_to_tweets(write_client, read_client, unique_targets, replied_ids)

    save_replied_ids(replied_ids)

    sent_count = sum(1 for r in all_results if r["status"] == "sent")
    print(f"\n📊 結果: {len(all_results)}件処理, {sent_count}件ポジデブ返信完了")

    # レポート生成
    generate_report(all_results, sent_count, time_label, now)
    print("✅ Complete!")


def generate_report(results, sent_count, time_label, now):
    lines = [
        f"## 🍖 ポジデブ自動返信レポート - {time_label}",
        "",
        f"**実行日時:** {now.strftime('%Y-%m-%d %H:%M JST')}",
        f"**処理数:** {len(results)}件",
        f"**自動返信:** {sent_count}件",
        "",
        "---",
        "",
    ]

    if not results:
        lines.append("*新しいネガデブ発言は見つかりませんでした。平和！🍖*")
    else:
        for i, r in enumerate(results, 1):
            emoji = "✅" if r["status"] == "sent" else "❌"
            source = {"google": "Google検索", "mention": "メンション"}.get(r.get("source"), "不明")
            lines.append(f"### #{i} {emoji} [{source}]")
            lines.append(f"**@{r['username']}**: {r['text'][:150]}")
            lines.append(f"")
            lines.append(f"**ポジデブ返信** ({r['member']['name']} {r['member']['role']}):")
            lines.append(f"> {r['response']}")
            lines.append(f"")
            lines.append("---")
            lines.append("")

    lines.append("*Powered by DEV PARADE ポジデブBot 🍖*")

    with open("search_report.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
