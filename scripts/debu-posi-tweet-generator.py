#!/usr/bin/env python3
"""
PosiDev Daily Tweet - 毎日のポジデブ自動投稿

曜日・時間帯に応じてバリエーション豊かなポジデブツイートを自動投稿。
30日以上被らないよう十分なテンプレートを用意。
"""

import os
import random
import hashlib
import urllib.parse
from datetime import datetime, timezone, timedelta

try:
    import tweepy
except ImportError:
    tweepy = None

CAMPAIGN = os.environ.get("CAMPAIGN", "scheduled")
API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")
BOT_URL = "https://dev-parade.github.io/debu-bot.html"
SITE_URL = "https://dev-parade.github.io/"
IG_URL = "https://www.instagram.com/dev.parade/"

# ===== 日替わりポジデブツイート（35種類以上） =====
DAILY_TWEETS = [
    # ----- ポジデブ名言系 -----
    f"""今日のポジデブ名言:

「この世に無駄な脂肪はない。
全部、お前という作品の一部だ。」

— DEV PARADE（総体重570kg超）🍖

{BOT_URL}
#ポジデブBot #ポジデブ""",

    f"""今日のポジデブ名言:

「体重が増えるたびに、
地球がお前を離したくなくなってる。」

モテてるぜ、地球に。🌍🍖

#ポジデブBot #DEVPARADE""",

    f"""今日のポジデブ名言:

「ダイエットは明日から」
→ これは「今日を全力で楽しむ」という意味。

正しい。🍖

#ポジデブBot #DEVPARADE""",

    f"""今日のポジデブ名言:

「デブは個性。個性は武器。武器は磨け。」

磨き方: 焼肉食う。🍖

#ポジデブBot #DEVPARADE""",

    f"""今日のポジデブ名言:

「痩せたら半分の男になる。
半分の男でいいのか？ 全部でいろ。」

— DEV PARADE 🍖

#ポジデブBot #ポジデブ""",

    f"""今日のポジデブ名言:

「腹が出てるんじゃない。
夢が詰まってるんだ。」

DEV PARADEの腹には570kg分の夢が詰まってます🍖

#ポジデブBot #DEVPARADE""",

    # ----- メンバー体重ネタ系 -----
    f"""【定期】DEV PARADEのメンバー体重

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

    f"""DEV PARADEの入団条件:

✅ 体重90kg以上
✅ 音楽が好き
✅ デブに誇りを持てる
✅ 痛風でも前を向ける

現在メンバー5名、合計570kg超。
次の仲間、募集中。🍖

#DEVPARADE #ポジデブBot""",

    f"""DEV PARADEメンバー豆知識:

ugazin（Gt.）は135kg。
ギターの弦より太い指で繊細なメロディを紡ぐ男。

体重と繊細さは共存する。🍖

#DEVPARADE #ポジデブ""",

    f"""DEV PARADEメンバー豆知識:

TAH（Dr.）は120kg。
バスドラが二度と元に戻らないパワー。

それがヘヴィメタボの「ヘヴィ」の意味。🍖

#DEVPARADE #ポジデブ""",

    # ----- ポジデブ変換例系 -----
    f"""「太った」→「成長した」
「デブ」→「存在感がある」
「メタボ」→「ロックな体型」
「ビール腹」→「人生楽しんでる証拠」
「痩せろ」→「そのままでいい」

全部ポジティブに変換するBot作った🍖
{BOT_URL}

#ポジデブBot #DEVPARADE""",

    f"""ポジデブBot 変換例:

😢「また太った...」
🍖「太った？ それは成長！細胞レベルで進化してる」

😢「デブって言われた」
🍖「DEV PARADEの入団資格満たしてます（条件:90kg以上）」

あなたも変換してみて👇
{BOT_URL}
#ポジデブBot""",

    f"""ポジデブ変換辞典:

「二重あご」→「顔にクッション装備」
「脂肪」→「努力の結晶」
「満腹」→「幸福度MAX」
「体重計が怖い」→「数字に支配されない生き方」

全部正解。🍖

#ポジデブBot #DEVPARADE
{BOT_URL}""",

    f"""ネガデブ → ポジデブ変換:

❌「食べすぎた...」
⭕「栄養を十分に摂取した」

❌「服が入らない」
⭕「服が追いついてない」

❌「体重やばい」
⭕「存在感がやばい」

言い方ひとつで世界は変わる🍖

#ポジデブBot #DEVPARADE""",

    # ----- バズ狙い / 共感系 -----
    f"""Q. デブのメリットは？

A.
・冬あったかい
・存在感がある
・海で浮きやすい
・抱きしめた時の安心感
・食レポの説得力が段違い
・地球に愛されてる（重力的な意味で）

反論は受け付けません。🍖

{BOT_URL}
#ポジデブBot #DEVPARADE""",

    f"""太ってる人にしかわからないこと

・椅子の肘掛けは敵
・ジェットコースターのバーが下がらない
・飛行機のベルト延長を頼む勇気
・電車で「すいません」が口癖

全部わかる。全部経験した。
でも全部ネタになる。
それがDEV PARADEのスピリット🍖

#ポジデブBot #DEVPARADE""",

    f"""太ってる人あるある:

・夏は存在するだけで暑い
・靴紐結ぶのが一苦労
・「痩せた？」が最高の褒め言葉になる
・でも焼肉の前ではダイエットの記憶が消える

全部あるある。全部愛おしい。🍖

#ポジデブBot #DEVPARADE""",

    f"""太ってる人の特殊能力:

・冬でも薄着で過ごせる（自家発熱）
・満員電車で押し負けない（物理）
・ハグの包容力が異次元
・「よく食べる人」として信頼される

全部、才能。🍖

#ポジデブBot #DEVPARADE""",

    # ----- バンドエピソード系 -----
    f"""NARUTOのエンディングテーマ歌ってた
メンバー全員90kg以上のバンドが
15年ぶりに復活して
「デブをポジティブにするBot」を作った

という情報が流れてきたら
それは全部事実です🍖

{SITE_URL}
#DEVPARADE #デブパレード #バッチコイ""",

    f"""DEV PARADEが解散した理由:

「メンバーが痩せてメタボを名乗れなくなった」

復活した理由:

「全員太り直した」

これが人生。🍖

#DEVPARADE #デブパレード""",

    f"""2011年「メンバーが痩せた」で解散。
2026年「全員太り直した」で復活。

15年かけて太り直すバンド、
他にいる？🍖

#DEVPARADE #デブパレード #バッチコイ
{SITE_URL}""",

    f"""DEV PARADE = Def Leppardのパロディ。
ただし体重は本家の3倍。

「ヘヴィメタル」じゃなくて「ヘヴィメタボ」。
メタルより重い、メタボの響き。🍖

#DEVPARADE #デブパレード""",

    f"""HEY!HEY!HEY!にも出た。
SUMMER SONICにも出た。
NARUTOのEDも歌った。

全部、デブのまま。
痩せなくても夢は叶う。🍖

#DEVPARADE #バッチコイ
{SITE_URL}""",

    # ----- 哲学 / ライフスタイル系 -----
    f"""ダイエットの語源は「生き方」（ギリシャ語 diaita）

つまり「ダイエットしなきゃ」は
「生き方を変えなきゃ」という意味。

でも今の生き方、最高じゃん？
変えなくていいよ。🍖

#ポジデブBot #DEVPARADE
{BOT_URL}""",

    f"""体重と幸福度は比例する。
（DEV PARADE調べ）

source: 俺たち570kg超で幸せ🍖

#ポジデブBot #DEVPARADE
{BOT_URL}""",

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

    f"""「痩せたらモテる」は嘘。

モテるかどうかは自信で決まる。
自信は自分を好きになることで生まれる。

デブの自分を好きになれ。
そしたら最強。🍖

#ポジデブBot #DEVPARADE""",

    f"""世界の偉人とデブ:

チャーチル → デブ
ベーブルース → デブ
パバロッティ → デブ
マツコデラックス → デブ
DEV PARADE → 全員デブ

デブは歴史を作る。🍖

#ポジデブBot #DEVPARADE""",

    # ----- 食テロ / グルメ系 -----
    f"""深夜のカップ麺は罪じゃない。
ご褒美。

お前は今日も頑張った。
だからカップ麺を食う権利がある。

DEV PARADEが許可する。🍖

#ポジデブBot #DEVPARADE""",

    f"""「食べたら太る」

当たり前だろ。
食べなかったら死ぬ。

生きてる証拠を太ると呼ぶな。
それは「生命力」だ。🍖

#ポジデブBot #DEVPARADE""",

    f"""焼肉は全てを解決する。

悩み → 肉食ったら忘れる
ストレス → 肉食ったら消える
体重 → 肉食ったら増える

2勝1分。勝ち越し。🍖

#ポジデブBot #DEVPARADE""",

    # ----- Bot告知系 -----
    f"""あなたの「デブ」エピソード、
ポジデブBotが全力ポジティブに変換します。

入力: ネガティブな体型の悩み
出力: DEV PARADEメンバーからの全力肯定

やってみて👇🍖
{BOT_URL}

#ポジデブBot""",

    f"""🍖【世界初】ポジデブBot

SNS上の全ての「デブ」をポジティブに変換！
総体重570kg超のバンド DEV PARADEが全力で肯定。

試してみて👇
{BOT_URL}

#ポジデブBot #DEVPARADE #デブパレード""",

    # ----- 季節・曜日系 -----
    f"""月曜日のポジデブ:

「月曜日が憂鬱」って？
大丈夫、体重が重いから
簡単には動じない。

どっしり構えろ。
それがデブの強さ。🍖

#ポジデブBot #DEVPARADE #月曜日""",

    f"""金曜日のポジデブ:

週末は何食べる？
迷ったら全部食え。

5日間頑張った体に
ご褒美をたっぷりと。

DEV PARADEが全力で肯定する。🍖

#ポジデブBot #DEVPARADE #金曜日""",

    f"""週末のポジデブ:

「食べすぎた週末」なんてない。
「栄養を十分に蓄えた週末」があるだけ。

来週に向けてエネルギー満タン。
準備万端。🍖

#ポジデブBot #DEVPARADE""",

    # ----- 参加型 / 質問系 -----
    f"""【質問】あなたの好きな食べ物は？

DEV PARADEメンバーの回答:
🎤 判治: 焼肉
🎙️ COYASS: ラーメン
🎸 ugazin: カレー
🎸 ぺー: 寿司
🥁 TAH: 全部

リプで教えて🍖

#ポジデブBot #DEVPARADE""",

    f"""【ポジデブチャレンジ】

鏡の前で「俺（私）、最高じゃん」
って言ってみて。

言えた人、もうポジデブ。
DEV PARADEの仲間。🍖

#ポジデブBot #ポジデブチャレンジ #DEVPARADE""",
]

