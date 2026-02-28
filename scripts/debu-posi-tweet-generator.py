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

# ===== 日替わりポジデブツイート（55種類以上） =====
DAILY_TWEETS = [
    # ===== 🔥 パンチライン / ワンライナー系 =====
    f"""俺の体重は92kg。
夢の重さも92kg。

軽い夢なんか持ったことない。🍖

#DEVPARADE #デブパレード""",

    f"""「デカい」は英語で"Big"。
"Big"は「偉大な」って意味もある。

つまりデブ＝偉大。
はい、証明終了。🍖

#ポジデブBot #DEVPARADE""",

    f"""1kg太るたびに、
俺は1kg分の人生を楽しんだ。

90kg超えたってことは、
90kg分の幸福の証拠。🍖

#DEVPARADE #デブパレード""",

    f"""鏡を見て「かっこいい」と思えるかどうかは
体重じゃなく生き様で決まる。

俺は90kg超。
そして、俺はかっこいい。🍖

#ポジデブBot #DEVPARADE""",

    f"""「太ってるのにステージ立つの？」

太ってるから立つんだよ。
この存在感、痩せたら出せねえぞ。🍖

#DEVPARADE #バッチコイ""",

    f"""スーツが似合わないんじゃない。
スーツが俺に追いついてないだけ。🍖

#ポジデブBot #DEVPARADE""",

    f"""腹が出てる？
これは腹筋の上に
もう一枚アーマーを装着してるだけだ。

防御力が高いとも言う。🍖

#DEVPARADE #デブパレード""",

    f"""BMIの「B」は
たぶん「Boss」の略。

確認はしてない。
でも俺のBMI、ボスの風格ある。🍖

#ポジデブBot #DEVPARADE""",

    # ===== 🎤 自虐→痛快反転系 =====
    f"""面接で「体力に自信は？」って聞かれた。

毎日この体重で生きてるんだぞ。
誰より体力あるわ。🍖

#ポジデブBot #DEVPARADE""",

    f"""満員電車で押されても動かない。

90kg超のメリットNo.1は
物理的に「ブレない男」になれること。🍖

#DEVPARADE #デブパレード""",

    f"""椅子に座ると軋む。

俺が重いんじゃない。
椅子が弱いだけ。

鍛えろ、椅子。🍖

#ポジデブBot #DEVPARADE""",

    f"""靴紐を結ぶ時、息が止まる。

これはフリーダイビングの訓練。
デブは日常的にアスリート。🍖

#DEVPARADE #デブパレード""",

    f"""試着室で「これもうワンサイズ上ありますか」

3回言った。
3回とも店員の笑顔が引きつった。

でも俺は笑えた。
それがポジデブ。🍖

#ポジデブBot #DEVPARADE""",

    f"""体重計「エラー」

いや、壊れたのはお前の方だろ。
俺は正常だ。絶好調だ。🍖

#DEVPARADE #デブパレード""",

    # ===== 🌍 かっこいいデブ / 偉人引用系 =====
    f"""チャーチルは太っていた。
300ポンドの体で世界を守った。

ビッグ・パンは太っていた。
ヒップホップの歴史を変えた。

Notorious B.I.G.は太っていた。
史上最高のラッパーと呼ばれた。

デブが世界を動かす。
DEV PARADEもそっち側。🍖

#DEVPARADE""",

    f"""相撲取りは何百年もの間、
体の大きさを「強さ」として誇ってきた。

日本にはもともと
「デブ＝かっこいい」文化がある。

俺たちは原点回帰してるだけ。🍖

#ポジデブBot #DEVPARADE""",

    f"""「痩せたらモテる」

嘘つけ。
DJ Khaledも
Rick Rossも
Action Bronsonも
痩せてねえけどモテてる。

モテるのは自信がある奴だ。
体重じゃない。🍖

#DEVPARADE #デブパレード""",

    f"""映画の中のデブは
いつも「いじられ役」か「お笑い担当」。

俺たちは主役をやる。
デブが主役のバンド。
しかもメジャーデビュー済み。

キャスティングは俺たちで変える。🍖

#DEVPARADE #バッチコイ""",

    # ===== 🍖 食のライフスタイル系 =====
    f"""深夜2時。冷蔵庫が俺を呼んでる。

これを「誘惑」と呼ぶ人がいるが、
俺は「運命の出会い」と呼ぶ。🍖

#ポジデブBot #DEVPARADE""",

    f"""「最後のひとくち」は嘘つきが使う言葉。

正直に「まだ食う」と言え。
その方がかっこいい。🍖

#DEVPARADE #デブパレード""",

    f"""焼肉を前にしたデブの集中力。

これをビジネスに応用すれば
世界を獲れる。

応用する気はないけど。
今は肉に集中させろ。🍖

#ポジデブBot #DEVPARADE""",

    f"""5人で焼肉屋に行くと、
店主の目が輝く。

客単価、確実に5倍。
俺たちは外食産業を支えている。

感謝しろ、経済。🍖

#DEVPARADE #デブパレード""",

    f"""「食べたら太る」

太らなかったら
食った意味ないだろ。

体に栄養が吸収されてる証拠。
お前の体、ちゃんと機能してる。
おめでとう。🍖

#ポジデブBot #DEVPARADE""",

    # ===== 🤘 バンドストーリー系 =====
    f"""2008年、ソニーのオフィスで
プロデューサーに言われた。

「君たち、見た目のインパクトすごいね」

ありがとう。
90kg × 5人 = 450kgのインパクト。
軽いバンドには出せない重厚感。🍖

{SITE_URL}
#DEVPARADE #デブパレード""",

    f"""NARUTOのエンディング「バッチコイ!!!」

全員90kg超のバンドが
忍者アニメのテーマ歌ってるの、
今考えると異常なんだけど、

だからこそ世界で覚えられてる。🍖

{SITE_URL}
#DEVPARADE #バッチコイ""",

    f"""2011年。
メンバーがダイエットに成功して解散。

バンド史上、最も意味不明な解散理由。

2026年。
全員リバウンドして復活。

バンド史上、最も美しい復活劇。🍖

#DEVPARADE #デブパレード""",

    f"""HEY!HEY!HEY!で松本人志に
「お前ら全員デカいな」って言われた。

あの松ちゃんが驚いた。
あの松ちゃんを驚かせた。

これ、履歴書に書ける。🍖

#DEVPARADE #バッチコイ""",

    f"""SUMMER SONIC 2009。
ステージの床が軋んだ。

たぶん俺たちのせい。
でもバンドの音はもっとデカかった。

重さで勝ち、音でも勝つ。
それがDEV PARADE。🍖

#DEVPARADE #デブパレード""",

    f"""DEV PARADE = Def Leppardのパロディ。

Def Leppardは「Heavy Metal」。
DEV PARADEは「Heavy Metabo」。

本家より重い。物理的に。🍖

#DEVPARADE #デブパレード""",

    # ===== 💎 哲学・メッセージ系 =====
    f"""「痩せたら人生変わる」

いや、太ったまま人生変えろ。

その方がかっこいい。
その方がロック。
その方が、DEV PARADE。🍖

#ポジデブBot #DEVPARADE""",

    f"""体型で人を判断する世界がおかしい。
体型で人を判断する目がおかしい。

俺たちは90kg超の体で
全国ツアーやって
メジャーデビューして
NARUTO歌った。

やれることやってから判断しろ。🍖

#DEVPARADE #デブパレード""",

    f"""ダイエットの語源は
ギリシャ語の「diaita」＝「生き方」。

つまり本来は痩せることじゃなく、
「どう生きるか」って話。

俺の生き方: 食って歌って生きる。
完璧なダイエット。🍖

#ポジデブBot #DEVPARADE""",

    f"""自分の体を好きになれない人へ。

俺も昔はそうだった。
でも90kgの体でステージに立って
歓声もらった時に気づいた。

体のせいじゃない。
体を言い訳にしてた自分のせいだった。

体を変えるな。考え方を変えろ。🍖

#ポジデブBot #DEVPARADE""",

    f"""「太ってるのに自信あるね」
って言われた。

「太ってるから自信あるんだよ」
って返した。

この切り返し、使っていいよ。
著作権フリー。🍖

#DEVPARADE #デブパレード""",

    # ===== 📊 データ・リスト系（バズりやすい形式） =====
    f"""デブが得する場面TOP5

1. 風で飛ばされない
2. 相席で相手が食い負ける
3. 秋冬のコート代が浮く（自前の脂肪コート）
4. サウナで一番汗かける
5. 「最近痩せた？」で無限に喜べる

#ポジデブBot #DEVPARADE""",

    f"""💪 重量級ミュージシャン名鑑

🎤 Notorious B.I.G. — HIP HOP GOAT
🎸 B.B. King — Blues界の王
🎹 Barry White — 低音の帝王
🎤 Big Pun — 最強のリリシスト
🎸 DEV PARADE — 全員90kg超

重い音楽は、重い奴が作る。🍖

#DEVPARADE""",

    f"""DEV PARADEの経済効果

🍖 焼肉屋 → 売上200%
🍖 スポーツジム → 売上0%
🍖 大きいサイズ専門店 → 顧客ロイヤリティMAX
🍖 体重計メーカー → 耐荷重テストに貢献

社会貢献してる。🍖

#DEVPARADE #デブパレード""",

    # ===== 🌏 海外向け / English =====
    f"""Band rule: You MUST weigh over 90kg to join.

We had a member who lost weight.
So the band broke up.

15 years later, everyone gained it back.
Band reunited.

This is a true story. This is DEV PARADE. 🍖

{SITE_URL}
#DEVPARADE #BodyPositive""",

    f"""Biggie was big. He became a legend.
Big Pun was big. He became a legend.
Action Bronson is big. He's a legend.

DEV PARADE? All 5 members over 90kg.
We're writing our own legend. 🍖

#DEVPARADE #BodyPositive""",

    f"""Your weight doesn't define your talent.
Your body doesn't limit your dreams.
Your size doesn't reduce your worth.

We're 5 musicians, all 90kg+.
Major label deal with Sony.
NARUTO ending theme.
Proof. 🍖

#DEVPARADE #BodyPositive""",

    # ===== 🔥 議論・バイラル狙い =====
    f"""正直に言う。

「デブは自己管理ができない」
これ、差別な。

5人で15年間バンド続けて
メジャーデビューした俺たちのどこが
自己管理できてない？

管理してるものが違うだけだ。
俺たちは音楽を管理してる。🍖

#DEVPARADE #ポジデブBot""",

    f"""日本で一番体重が重いバンドは
たぶん俺たち。

5人で全員90kg超。
合計体重は企業秘密。

でも日本で一番
「デブで良かった」と思ってるバンドは
間違いなく俺たち。🍖

#DEVPARADE #デブパレード""",

    f"""「太ってるのにバンドやってるの？」

逆に聞くけど、
痩せてたらバンドやれるの？

体重と音楽は関係ない。
でも俺たちは
体重を音楽にした。

関係なくしたのに、
関係あるものにした。
ややこしいけど、最高だろ。🍖

#DEVPARADE #バッチコイ""",

    # ===== 💬 参加型・エンゲージメント系 =====
    f"""【投票】

デブの特技で一番強いのは？

🔥 冬でも半袖（自家発熱）
💪 満員電車で押し負けない（物理）
🍖 食レポの説得力（信頼の体型）
🫂 ハグの包容力（もはや布団）

リプで教えて🍖

#DEVPARADE #ポジデブBot""",

    f"""お前の今日の晩飯を
リプで教えてくれ。

DEV PARADE名義で
全力で「最高」って肯定する。

コンビニ弁当でもカップ麺でも
焼肉でも寿司でも。

食ってる時点で最高。🍖

#DEVPARADE #ポジデブBot""",

    f"""いいねした人、
全員「かっこいいデブ」認定します。

痩せてる人がいいねしても認定します。
かっこいいデブはマインドの問題。

体型じゃなく生き様。🍖

#DEVPARADE #ポジデブBot""",

    f"""RTした人に
DEV PARADEメンバーが
ランダムで1人ポジデブメッセージ送ります。

嘘です。手が回りません。
でも心の中で全員肯定してます。

全員90kg超の愛を受け取れ。🍖

#DEVPARADE #ポジデブBot #拡散希望""",

    # ===== 🎭 シュール / 不条理系（バズ狙い） =====
    f"""デブあるある:

地面「重い…」
椅子「軋む…」
ベッド「沈む…」
地球「引力強めときます」

全ての物質が俺を求めてる。
モテ期、到来。🍖

#DEVPARADE #デブパレード""",

    f"""今日のスケジュール:

7:00 起床（重い）
7:30 朝食（しっかり）
12:00 昼食（たっぷり）
15:00 おやつ（当然）
19:00 夕食（本気）
23:00 夜食（仕上げ）
24:00 就寝（満足）

完璧な1日。隙がない。🍖

#ポジデブBot #DEVPARADE""",

    f"""痩せてる人にしかできないこと:
・狭い隙間を通れる

デブにしかできないこと:
・冬暖かい
・ハグが最強
・存在感がある  
・食レポに説得力
・NARUTOのED歌える（※DEV PARADEに限る）

勝ってる。圧倒的に。🍖

#DEVPARADE #バッチコイ""",
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
    """日付+時間帯ベースでツイートを選択（1日3回、全て別のツイート）"""
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    today = now.strftime("%Y-%m-%d")
    hour = now.hour
    n = len(DAILY_TWEETS)

    # 日付のハッシュで基準インデックスを決定
    day_seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    base = day_seed % n

    # 時間帯ごとにオフセットを加算（必ず4つとも別になる）
    if hour < 10:
        slot = "morning"
        offset = 0
    elif hour < 15:
        slot = "noon"
        offset = n // 4        # 1/4ずらす
    elif hour < 19:
        slot = "evening"
        offset = (n * 2) // 4  # 2/4ずらす
    else:
        slot = "night"
        offset = (n * 3) // 4  # 3/4ずらす

    index = (base + offset) % n
    print(f"Time slot: {slot} (index: {index}/{n})")
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
