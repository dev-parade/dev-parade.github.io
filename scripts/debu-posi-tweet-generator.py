#!/usr/bin/env python3
"""
PosiDev Daily Tweet - 毎日のポジデブ自動投稿

曜日・時間帯に応じてバリエーション豊かなポジデブツイートを自動投稿。
30日以上被らないよう十分なテンプレートを用意。
"""

import os
import json
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

# ===== 追加ツイートの読み込み =====
try:
    from extra_tweets import EXTRA_TWEETS
except ImportError:
    try:
        from scripts.extra_tweets import EXTRA_TWEETS
    except ImportError:
        EXTRA_TWEETS = []

try:
    from extra_tweets_2 import EXTRA_TWEETS_2
except ImportError:
    try:
        from scripts.extra_tweets_2 import EXTRA_TWEETS_2
    except ImportError:
        EXTRA_TWEETS_2 = []

try:
    from extra_tweets_3 import EXTRA_TWEETS_3
except ImportError:
    try:
        from scripts.extra_tweets_3 import EXTRA_TWEETS_3
    except ImportError:
        EXTRA_TWEETS_3 = []

# ===== 日替わりポジデブツイート =====
DAILY_TWEETS_BASE = [
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

    # ===== 🌐 DEVの二重性ネタ =====
    f"""DEV PARADEの"DEV"、

🇯🇵 日本語 → デブ（FAT）
🇺🇸 英語 → Developer（開発者）

どっちも正解。
俺たちはデブであり、クリエイターでもある。

開発するのは、デブの新しい価値観。🍖

#DEVPARADE #デブパレード""",

    f"""英語圏の人が"DEV PARADE"を見ると
「開発者たちのパレード」だと思うらしい。

実際にはメンバー全員90kg超の
デブのパレードなんだけど、

「重厚なものを生み出す集団」
って意味では合ってる。

俺たちが生み出すのは音楽と脂肪。🍖

#DEVPARADE""",

    f"""DEV = Developer（開発者）
DEV = デブ（90kg超）

つまり DEV PARADE は
「開発者のパレード」であり
「デブのパレード」でもある。

シリコンバレーでも通じる。
焼肉屋でも通じる。
最強のバンド名。🍖

#DEVPARADE #デブパレード""",

    f"""IT業界で"dev"って言ったら開発者。
日本で"デブ"って言ったら俺たち。

どっちも何かを生み出す存在。

開発者はコードを書く。
俺たちは歴史を書く。
あと脂肪も書く（体に）。🍖

#DEVPARADE #デブパレード""",

    f"""Fun fact:

"DEV PARADE" in English sounds like
"A parade of developers/creators."

In Japanese, it sounds like
"A parade of fat guys."

Both are true.
We create music. We are fat.
Proudly both. 🍖

#DEVPARADE #BodyPositive""",

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

    # ===== 💘 恋愛 / モテ系 =====
    f"""「デブはモテない」

嘘だね。

俺たちのライブ、
最前列は女性ファンで埋まる。

90kg超の男5人が
汗だくでステージに立つ姿は
「かわいい」らしい。

もう意味わかんないけど、モテてる。🍖

#DEVPARADE #デブパレード""",

    f"""デブの彼氏/旦那がいる人、
聞いたことあるでしょ。

「冬、あんたがいると暖房いらない」

それ、最高の愛の言葉だからな。
俺たちは人間暖房。エコ。🍖

#ポジデブBot #DEVPARADE""",

    f"""デブのハグって知ってる？

包まれる面積が広い。
体温が高い。
柔らかい。
安心感が異常。

ハグの世界大会があったら
俺たちが優勝する自信ある。🍖

#DEVPARADE #デブパレード""",

    # ===== 🏢 ビジネス / 成功哲学系 =====
    f"""成功者にデブは多い。

スティーブ・ウォズニアック → デブ
ジャック・ブラック → デブ
マツコ・デラックス → デブ
秋元康 → デブ

太ってる暇があるってことは、
余計なことで悩んでないってこと。

脳のリソースが本業に全振り。🍖

#DEVPARADE""",

    f"""会社で「存在感がない」と悩んでる人、

太れ。

物理的に存在感が出る。
会議室に入っただけで空気が変わる。
プレゼンは声より体で語れ。

これ、最短のキャリアアップ術。🍖

#ポジデブBot #DEVPARADE""",

    f"""名刺交換で覚えてもらえないって？

90kgになれ。
一発で覚えてもらえる。

ビジネスの基本は「印象に残ること」。
俺たちは名刺を渡す前に勝ってる。🍖

#DEVPARADE #デブパレード""",

    # ===== 🕐 時間帯特化（早朝/深夜） =====
    f"""朝7時にこのツイートを見てるデブへ。

偉い。起きてる。
その体を起こすだけで
痩せてる人の3倍のエネルギーを使ってる。

今日もすでに3倍頑張ってる。
おはよう。🍖

#ポジデブBot #DEVPARADE""",

    f"""深夜にスマホ見てるデブへ。

わかる。腹減ったよな。

食え。
明日の朝後悔するかもしれないけど、
今夜の幸福は本物だ。

DEV PARADEが深夜の空腹を全力肯定。🍖

#DEVPARADE #デブパレード""",

    f"""午前3時のラーメンは
背徳感があるほど美味い。

背徳感はカロリーゼロだから
実質ヘルシー。

この理論に反論できる奴いる？🍖

#ポジデブBot #DEVPARADE""",

    # ===== 🔄 反論 / 切り返し系 =====
    f"""「痩せた方がいいよ」

返し:「お前も黙った方がいいよ」

使っていいよ。無料。🍖

#DEVPARADE #デブパレード""",

    f"""「よく食べるね〜」

返し:「うん、人生楽しんでる」

「運動しないの？」

返し:「この体重で生きてるのが運動」

全部ポジティブに返せ。
それがデブの知性。🍖

#ポジデブBot #DEVPARADE""",

    f"""「そんなに食べて大丈夫？」

大丈夫じゃなかったら
とっくに食べてない。

大丈夫だから食べてる。
体が求めてるから食べてる。

心配してくれてありがとう。
でも俺は大丈夫。絶好調。🍖

#DEVPARADE #デブパレード""",

    f"""「デブは自分に甘い」

違う。自分に正直なだけ。

食べたい時に食べ、
休みたい時に休み、
歌いたい時に歌う。

自分に嘘をつかない生き方、
それを甘いとは言わない。🍖

#ポジデブBot #DEVPARADE""",

    # ===== 👤 メンバーエピソード系 =====
    f"""ハンサム判治（Vo.）の名言:

「ハンサムは体重じゃない。生き様だ」

本名に「ハンサム」って入ってて
体重90kg超。

矛盾してるようで全く矛盾してない。
かっこいいは見た目じゃない。🍖

#DEVPARADE #デブパレード""",

    f"""COYASS（MC）は歯科医師で歯学博士。

患者:「先生、太ってますね」
COYASS:「歯は細いから大丈夫です」

この返し、医学部では教えてくれない。🍖

#DEVPARADE #デブパレード""",

    f"""ugazin（Gt.）の太い指で
繊細なギターソロを弾く。

太い指 × 細い弦 = 奇跡の音色。

相性が悪いはずなのに最高の音が出る。
人生もそういうもん。🍖

#DEVPARADE #デブパレード""",

    f"""TAH（Dr.）のバスドラムは
一度踏んだら元の形に戻らない。

楽器に歴史を刻む男。
それを「破壊」と呼ぶか「芸術」と呼ぶか。

俺たちは「ヘヴィメタボ」と呼ぶ。🍖

#DEVPARADE #デブパレード""",

    f"""ぺー（Ba.）は2026年加入の新メンバー。

加入条件: 90kg以上。演奏力。デブの誇り。

オーディションで体重計に乗った瞬間、
合格が決まった。

実力は後から確認した。
順番おかしいけど、正しい。🍖

#DEVPARADE #デブパレード""",

    # ===== 🌸🎆 季節ネタ拡充 =====
    f"""春のデブ:

桜が散る。
花びらが体に当たる面積が広い。
つまり、桜を一番楽しめる体型。

春はデブの季節。🍖

#ポジデブBot #DEVPARADE""",

    f"""夏のデブ:

暑い。とにかく暑い。
存在するだけで3度上がる。

でもプールに入った時の浮力は最強。
俺たちは沈まない。物理的にも精神的にも。🍖

#DEVPARADE #デブパレード""",

    f"""秋のデブ:

食欲の秋。
デブにとっては年中が食欲の秋なんだけど、
公式に「食っていい季節」が来たのは嬉しい。

堂々と食え。秋だから。🍖

#ポジデブBot #DEVPARADE""",

    f"""冬のデブ:

ダウンジャケットいらない。
自前のダウン（脂肪）装備済み。

暖房費も節約。
エコな体型、デブ。🍖

#DEVPARADE #デブパレード""",

    # ===== 🎯 ワンライナー追加（キレ重視） =====
    f"""重力は俺を愛してる。
毎日離さないでくれる。🍖

#DEVPARADE""",

    f"""体重は秘密。
でも才能は公開中。🍖

{SITE_URL}
#DEVPARADE #デブパレード""",

    f"""ベルトの穴を増やすのは
「成長」って呼ぶんだぞ。🍖

#ポジデブBot #DEVPARADE""",

    f"""エレベーター、定員7名。
俺たちが乗ると定員4名。

特別扱い。VIP。🍖

#DEVPARADE #デブパレード""",

    f"""「最近どう？」

横にデカい。🍖

#DEVPARADE""",

    f"""体脂肪率は測らない。
夢の達成率だけ測る。🍖

#ポジデブBot #DEVPARADE""",

    f"""腹筋は割れてない。
でも常識は割ってきた。🍖

#DEVPARADE #デブパレード""",

    f"""「一日一食にしてる」って言う人いるけど、
俺は一食を一日かけて食べてる。

アプローチが違うだけ。
結果は同じ。…ではない。🍖

#ポジデブBot #DEVPARADE""",

    # ===== 🧠 知識 / トリビア系 =====
    f"""マリリン・モンローは
当時の基準では「ぽっちゃり」だった。

でも世界一セクシーだった。

美の基準なんて時代で変わる。
今の基準が正しいとは限らない。

自分を基準にしろ。🍖

#ポジデブBot #DEVPARADE""",

    f"""力士の体脂肪率は実は23%前後。
見た目ほど脂肪じゃない。

つまりデブに見えても
中身は筋肉の塊ってこと。

俺たちも…たぶん…そう…。
（確認はしてない）🍖

#DEVPARADE #デブパレード""",

    f"""赤ちゃんはみんなぽっちゃり。
人間は太った状態で生まれてくる。

つまり太ってるのが
人間の「デフォルト」。

痩せてる方が「カスタム」。
俺たちはデフォルト。安定。🍖

#ポジデブBot #DEVPARADE""",

    # ===== 🎵 音楽 × デブ =====
    f"""ライブハウスに入った瞬間、

「あ、デブのバンドだ」

って空気になる。

でも1曲目が始まった瞬間、

「あ、かっこいいバンドだ」

に変わる。

その瞬間のために俺たちは生きてる。🍖

#DEVPARADE #バッチコイ""",

    f"""「バッチコイ!!!」って叫ぶ時、
腹から声が出る。

腹がデカいから、声もデカい。
面積で勝ってる。共鳴で勝ってる。

デブは楽器。
体全体が楽器。🍖

#DEVPARADE #バッチコイ""",

    f"""楽器の重さランキング:

ギター: 約4kg
ベース: 約5kg
ドラムセット: 約30kg
DEV PARADEメンバー: 90kg超

メンバーが一番重い。
でもメンバーが一番いい音出す。🍖

#DEVPARADE #デブパレード""",

    # ===== 🤝 ボディポジティブ / メッセージ =====
    f"""太ってる人も、
痩せてる人も、
普通の人も、

全員、自分の体で生きてるだけで偉い。

ただ、俺たち90kg超の人間は
「生きてるだけでエネルギー消費量が多い」
ので、ちょっとだけ余分に偉い。🍖

#ポジデブBot #DEVPARADE""",

    f"""ボディポジティブって言葉が
流行る前から、

俺たちは90kgの体で
ステージに立ってた。

トレンドじゃない。
ライフスタイルだ。🍖

#DEVPARADE #デブパレード""",

    f"""誰かに「太ってるね」と言われたら、
こう思え。

「俺のこと見てるじゃん」

見られてる時点で勝ち。
存在感の証明。🍖

#ポジデブBot #DEVPARADE""",

    # ===== 🔥 追加ワンライナー =====
    f"""全員が痩せた世界より、
全員が自分を好きな世界の方が
絶対にいい。

俺は後者を選ぶ。🍖

#DEVPARADE #ポジデブBot""",

    f"""ジムに行く暇があったら
ライブに来い。

2時間暴れたら
ジムより痩せる。

…痩せたくないけど。🍖

#DEVPARADE #バッチコイ""",

    f"""「第一印象は3秒で決まる」

90kg超が入ってきたら
0.5秒で決まる。

スピード勝負でも勝ってる。🍖

#DEVPARADE #デブパレード""",

    f"""飛行機のシートベルトが
ギリギリ閉まった時の達成感。

これを知らない人は
人生の半分損してる。🍖

#ポジデブBot #DEVPARADE""",

    f"""Google検索:
「デブ メリット」

検索結果:
DEV PARADE公式サイト

全ての答えはここにある。🍖

{SITE_URL}
#DEVPARADE #デブパレード""",

    f"""俺たちの合言葉:

食え。歌え。太れ。
そして、愛されろ。

DEV PARADE。🍖

{SITE_URL}
#DEVPARADE #バッチコイ""",

    # ===== 🎶 歌詞ネタ / バンドファクト系 =====
    f"""冬なのに半袖。
冬なのに半ズボン。
冬なのにサンダル。

寒くないの？って聞かれる。

寒いわけない。
90kg超の体は常時発熱中。
俺たちにとって冬は「やや涼しい夏」。🍖

#DEVPARADE #デブパレード""",

    f"""「夏はまだ終わらない」

DEV PARADEの体温的には
12月でもまだ夏。
2月でもまだ夏。

年中夏。
俺たちに秋冬はない。
あるのは夏と、もっと夏だけ。🍖

#DEVPARADE #デブパレード""",

    f"""1月。雪が降ってる。

ハンサム判治: 半袖
COYASS: 半袖
ugazin: 半袖
ぺー: 半袖
TAH: 半袖

全員半袖。

通行人が二度見する。
でも俺たちは涼しい顔してる。

嘘。暑い。🍖

#DEVPARADE #デブパレード""",

    f"""冬のDEV PARADE装備:

一般人: ダウンジャケット+マフラー+手袋
俺たち: Tシャツ1枚

それで汗かいてる。

「寒くないの？」
「暑い」

季節感を超越した存在、DEV PARADE。🍖

#DEVPARADE""",

    f"""結成時のメンバー合計体重: 約570kg。

570kg。

軽自動車より重い。
バンドごと走れる。🍖

#DEVPARADE #デブパレード""",

    f"""TAH（Dr.）の2008年時点の体重: 146kg。

146kg。

ドラムを叩いてるのか、
ドラムがTAHに叩かれてるのか。

どっちにしろ、
あの音は146kgじゃないと出ない。🍖

#DEVPARADE #デブパレード""",

    f"""12月の渋谷。
みんなコートを着てる。

俺たちだけ半袖。
しかもちょっと汗かいてる。

「寒くないんですか？」

冬なのに半袖。
冬なのに半ズボン。
冬なのにサンダル。

これがDEV PARADEの冬。🍖

#DEVPARADE #バッチコイ""",

    f"""衣替えの季節。

一般人:「そろそろ長袖かな」
DEV PARADE:「まだ半袖でいける」

一般人:「もうコートだよね」
DEV PARADE:「まだ半袖でいける」

一般人:「雪降ってるけど」
DEV PARADE:「まだ半袖でいける」

夏は終わらない。俺たちの中では。🍖

#DEVPARADE""",

    f"""ライブのMCで
COYASSが言った名言:

「みんな暑い？
俺たちはステージに立つ前から暑い。
生きてるだけで暑い。
存在が熱い。」

物理的にも比喩的にも正しい。🍖

#DEVPARADE #バッチコイ""",

    f"""DEV PARADEの夏の過ごし方:

暑い→いつもと変わらない
汗かく→いつもと変わらない  
冷房ほしい→いつもと変わらない

俺たちにとって夏は平常運転。
むしろ世界が俺たちに追いついた季節。🍖

#DEVPARADE #デブパレード""",
    # ===== 🎤 楽曲パンチライン系（バッチコイ!!! / GODS N' DEATH / ME★TA★BO） =====
    f"""DEV PARADEの歌詞:

「全ての武器をお箸にするぜ」

戦争なんかいらない。
俺たちに必要なのは箸だけ。

世界平和は食卓から始まる。🍖

#DEVPARADE #バッチコイ""",

    f"""DEV PARADEの名言:

「お寿司はデザート」

— バッチコイ!!!より

異論は認めない。
寿司はデザート。
これは公式見解。🍖

#DEVPARADE #バッチコイ""",

    f"""「おにぎりくれる奴、だいたい友達」

— DEV PARADE「バッチコイ!!!」

これ以上シンプルで
これ以上正確な
友情の定義を知らない。🍖

#DEVPARADE #バッチコイ""",

    f"""どんなにハングリーでも
どんなにアングリーでも

ドンブリ食ってダンシング！

これがDEV PARADEの人生哲学。
悩んだら食え。食ったら踊れ。🍖

#DEVPARADE #バッチコイ""",

    f"""「牛丼でドンクライ
スパゲッチュでゲッチュー
ロースはお野菜
カレーライスは飲みきり」

— DEV PARADE「バッチコイ!!!」

全ての食を肯定する歌詞。
NARUTOのEDでこれ流れてた。
すごい時代。🍖

#DEVPARADE #バッチコイ""",

    f"""「キミの涙の理由(ワケ)、
きっとお腹が空いているだけ」

— DEV PARADE「GODS N' DEATH」

泣いてる人がいたら
まず飯を食わせろ。

これが医学より確実な処方箋。🍖

#DEVPARADE""",

    f"""「カレーを飲ませろ」

— DEV PARADE「GODS N' DEATH」

カレーは食べるものじゃない。
飲むもの。

この事実を世界に広めたい。🍖

#DEVPARADE""",

    f"""「メシを食わせろ、欲望のまま。
神の恵みか？死神の罠？」

— DEV PARADE「GODS N' DEATH」

食欲は神と死神の間にある。
でも俺たちは迷わず食う側。🍖

#DEVPARADE""",

    f"""「腹がへっては戦は出来ん、
なんて嘘。
これが怒りの原因」

— DEV PARADE「GODS N' DEATH」

空腹は怒りの元。
つまり食えば世界は平和になる。
ノーベル平和賞ください。🍖

#DEVPARADE""",

    f"""「脂肪に見えるの？
これは貫禄」

— DEV PARADE「ME★TA★BO」

これ以上の切り返しが
この世にあるだろうか。

無い。🍖

#DEVPARADE #デブパレード""",

    f"""「君を包み込む愛の弾力。
優しさを目いっぱい詰めたさ」

— DEV PARADE「ME★TA★BO」

脂肪じゃない。
愛の弾力。
優しさの詰め合わせ。

太ってる人をハグすると
わかる。これ、本当。🍖

#DEVPARADE""",

    f"""「自慢じゃないが、俺は肥満さ」

— DEV PARADE「ME★TA★BO」

この1行で全てが伝わる。
誇りと開き直りと
ユーモアが完璧に同居してる。

これがDEV PARADEのスピリット。🍖

#DEVPARADE #デブパレード""",

    f"""「人は肉まんだろう？」

— DEV PARADE「ME★TA★BO」

哲学。

ソクラテスも言わなかった。
デカルトも言わなかった。
DEV PARADEが言った。🍖

#DEVPARADE #デブパレード""",

    f"""EVERYBODY FAT ME
EVERYBODY FAT YOU

— DEV PARADE「ME★TA★BO」

みんな太ってる。
みんな太っていい。

世界一シンプルな
ボディポジティブ宣言。🍖

#DEVPARADE #デブパレード""",

    f"""「何が何でも
あーでもこーでも
諦めるな」

— DEV PARADE「バッチコイ!!!」

デブが言うと説得力が違う。
だって俺たち、
ダイエットは諦めたけど
夢は諦めなかった。🍖

#DEVPARADE #バッチコイ""",

    # ===== 🎤 楽曲パンチライン系（うっちゃりFUNK / ダブルベッド / タチアガレ / 夏の終わりに / パルフェ） =====
    f"""「No Meat! No Life!
おなかにつまった夢と希望と愛」

— DEV PARADE「うっちゃりFUNK」

俺たちの腹は
脂肪じゃない。
夢と希望と愛が詰まってる。

CT撮っても映らないけど。🍖

#DEVPARADE #デブパレード""",

    f"""「お太り様ですか？
ある意味サイズ的にお二人様分」

— DEV PARADE「うっちゃりFUNK」

レストランで1人で予約して
2人分の席をキープする男。

それがDEV PARADE。🍖

#DEVPARADE""",

    f"""「満たされたお腹は
心も満たされ I'm So FAT」

— DEV PARADE「うっちゃりFUNK」

FAT = 満たされた。
最高の自己肯定。

腹が満たされれば
心も満たされる。
真理。🍖

#DEVPARADE""",

    f"""「学校じゃ教えてくれない
１００点より上の取り方」

— DEV PARADE「うっちゃりFUNK」

100点の取り方は学校で教わる。
100kgの超え方は
DEV PARADEが教える。🍖

#DEVPARADE #デブパレード""",

    f"""「母1人子肥り
かあさん、ありGETS YOU」

— DEV PARADE「うっちゃりFUNK」

母の愛で育ち、
母の飯で太った。

全ての太ったお前は
母親の愛の結晶。🍖

#DEVPARADE""",

    f"""「キミが隣に眠らないから
ボクは体をふくらませた」

— DEV PARADE「ダブルベッド」

寂しさで食べて太った。
つまり太ってる人は
愛が深い人。

異論は認めない。🍖

#DEVPARADE #デブパレード""",

    f"""「ダブルベッドなのに
一人でいっぱいなのさ」

— DEV PARADE「ダブルベッド」

切ない。
けど笑える。
けど切ない。

このバランスが
DEV PARADEの真骨頂。🍖

#DEVPARADE""",

    f"""「君がいなくて俺はふくらんだ。
君への想いがまたふくらんだ」

— DEV PARADE「ダブルベッド」

体も想いも
ふくらんだ。

これ、ラブソングの歴史で
前例がない切なさ。🍖

#DEVPARADE""",

    f"""「痩せているとか太ってるとか
肌の色とか関係ないさ」

— DEV PARADE「タチアガレ」

体重90kg超の男5人が
これを歌うから説得力がある。

言葉じゃなく存在で語る。🍖

#DEVPARADE""",

    f"""「君の弱さ、他人の個性、
受け入れるのが真の強さだってさ」

— DEV PARADE「タチアガレ」

デブを受け入れた俺たちは
真の強さを手に入れた。

タチアガレ。コブシ挙げて。🍖

#DEVPARADE #バッチコイ""",

    f"""「憧れのシルエット、
俺は比較的丸くて。
心も丸くなった今なら伝えれる」

— DEV PARADE「夏の終わりに」

体型が丸い。
心も丸い。
全部丸い。
それでいい。🍖

#DEVPARADE #デブパレード""",

    f"""「インスタグラムより100キログラム
TIKTOKよりビーフとポーク」

— DEV PARADE「パルフェ」

このパンチライン以上の
パンチラインを
俺はまだ知らない。🍖

#DEVPARADE #デブパレード""",

    f"""「AIより愛。マニュアルなしさ」

— DEV PARADE「パルフェ」

2026年、AIの時代に
デブが歌う「AIより愛」。

重い。深い。太い。
全部褒め言葉。🍖

#DEVPARADE""",

    f"""「デブは甘え？ バカめ。
おもいっきり甘えていいんだぜ」

— DEV PARADE「パルフェ」

甘えろ。
甘いもの食え。
人に甘えろ。

甘えることを
恥じるな。🍖

#DEVPARADE #デブパレード""",

    f"""「最高さ、震える脂肪細胞が。
内臓が喜ぶ魅力は異常さ」

— DEV PARADE「パルフェ」

脂肪細胞が震える曲を
作れるバンドは世界に
DEV PARADEだけ。🍖

#DEVPARADE""",

    # ===== 🎤 楽曲パンチライン系（100CAN DIVE / 万年FAT / HAPPY！乱デブー / メシ食わせろ / 自転車） =====
    f"""「6パックから1パック。逆ライザップ」

— DEV PARADE「100CAN DIVE」

世の中ライザップで痩せる人ばかり。
俺たちは逆を行く。

トレンドに逆らう勇気。
これがロック。🍖

#DEVPARADE #デブパレード""",

    f"""「ポジティブな肥満師」

— DEV PARADE「100CAN DIVE」

肥満師。
師って付いてる。
もはや職業。もはや称号。

弟子も募集中。🍖

#DEVPARADE""",

    f"""「尿酸値、高いけど超ダンディ」

— DEV PARADE「100CAN DIVE」

健康診断の数値は赤字。
ダンディズムは黒字。

トータルでプラス。🍖

#DEVPARADE #デブパレード""",

    f"""「あきらかに負け戦だとしても
友よ闘え、明日の為に」

— DEV PARADE「100CAN DIVE」

体重計との戦いは毎日負け戦。
でも俺たちは明日も闘う。

100CAN DIVE！🍖

#DEVPARADE #バッチコイ""",

    f"""「肥満は文化」

— DEV PARADE「何年経っても万年FAT」

この4文字に全てが詰まってる。

文化遺産に登録してくれ。🍖

#DEVPARADE #デブパレード""",

    f"""「まだ食べたい。まだ飲みたい。
もう眠たい。」

— DEV PARADE「何年経っても万年FAT」

人間の三大欲求を
最もシンプルに表現した歌詞。

ノーベル文学賞候補。🍖

#DEVPARADE""",

    f"""「食っては悔いて、悔いては食って」

— DEV PARADE「何年経っても万年FAT」

人類の永遠のループ。
でも俺たちは
「悔い」の部分を削除した。

食って、食って、食う。🍖

#DEVPARADE""",

    f"""「照らすミラーボール、
俺、体型がミートボール」

— DEV PARADE「HAPPY！乱デブー」

ミラーボールとミートボール。
韻がやばい。
体型もやばい。🍖

#DEVPARADE #デブパレード""",

    f"""「食べれないほどアイニージュー」

— DEV PARADE「HAPPY！乱デブー」

「食べれないほど」って
DEV PARADEが言うと
相当な愛の深さ。🍖

#DEVPARADE""",

    f"""「生きる為に食べてなくて、
食べる為に生きてる」

— DEV PARADE「メシ食わせろ」

人生の目的が明確な男たち。

食べる為に生きる。
この潔さ。🍖

#DEVPARADE #デブパレード""",

    f"""「メシを喰わせろ。腹が減ったぞ。
メシを喰わせろ。痩せちまうだろ」

— DEV PARADE「メシ食わせろ」

「痩せちまうだろ」って
脅し文句が他のバンドと
方向性違いすぎて最高。🍖

#DEVPARADE""",

    f"""「LUUPですら100キロ制限体重。
食ったら乗るな」

— DEV PARADE「自転車」

電動キックボードすら
乗れない体重。

でも俺たちには
音楽がある。🍖

#DEVPARADE #デブパレード""",

    f"""「自重が自由うばう地球。
万有引力発見、ニュートン」

— DEV PARADE「自転車」

ニュートンを恨んでる
90kg超のバンド。

引力なかったら
もっと自由だった。🍖

#DEVPARADE""",

    f"""「夜に肥えて行くのさ
ラーメンとか夜食で」

— DEV PARADE「自転車」

夜は太る時間。
でも夜のラーメンは
昼の3倍美味い。

美味さとカロリーは比例する。
これ物理法則。🍖

#DEVPARADE""",

    f"""「サドル、ケツ、空気ぬけ
パンクしやすい。体重による残念」

— DEV PARADE「自転車」

自転車のパンクの原因:

普通の人 → 釘を踏んだ
DEV PARADE → 体重

そういうバンド。🍖

#DEVPARADE #デブパレード""",
]
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