# ===== ランチ / コラボ用 =====
LAUNCH_TWEETS = [
    f"""「デブ」って言われて傷ついた全ての人へ。

俺たちDEV PARADE、メンバー全員90kg以上。
バンド名にデブ入れてる。
しかもメジャーデビューした。

デブは才能。脂肪は努力の結晶。

そんな俺たちが作った「ポジデブBot」🍖

{BOT_URL}
#ポジデブBot #DEVPARADE""",
]

COLLAB_TWEETS = [
    f"""【コラボ募集】

ポジデブBotと一緒にデブをポジティブにしたい
企業・ブランド・インフルエンサーを募集中！

・フードブランド🍔
・アパレル（大きいサイズ）👕
・お笑い芸人（デブ芸人さん大歓迎）🎤

DM or リプライで！🍖
#ポジデブBot #コラボ募集""",
]

TWEETS = {
    "launch": LAUNCH_TWEETS,
    "scheduled": DAILY_TWEETS,
    "collab": COLLAB_TWEETS,
}


def select_daily_tweet():
    """日付ベースでツイートを選択（同じ日は同じツイート、日が変われば別のツイート）"""
    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).strftime("%Y-%m-%d")
    # 日付からハッシュを生成して、テンプレートのインデックスに変換
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    index = seed % len(DAILY_TWEETS)
    return DAILY_TWEETS[index]


