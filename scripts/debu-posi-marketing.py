#!/usr/bin/env python3
"""
PosiDev Marketing - 自動マーケティング・告知投稿スクリプト

各SNSにポジデブBotの告知を自動投稿し、集客する。
バイラルを狙ったコンテンツを定期投稿。
"""

import os
import sys
import random
from datetime import datetime, timezone, timedelta

try:
    import tweepy
except ImportError:
    print("tweepy not installed")
    sys.exit(1)

CAMPAIGN = os.environ.get("CAMPAIGN", "scheduled")
BOT_URL = "https://devparade.jp/debu-bot.html"
SITE_URL = "https://devparade.jp/"
YOUTUBE_URL = "https://youtube.com/playlist?list=PL0THYLU4QbDkldXStxeHXCfsTnas90AoP"

# ===== 告知ツイートのバリエーション =====
PROMO_TWEETS = {
    "launch": [
        f"""🍖 ポジデブBot、爆誕。

SNS上の全ての「デブ」をポジティブに変換するBot、作りました。

全員90kg超のバンド Devparadeが、
全てのネガティブなデブ発言を
全力で肯定します。

試してみて👇
{BOT_URL}

#ポジデブBot #DEVPARADE #デブパレード""",

        f"""「デブ」って言われて傷ついた全ての人へ。

俺たちDevparade、メンバー全員90kg以上。
バンド名にデブ入れてる。
しかもメジャーデビューした。

デブは才能。脂肪は努力の結晶。

そんな俺たちが作った「ポジデブBot」
ネガティブ → ポジティブに全変換🍖

{BOT_URL}
#ポジデブBot""",
    ],

    "scheduled": [
        # ===== バズ狙いツイート（ランダムで1つ選択） =====

        f"""Q. デブのメリットは？

A.
・冬あったかい
・ぶつかっても痛くない
・存在感がある
・海で浮きやすい
・抱きしめた時の安心感
・食レポの説得力が段違い
・地球に愛されてる（重力的な意味で）

反論は受け付けません。🍖

{BOT_URL}
#ポジデブBot #DEVPARADE""",

        f"""【定期】

Devparadeのメンバー

🎤 ハンサム判治（Vo./Leader）
🎙️ COYASS（MC）
🎸 ugazin（Gt./作曲）
🎸 ぺー（Ba.）NEW!
🥁 TAH（Dr.）

全員90kg以上。DefSTAR Records（ソニー）からメジャーデビュー。

体重と才能は比例する。🍖
#DEVPARADE #デブパレード""",

        f"""「太った」→「成長した」
「デブ」→「存在感がある」
「メタボ」→「ロックな体型」
「ビール腹」→「人生楽しんでる証拠」
「痩せろ」→「そのままでいい」

全部ポジティブに変換するBot作った🍖
{BOT_URL}

#ポジデブBot #DEVPARADE""",

        f"""今日のデブポジ名言:

「この世に無駄な脂肪はない。
全部、お前という作品の一部だ。」

— Devparade（全員90kg超）🍖

{BOT_URL}
#ポジデブBot #ポジデブ""",

        f"""体重と幸福度は比例する。

（Devparade調べ）

source: 俺たち全員90kg超で幸せ🍖

#ポジデブBot #DEVPARADE
{BOT_URL}""",

        f"""NARUTOのエンディングテーマ歌ってた
メンバー全員90kg以上のバンドが
15年ぶりに復活して
「デブをポジティブにするBot」を作った
という情報が流れてきたら
それは全部事実です🍖

{SITE_URL}
#DEVPARADE #デブパレード #バッチコイ""",

        f"""ダイエットの語源は「生き方」（ギリシャ語 diaita）

つまり「ダイエットしなきゃ」は
「生き方を変えなきゃ」という意味。

でも今の生き方、
最高じゃん？

変えなくていいよ。🍖

#ポジデブBot #DEVPARADE
{BOT_URL}""",

        f"""あなたの「デブ」エピソード、
ポジデブBotが全力ポジティブに変換します。

入力: ネガティブな体型の悩み
出力: Devparadeメンバーからの全力肯定

やってみて👇🍖
{BOT_URL}

#ポジデブBot""",

        f"""太ってる人にしかわからないこと

・椅子の肘掛けは敵
・ジェットコースターのバーが下がらない
・飛行機のベルト延長を頼む勇気
・電車の席で隣に申し訳ない

全部わかる。全部経験した。
でも全部ネタになる。
それがDevparadeのスピリット🍖

#ポジデブBot #DEVPARADE""",

        f"""【大募集】
あなたの「ポジデブ」なエピソード募集中！

「太ってるからこそ、こんなに幸せ！」
「この食べ物、実は野菜！」
など、あなたのポジティブなデブライフを
リプで送ってください🍖

ポジデブBotが全力で肯定します。
{BOT_URL}
#ポジデブBot #DEVPARADE""",

        f"""太ったことを後悔してるあなたへ。

後悔する必要ゼロ。

俺たちは太ったことを武器にして
バンド組んで
メジャーデビューして
NARUTOのエンディング歌って
15年ぶりに復活した。

全部、太ってたから。🍖

#ポジデブBot #DEVPARADE #バッチコイ
{SITE_URL}""",
    ],

    "collab": [
        f"""【コラボ募集】

ポジデブBotと一緒にデブをポジティブにしたい
企業・ブランド・インフルエンサーを募集中！

・フードブランド🍔
・アパレル（大きいサイズ）👕
・フィットネス（ボディポジティブ系）💪
・お笑い芸人（デブ芸人さん大歓迎）🎤

DM or リプライで！🍖
#ポジデブBot #コラボ募集""",
    ],
}