# ===== DAILY_TWEETSを統合 =====
DAILY_TWEETS = DAILY_TWEETS_BASE + EXTRA_TWEETS + EXTRA_TWEETS_2 + EXTRA_TWEETS_3

TWEETS = {
    "launch": LAUNCH_TWEETS,
    "scheduled": DAILY_TWEETS,
    "collab": COLLAB_TWEETS,
}


# ===== 投稿履歴ファイル =====
POSTED_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "posted_tweets.json")


def tweet_hash(text):
    """ツイートのハッシュ値を生成（重複チェック用）"""
    return hashlib.md5(text.strip().encode()).hexdigest()[:12]


def load_posted():
    """投稿済みツイートのハッシュリストを読み込み"""
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"posted": [], "scores": {}, "cycle": 1}


def save_posted(data):
    """投稿済みデータを保存"""
    os.makedirs(os.path.dirname(POSTED_FILE), exist_ok=True)
    with open(POSTED_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def score_tweet(text):
    """ツイートのバズりやすさスコアを算出（0〜100）"""
    score = 50  # 基本スコア

    # --- 長さ（短くてパンチがある方がバズる） ---
    char_count = len(text)
    if char_count <= 80:
        score += 12   # ワンライナーは強い
    elif char_count <= 140:
        score += 8
    elif char_count > 250:
        score -= 5    # 長すぎはマイナス

    # --- エンゲージメント要素 ---
    if "？" in text or "?" in text:
        score += 6    # 質問形式は反応を誘う
    if "リプ" in text or "教えて" in text:
        score += 5    # リプ誘導
    if "RT" in text or "拡散" in text:
        score += 4    # 拡散要請
    if "いいね" in text:
        score += 3    # いいね誘導

    # --- ユーモア指標 ---
    if "。…" in text or "…で" in text or "…は" in text:
        score += 4    # 間の取り方（オチ感）
    humor_words = ["嘘", "違う", "逆に", "実は", "正直", "ないけど", "だけど"]
    for w in humor_words:
        if w in text:
            score += 2
            break

    # --- 反転・ギャップ構造（バズの黄金パターン） ---
    reversal_patterns = ["でも", "→", "じゃない", "じゃなくて", "ではない", "ところが"]
    for p in reversal_patterns:
        if p in text:
            score += 5
            break

    # --- リスト形式（スクロール止め効果） ---
    if text.count("・") >= 3 or text.count("→") >= 3:
        score += 6
    numbered = sum(1 for c in "12345" if f"{c}." in text or f"{c}位" in text)
    if numbered >= 3:
        score += 6

    # --- DEV PARADE固有の強みを活かしてるか ---
    if "NARUTO" in text or "バッチコイ" in text:
        score += 5    # 認知度の高いキーワード
    if "90kg" in text or "全員90" in text:
        score += 3    # コアアイデンティティ
    if "ソニー" in text or "メジャー" in text:
        score += 3    # 実績
    if "HEY!HEY!HEY!" in text or "SUMMER SONIC" in text:
        score += 4    # テレビ/フェス実績

    # --- 絵文字の適度な使用 ---
    emoji_count = sum(1 for c in text if ord(c) > 0x1F000)
    if 1 <= emoji_count <= 4:
        score += 2
    elif emoji_count > 6:
        score -= 2

    # --- 英語ツイート（海外リーチ） ---
    if "#BodyPositive" in text:
        score += 3

    # --- 切り返し系（共感+使える＝保存される） ---
    if "返し:" in text or "使っていいよ" in text or "著作権フリー" in text:
        score += 7

    return min(100, max(0, score))


def select_smart_tweet():
    """スマート選択：上位20%の未投稿ツイートから選ぶ"""
    data = load_posted()
    posted_hashes = set(data.get("posted", []))

    # 全ツイートをスコアリング
    scored = []
    for tweet in DAILY_TWEETS:
        h = tweet_hash(tweet)
        s = score_tweet(tweet)
        scored.append({"text": tweet, "hash": h, "score": s, "posted": h in posted_hashes})

    # 未投稿のみフィルタ
    unposted = [t for t in scored if not t["posted"]]

    # 全部投稿済みならサイクルリセット
    if len(unposted) == 0:
        print(f"🔄 全{len(DAILY_TWEETS)}種を投稿済み → サイクル{data.get('cycle', 1) + 1}へリセット")
        data["posted"] = []
        data["cycle"] = data.get("cycle", 1) + 1
        save_posted(data)
        unposted = scored.copy()
        for t in unposted:
            t["posted"] = False

    # スコア降順ソート
    unposted.sort(key=lambda x: x["score"], reverse=True)

    # 上位20%から選択（最低5個は確保）
    top_count = max(5, len(unposted) // 5)
    top_tweets = unposted[:top_count]

    # 上位グループからランダム選択
    selected = random.choice(top_tweets)

    # スコア分布の表示
    all_scores = [t["score"] for t in scored]
    top_scores = [t["score"] for t in top_tweets]
    print(f"\n📊 ツイートスコアリング:")
    print(f"   全{len(scored)}種 | 投稿済み: {len(posted_hashes)} | 未投稿: {len(unposted)}")
    print(f"   スコア範囲: {min(all_scores)}〜{max(all_scores)} (平均: {sum(all_scores)//len(all_scores)})")
    print(f"   上位20% ({top_count}種): スコア{min(top_scores)}〜{max(top_scores)}")
    print(f"   ✅ 選択: スコア{selected['score']} | ハッシュ: {selected['hash']}")
    print(f"   サイクル: {data.get('cycle', 1)}")

    return selected


def mark_as_posted(tweet_data):
    """ツイートを投稿済みとしてマーク"""
    data = load_posted()
    if tweet_data["hash"] not in data.get("posted", []):
        data.setdefault("posted", []).append(tweet_data["hash"])
    # スコアも記録
    data.setdefault("scores", {})[tweet_data["hash"]] = {
        "score": tweet_data["score"],
        "posted_at": datetime.now(timezone(timedelta(hours=9))).isoformat(),
    }
    save_posted(data)


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
        selected = select_smart_tweet()
        tweet_text = selected["text"]
    else:
        tweets = TWEETS.get(CAMPAIGN, DAILY_TWEETS)
        tweet_text = random.choice(tweets)
        selected = {"text": tweet_text, "hash": tweet_hash(tweet_text), "score": 0}

    print(f"\nCampaign: {CAMPAIGN}")
    print(f"Tweet ({len(tweet_text)} chars):")
    print(tweet_text)

    # 自動投稿
    tweet_id = auto_post(tweet_text)
    auto_posted = tweet_id is not None

    # 投稿済みマーク
    if auto_posted:
        mark_as_posted(selected)
        print("📝 投稿履歴を更新しました")

    # Intent URL
    intent_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet_text)

    # Issue用Markdown
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")
    status = "✅ 自動投稿済み" if auto_posted else "📋 手動投稿待ち"
    tweet_link = f"https://twitter.com/dev_parade/status/{tweet_id}" if tweet_id else ""

    data = load_posted()
    posted_count = len(data.get("posted", []))
    total_count = len(DAILY_TWEETS)
    cycle = data.get("cycle", 1)

    issue_md = f"""## 🍖 ポジデブツイート（スマート選択）

**生成日時:** {now}
**キャンペーン:** {CAMPAIGN}
**ステータス:** {status}
**品質スコア:** {selected['score']}/100
**投稿進捗:** {posted_count}/{total_count}（サイクル{cycle}）
{"**投稿リンク:** " + tweet_link if tweet_link else ""}

---

### ツイート内容（{len(tweet_text)}文字）

```
{tweet_text}
```

---

{"✅ 自動投稿完了！" if auto_posted else "### 👇 ワンクリックで投稿 👇"}

---
🍖 Smart PosiDev Tweet by DEV PARADE
"""

    with open("tweet_issue.md", "w") as f:
        f.write(issue_md)

    print(f"\nIntent URL: {intent_url}")
    print("✅ Issue markdown generated!")


if __name__ == "__main__":
    main()