def auto_post(tweet_text):
    """X APIで自動投稿"""
    if not tweepy or not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
        return None
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET,
        )
        result = client.create_tweet(text=tweet_text)
        tweet_id = result.data["id"]
        print(f"✅ Auto-posted! Tweet ID: {tweet_id}")
        return tweet_id
    except Exception as e:
        print(f"❌ Auto-post failed: {e}")
        return None


def main():
    if CAMPAIGN == "scheduled":
        tweet_text = select_daily_tweet()
    else:
        tweets = TWEETS.get(CAMPAIGN, DAILY_TWEETS)
        tweet_text = random.choice(tweets)

    print(f"Campaign: {CAMPAIGN}")
    print(f"Tweet ({len(tweet_text)} chars):")
    print(tweet_text)

    # 自動投稿
    tweet_id = auto_post(tweet_text)
    auto_posted = tweet_id is not None

    # Intent URL
    intent_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet_text)

    # Issue用Markdown
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")
    status = "✅ 自動投稿済み" if auto_posted else "📋 手動投稿待ち"
    tweet_link = f"https://twitter.com/dev_parade/status/{tweet_id}" if tweet_id else ""

    issue_md = f"""## 🍖 ポジデブツイート（自動生成）

**生成日時:** {now}
**キャンペーン:** {CAMPAIGN}
**ステータス:** {status}
{"**投稿リンク:** " + tweet_link if tweet_link else ""}

---

### ツイート内容（{len(tweet_text)}文字）

```
{tweet_text}
```

---

{"✅ 自動投稿完了！" if auto_posted else "### 👇 ワンクリックで投稿 👇"}

---
🍖 Daily PosiDev Tweet by DEV PARADE
"""

    with open("tweet_issue.md", "w") as f:
        f.write(issue_md)

    print(f"\nIntent URL: {intent_url}")
    print("✅ Issue markdown generated!")


if __name__ == "__main__":
    main()