# ===== リプライ用テンプレート（バズりそうなツイートに反応） =====
VIRAL_REPLIES = [
    "デブの話題が出たので来ました。全員90kg超バンドのDevparadeです。デブは才能。🍖 #ポジデブBot",
    "デブをネガティブに語るスレッドに割り込む全員90kg超バンドです。デブは最高。🍖 #ポジデブBot",
]


def get_x_client():
    """X API v2クライアント"""
    bearer = os.environ.get("X_BEARER_TOKEN")
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_SECRET")

    if not all([bearer, api_key, api_secret, access_token, access_secret]):
        return None

    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
        wait_on_rate_limit=True,
    )


def is_hallucination_suspected(text):
    """
    ツイート内容に捏造（ハルシネーション）の疑いがあるかチェック。
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


def post_promo_tweet(client, campaign):
    """告知ツイートを投稿"""
    tweets = PROMO_TWEETS.get(campaign, PROMO_TWEETS["scheduled"])
    
    # ハルシネーションチェックを行いつつツイートを選択
    tweet_text = random.choice(tweets)
    if is_hallucination_suspected(tweet_text):
        print(f"⚠️ [GUARDRAIL] Hallucination suspected in template: {tweet_text[:30]}...")
        # テンプレートに問題がある場合は別の候補を探す
        safe_tweets = [t for t in tweets if not is_hallucination_suspected(t)]
        if safe_tweets:
            tweet_text = random.choice(safe_tweets)
        else:
            print("❌ No safe tweets found in this campaign. Aborting.")
            return {"text": tweet_text, "id": None, "status": "aborted (hallucination)"}

    print(f"Campaign: {campaign}")
    print(f"Tweet ({len(tweet_text)} chars):")
    print(tweet_text)
    print("---")

    if client:
        try:
            result = client.create_tweet(text=tweet_text)
            tweet_id = result.data["id"]
            print(f"✅ Posted! Tweet ID: {tweet_id}")
            return {"text": tweet_text, "id": tweet_id, "status": "posted"}
        except tweepy.errors.Forbidden as e:
            print(f"❌ Failed (403): {e}")
            print(f"Response: {e.response.text if hasattr(e, 'response') and e.response else 'N/A'}")
            print(f"API Errors: {e.api_errors if hasattr(e, 'api_errors') else 'N/A'}")
            return {"text": tweet_text, "id": None, "status": f"failed: {e}"}
        except Exception as e:
            print(f"❌ Failed: {type(e).__name__}: {e}")
            return {"text": tweet_text, "id": None, "status": f"failed: {e}"}
    else:
        print("⚠️ No X client - dry run")
        return {"text": tweet_text, "id": None, "status": "dry_run"}


def generate_marketing_log(result):
    """マーケティングログ生成"""
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")

    log = f"""## 📢 ポジデブBot マーケティングログ

**実行日時:** {now}
**キャンペーン:** {CAMPAIGN}
**ステータス:** {result['status']}

### 投稿内容

```
{result['text']}
```

### プラットフォーム

| SNS | ステータス |
|-----|----------|
| X (Twitter) | {'✅ 投稿済み' if result['id'] else '⚠️ ' + result['status']} |
| Instagram | 📋 手動投稿推奨 |
| Facebook | 📋 手動投稿推奨 |
| TikTok | 📋 動画コンテンツ推奨 |

### 次のアクション

- [ ] Instagramストーリーで告知
- [ ] Facebookページに投稿
- [ ] TikTokでデブポジ動画作成
- [ ] noteで関連記事公開

### Instagramストーリー用テキスト（コピペ用）

```
🍖 ポジデブBot 始動！

SNSの「デブ」を全部ポジティブに変換する
世界初のBot作った！

プロフのリンクから試してみて！

#ポジデブBot #DEVPARADE #デブパレード
```

### Facebook投稿用テキスト（コピペ用）

```
【ポジデブBot 始動🍖】

Devparadeが、SNS上の全ての「デブ」「太った」「痩せろ」を
ポジティブに変換するBotを作りました！

全員90kg超のバンドだからこそ言える。
デブは才能。脂肪は努力の結晶。

試してみてください👇
{BOT_URL}

#ポジデブBot #DEVPARADE #デブパレード
```

---
🍖 Powered by Devparade Marketing
"""

    with open("marketing_log.md", "w") as f:
        f.write(log)


def main():
    print("=" * 50)
    print("📢 PosiDev Marketing")
    print(f"   Campaign: {CAMPAIGN}")
    print("=" * 50)

    client = get_x_client()
    result = post_promo_tweet(client, CAMPAIGN)
    generate_marketing_log(result)

    print("\n📢 Marketing run complete!")


if __name__ == "__main__":
    main()
