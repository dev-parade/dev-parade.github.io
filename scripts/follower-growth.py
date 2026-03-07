#!/usr/bin/env python3
"""
DEV PARADE X Follower Growth Engine
フォロワー増加マーケティング自動化

戦略:
1. エンゲージメント分析 - 過去ツイートのパフォーマンスを分析
2. 最適投稿時間の学習
3. ターゲットユーザーへのいいね・フォロー
4. トレンドハッシュタグの活用
5. フォロワー増加レポート生成
"""

import os
import json
import random
from datetime import datetime, timezone, timedelta

try:
    import tweepy
except ImportError:
    tweepy = None

API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")

GROWTH_LOG = "data/growth_log.json"

# フォロー対象のキーワード（これらに言及してるユーザーに関わる）
TARGET_KEYWORDS = [
    "ボディポジティブ", "ぽっちゃり", "大きいサイズ",
    "body positive", "plus size", "self love",
    "デブ芸人", "おデブ", "太ってる",
    "NARUTO", "バッチコイ",
]

# 関連アカウント（これらのフォロワーと交流）
RELATED_ACCOUNTS = [
    "matslovedx",      # マツコ系
    "watanabe_naomi",   # 渡辺直美
]

# 戦略的ハッシュタグセット
HASHTAG_SETS = {
    "core": ["#ポジデブ", "#ポジデブBot", "#DEVPARADE", "#デブパレード"],
    "reach": ["#ボディポジティブ", "#自己肯定感", "#ありのまま", "#bodypositivity"],
    "music": ["#バンド", "#ロック", "#邦ロック", "#バッチコイ", "#NARUTO"],
    "viral": ["#拡散希望", "#フォロバ100", "#相互フォロー"],
    "english": ["#BodyPositive", "#SelfLove", "#PlusSize", "#FatPositive"],
    "food": ["#焼肉", "#グルメ", "#大盛り", "#飯テロ"],
}


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


def load_growth_log():
    try:
        with open(GROWTH_LOG, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"runs": [], "liked_users": [], "followers_history": []}


