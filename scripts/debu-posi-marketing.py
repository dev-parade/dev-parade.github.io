#!/usr/bin/env python3
"""
DebuPosi Marketing - 自動マーケティング・告知投稿スクリプト

各SNSにデブポジBotの告知を自動投稿し、集客する。
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
BOT_URL = "https://dev-parade.github.io/debu-bot.html"
SITE_URL = "https://dev-parade.github.io/"
YOUTUBE_URL = "https://youtube.com/playlist?list=PL0THYLU4QbDkldXStxeHXCfsTnas90AoP"

# ===== 告知ツイートのバリエーション =====
PROMO_TWEETS = {
    "launch": [
        f"""🍖【世界初】デブポジBot、爆誕。

SNS上の全ての「デブ」をポジティブに変換するBot、作りました。

総体重570kg超のバンド DEV PARADEが、
全てのネガティブなデブ発言を
全力で肯定します。

試してみて👇
{BOT_URL}

#デブポジBot #DEVPARADE #デブパレード""",

        f"""「デブ」って言われて傷ついた全ての人へ。

俺たちDEV PARADE、メンバー全員90kg以上。
バンド名にデブ入れてる。
しかもメジャーデビューした。

デブは才能。脂肪は努力の結晶。

そんな俺たちが作った「デブポジBot」
ネガティブ → ポジティブに全変換🍖

{BOT_URL}
#デブポジBot""",
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
#デブポジBot #DEVPARADE""",

        f"""【定期】

DEV PARADEのメンバー体重

🎤 ハンサム判治 100kg
🎙️ COYASS 93kg
🎸 ugazin 135kg
🎸 ぺー 120kg
🥁 TAH 120kg

合計: 570kg超

全員痛風ホルダー。
全員メジャーデビュー経験あり。

体重と才能は比例する。🍖
#DEVPARADE #デブパレード""",

        f"""「太った」→「成長した」
「デブ」→「存在感がある」
「メタボ」→「ロックな体型」
「ビール腹」→「人生楽しんでる証拠」
「痩せろ」→「そのままでいい」

全部ポジティブに変換するBot作った🍖
{BOT_URL}

#デブポジBot #DEVPARADE""",

        f"""今日のデブポジ名言:

「この世に無駄な脂肪はない。
全部、お前という作品の一部だ。」

— DEV PARADE（総体重570kg超）🍖

{BOT_URL}
#デブポジBot #デブポジ""",

        f"""体重と幸福度は比例する。

（DEV PARADE調べ）

source: 俺たち570kg超で幸せ🍖

#デブポジBot #DEVPARADE
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

#デブポジBot #DEVPARADE
{BOT_URL}""",

        f"""あなたの「デブ」エピソード、
デブポジBotが全力ポジティブに変換します。

入力: ネガティブな体型の悩み
出力: DEV PARADEメンバーからの全力肯定

やってみて👇🍖
{BOT_URL}

#デブポジBot""",

        f"""太ってる人にしかわからないこと

・椅子の肘掛けは敵
・ジェットコースターのバーが下がらない
・飛行機のベルト延長を頼む勇気
・電車の席で隣に申し訳ない

全部わかる。全部経験した。
でも全部ネタになる。
それがDEV PARADEのスピリット🍖

#デブポジBot #DEVPARADE""",

        f"""【急募】体重90kg以上の仲間

資格:
・体重90kg以上
・音楽が好き
・デブに誇りを持てる
・痛風でも前を向ける

待遇:
・DEV PARADEが全力で肯定
・デブポジBotが24時間あなたの味方

{BOT_URL}
#デブポジBot #DEVPARADE""",

        f"""太ったことを後悔してるあなたへ。

後悔する必要ゼロ。

俺たちは太ったことを武器にして
バンド組んで
メジャーデビューして
NARUTOのエンディング歌って
15年ぶりに復活した。

全部、太ってたから。🍖

#デブポジBot #DEVPARADE #バッチコイ
{SITE_URL}""",
    ],

    "collab": [
        f"""【コラボ募集】

デブポジBotと一緒にデブをポジティブにしたい
企業・ブランド・インフルエンサーを募集中！

・フードブランド🍔
・アパレル（大きいサイズ）👕
・フィットネス（ボディポジティブ系）💪
・お笑い芸人（デブ芸人さん大歓迎）🎤

DM or リプライで！🍖
#デブポジBot #コラボ募集""",
    ],
}

# ===== リプライ用テンプレート（バズりそうなツイートに反応） =====
VIRAL_REPLIES = [
    "デブの話題が出たので来ました。総体重570kg超バンドのDEV PARADEです。デブは才能。🍖 #デブポジBot",
    "デブをネガティブに語るスレッドに割り込む総体重570kg超バンドです。デブは最高。🍖 #デブポジBot",
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
        bearer_token=bearer,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
        wait_on_rate_limit=True,
    )


def post_promo_tweet(client, campaign):
    """告知ツイートを投稿"""
    tweets = PROMO_TWEETS.get(campaign, PROMO_TWEETS["scheduled"])
    tweet_text = random.choice(tweets)

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
        except Exception as e:
            print(f"❌ Failed: {e}")
            return {"text": tweet_text, "id": None, "status": f"failed: {e}"}
    else:
        print("⚠️ No X client - dry run")
        return {"text": tweet_text, "id": None, "status": "dry_run"}


def generate_marketing_log(result):
    """マーケティングログ生成"""
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")

    log = f"""## 📢 デブポジBot マーケティングログ

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
🍖 デブポジBot 始動！

SNSの「デブ」を全部ポジティブに変換する
世界初のBot作った！

プロフのリンクから試してみて！

#デブポジBot #DEVPARADE #デブパレード
```

### Facebook投稿用テキスト（コピペ用）

```
【デブポジBot 始動🍖】

DEV PARADEが、SNS上の全ての「デブ」「太った」「痩せろ」を
ポジティブに変換するBotを作りました！

総体重570kg超のバンドだからこそ言える。
デブは才能。脂肪は努力の結晶。

試してみてください👇
{BOT_URL}

#デブポジBot #DEVPARADE #デブパレード
```

---
🍖 Powered by DEV PARADE Marketing
"""

    with open("marketing_log.md", "w") as f:
        f.write(log)


def main():
    print("=" * 50)
    print("📢 DebuPosi Marketing")
    print(f"   Campaign: {CAMPAIGN}")
    print("=" * 50)

    client = get_x_client()
    result = post_promo_tweet(client, CAMPAIGN)
    generate_marketing_log(result)

    print("\n📢 Marketing run complete!")


if __name__ == "__main__":
    main()