def save_growth_log(log):
    with open(GROWTH_LOG, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def get_account_stats(read_client, write_client):
    """自アカウントの統計を取得"""
    try:
        me = write_client.get_me(
            user_fields=["public_metrics", "description", "created_at"]
        )
        if me.data:
            metrics = me.data.public_metrics or {}
            return {
                "username": me.data.username,
                "name": me.data.name,
                "followers": metrics.get("followers_count", 0),
                "following": metrics.get("following_count", 0),
                "tweets": metrics.get("tweet_count", 0),
                "listed": metrics.get("listed_count", 0),
            }
    except Exception as e:
        print(f"   ⚠️ アカウント情報取得エラー: {e}")
    return None


def analyze_recent_tweets(read_client, user_id):
    """直近ツイートのエンゲージメント分析"""
    try:
        tweets = read_client.get_users_tweets(
            id=user_id,
            max_results=20,
            tweet_fields=["public_metrics", "created_at", "text"],
        )
        if not tweets.data:
            return []

        results = []
        for tweet in tweets.data:
            metrics = tweet.public_metrics or {}
            engagement = (
                metrics.get("like_count", 0)
                + metrics.get("retweet_count", 0) * 2
                + metrics.get("reply_count", 0) * 3
                + metrics.get("quote_count", 0) * 2
            )
            results.append({
                "id": str(tweet.id),
                "text": tweet.text[:100],
                "likes": metrics.get("like_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "replies": metrics.get("reply_count", 0),
                "engagement_score": engagement,
                "created_at": str(tweet.created_at) if tweet.created_at else "",
            })

        results.sort(key=lambda x: x["engagement_score"], reverse=True)
        return results

    except Exception as e:
        print(f"   ⚠️ ツイート分析エラー: {e}")
        return []


def engage_with_mentions(write_client, read_client):
    """メンションに「いいね」で反応（フォロワーとの関係構築）"""
    liked = 0
    try:
        me = write_client.get_me()
        if not me.data:
            return 0

        mentions = read_client.get_users_mentions(
            id=me.data.id,
            max_results=10,
            tweet_fields=["author_id"],
        )
        if not mentions.data:
            return 0

        for tweet in mentions.data:
            if tweet.author_id == me.data.id:
                continue
            try:
                write_client.like(tweet.id)
                liked += 1
                print(f"   ❤️ いいね: {str(tweet.id)[:10]}...")
            except tweepy.errors.Forbidden:
                pass  # 既にいいね済み
            except Exception:
                pass

    except Exception as e:
        print(f"   ⚠️ メンションエンゲージ: {e}")

    return liked


def generate_growth_report(stats, tweet_analysis, liked_count, log):
    """フォロワー増加レポート生成"""
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)

    # フォロワー推移
    prev_followers = 0
    if log.get("followers_history"):
        prev_followers = log["followers_history"][-1].get("count", 0)

    followers = stats["followers"] if stats else 0
    diff = followers - prev_followers if prev_followers > 0 else 0
    diff_str = f"+{diff}" if diff >= 0 else str(diff)

    lines = [
        f"## 📈 DEV PARADE X Growth Report",
        "",
        f"**日時:** {now.strftime('%Y-%m-%d %H:%M JST')}",
        "",
        "---",
        "",
        "### アカウント統計",
        "",
    ]

    if stats:
        lines.extend([
            f"| 指標 | 数値 |",
            f"|------|------|",
            f"| フォロワー | **{stats['followers']}** ({diff_str}) |",
            f"| フォロー中 | {stats['following']} |",
            f"| ツイート数 | {stats['tweets']} |",
            f"| リスト登録 | {stats['listed']} |",
            "",
        ])

    # エンゲージメント分析
    if tweet_analysis:
        lines.extend([
            "### トップエンゲージメント ツイート",
            "",
        ])
        for i, t in enumerate(tweet_analysis[:5], 1):
            lines.extend([
                f"**#{i}** (Score: {t['engagement_score']})",
                f"> {t['text']}",
                f"❤️ {t['likes']} | 🔄 {t['retweets']} | 💬 {t['replies']}",
                "",
            ])

    # アクション実行結果
    lines.extend([
        "### 実行アクション",
        "",
        f"- メンションへのいいね: {liked_count}件",
        "",
    ])

    # マーケティングTIPS
    lines.extend([
        "### 📊 次のアクション推奨",
        "",
        "1. **エンゲージメント高いツイートの傾向を分析** → 似た内容を増やす",
        "2. **メンションには必ず反応** → ファンとの関係構築",
        "3. **ハッシュタグ戦略** → #ポジデブ #BodyPositive を定着させる",
        "4. **コラボ** → デブ芸人、フードインフルエンサーとの絡み",
        "5. **スレッド投稿** → 滞在時間UPでアルゴリズム優遇",
        "",
        "---",
        "*DEV PARADE Growth Engine 🍖*",
    ])

    with open("growth_report.md", "w") as f:
        f.write("\n".join(lines))

    return "\n".join(lines)


def main():
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)

    print("=" * 50)
    print(f"📈 DEV PARADE X Growth Engine")
    print(f"   {now.strftime('%Y-%m-%d %H:%M JST')}")
    print("=" * 50)

    write_client = get_write_client()
    read_client = get_read_client()

    if not write_client:
        print("❌ X API credentials not set")
        return

    log = load_growth_log()

    # 1. アカウント統計取得
    print("\n📊 アカウント統計...")
    stats = get_account_stats(read_client, write_client)
    if stats:
        print(f"   @{stats['username']}")
        print(f"   フォロワー: {stats['followers']}")
        print(f"   ツイート数: {stats['tweets']}")

        # 履歴に追加
        log.setdefault("followers_history", []).append({
            "date": now.strftime("%Y-%m-%d %H:%M"),
            "count": stats["followers"],
        })
        # 最新30件のみ保持
        log["followers_history"] = log["followers_history"][-30:]

    # 2. ツイート分析
    print("\n📈 エンゲージメント分析...")
    tweet_analysis = []
    if stats:
        try:
            me = write_client.get_me()
            if me.data:
                tweet_analysis = analyze_recent_tweets(read_client, me.data.id)
                if tweet_analysis:
                    best = tweet_analysis[0]
                    print(f"   ベストツイート: {best['text'][:50]}...")
                    print(f"   Score: {best['engagement_score']} (❤️{best['likes']} 🔄{best['retweets']})")
        except Exception as e:
            print(f"   ⚠️ 分析エラー: {e}")

    # 3. メンションへの「いいね」
    print("\n❤️ メンションエンゲージメント...")
    liked_count = engage_with_mentions(write_client, read_client)
    print(f"   いいね実行: {liked_count}件")

    # 4. レポート生成
    print("\n📝 レポート生成...")
    generate_growth_report(stats, tweet_analysis, liked_count, log)

    # ログ保存
    log.setdefault("runs", []).append({
        "date": now.strftime("%Y-%m-%d %H:%M"),
        "followers": stats["followers"] if stats else 0,
        "liked": liked_count,
    })
    log["runs"] = log["runs"][-100:]
    save_growth_log(log)

    print("\n✅ Growth Engine Complete!")


if __name__ == "__main__":
    main()
