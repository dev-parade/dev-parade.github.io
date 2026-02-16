"""
PosiDev Keywords - デブにまつわるキーワード100個+ & ポジデブ変換辞典
日本語 + 英語（世界規模対応）

DEV PARADE流のユーモアとポジティブさで変換。
"""

# ===== 検索用キーワード（Google検索 / メンション検知用） =====
# カテゴリ別に整理。各キーワードに対してポジデブ返信を用意。

KEYWORDS_JA = {
    # ----- 直接的な表現 -----
    "デブ": [
        "DEV（デブ）は才能。俺たち5人で570kg、全員メジャーデビュー済み🍖 #ポジデブ",
        "デブ？ DEV PARADEの入団資格（90kg以上）満たしてるじゃん！おめでとう🍖 #ポジデブ",
        "「デブ」= Delightful Excellent Beautiful。正式名称です🍖 #ポジデブ",
    ],
    "でぶ": [
        "でぶは愛称。DEV PARADEはバンド名にデブ入れて誇ってます🍖 #ポジデブ",
    ],
    "太った": [
        "太った？ それ「成長した」の同義語。細胞レベルで進化してる🍖 #ポジデブ",
        "太った分だけ地球がお前を離したくなくなってる。モテてるぜ、地球に🌍🍖",
    ],
    "太る": [
        "太る＝パワーアップ。RPGで言えばレベルアップだ🍖 #ポジデブ",
    ],
    "太り": [
        "太りは成長の証。570kgバンドDEV PARADEが保証する🍖 #ポジデブ",
    ],
    "ふとった": [
        "ふとった？ 存在感が増したってこと。ステージ映えするぜ🍖 #ポジデブ",
    ],
    "肥満": [
        "肥満じゃない、「豊満」だ。字面もゴージャス🍖 #ポジデブ",
    ],
    "メタボ": [
        "メタボ＝メタル＋ボディ。ロックな体型認定おめでとう🤘🍖 #ポジデブ",
        "俺たち自称「ヘヴィメタボバンド」。メタボは音楽ジャンル🍖 #ポジデブ",
    ],
    "ぽっちゃり": [
        "ぽっちゃり＝やわらかい魅力。包容力がハンパない🍖 #ポジデブ",
    ],
    "おデブ": [
        "おデブ様と呼びなさい。敬称をつけるのがマナー🍖 #ポジデブ",
    ],
    "巨漢": [
        "巨漢は存在感の塊。DEV PARADEのugazinは135kgの巨漢ギタリスト🍖 #ポジデブ",
    ],
    "巨体": [
        "巨体は力の象徴。相撲取りもプロレスラーもみんな巨体で偉大🍖 #ポジデブ",
    ],
    "激太り": [
        "激太り？ 激成長だ。勢いがあっていい🍖 #ポジデブ",
    ],

    # ----- SNSネガティブ表現 -----
    "痩せろ": [
        "痩せる必要？ ないね。俺たち570kgで武道館目指してる💪🍖 #ポジデブ",
        "痩せろ？ お断りだ。DEV PARADEは90kg以上限定🍖 #ポジデブ",
    ],
    "やせろ": [
        "やせろなんて古い価値観。ポジデブが新時代🍖 #ポジデブ",
    ],
    "痩せなきゃ": [
        "痩せなくていい。むしろDEV PARADE入らない？条件は90kg以上🍖 #ポジデブ",
    ],
    "痩せたい": [
        "「痩せたい」→「もっと愛されたい」に変換。大丈夫、そのままで最高🍖 #ポジデブ",
    ],
    "豚": [
        "豚は知能が高く清潔な動物。つまり褒め言葉🍖 #ポジデブ",
    ],
    "ブタ": [
        "ブタは可愛いし美味しい。最高の生き物🍖 #ポジデブ",
    ],
    "太りすぎ": [
        "太りすぎなんてない。充実しすぎてるだけ🍖 #ポジデブ",
    ],
    "醜い": [
        "醜い体なんてない。全部お前という作品の一部🍖 #ポジデブ",
    ],
    "デブ専": [
        "デブ専は審美眼がある。正しい目を持ってる🍖 #ポジデブ",
    ],

    # ----- ダイエット関連 -----
    "ダイエット": [
        "ダイエットの語源は「生き方」。今の生き方、最高じゃん？🍖 #ポジデブ",
    ],
    "糖質制限": [
        "糖質制限より愛情無制限。DEV PARADEが保証する🍖 #ポジデブ",
    ],
    "食べ過ぎ": [
        "食べ過ぎじゃない、幸せ過ぎだ。最高の状態🍖 #ポジデブ",
    ],
    "カロリー": [
        "カロリーは幸せの単位。高カロリー＝高幸福度🍖 #ポジデブ",
    ],
    "体重": [
        "体重は数字。お前の価値じゃない。DEV PARADEが保証する🍖 #ポジデブ",
    ],
    "体重計": [
        "体重計に支配されるな。数字より心の充実🍖 #ポジデブ",
    ],
    "リバウンド": [
        "リバウンドじゃない、カムバックだ。DEV PARADEも15年ぶりにカムバックした🍖 #ポジデブ",
    ],
    "食事制限": [
        "食事制限より笑顔無制限。人生は美味しく楽しく🍖 #ポジデブ",
    ],
    "ドカ食い": [
        "ドカ食いは情熱の表れ。食に対する真剣さ🍖 #ポジデブ",
    ],
    "爆食": [
        "爆食は爆発的なエネルギー補給。ロケット燃料🍖 #ポジデブ",
    ],
    "大食い": [
        "大食いは才能。フードファイターはアスリート🍖 #ポジデブ",
    ],

    # ----- 体型コンプレックス -----
    "体型": [
        "体型は個性。DEV PARADEはメンバー全員90kg以上で誇りに思ってる🍖 #ポジデブ",
    ],
    "二重あご": [
        "二重あご＝顔にクッション装備。安全性が高い🍖 #ポジデブ",
    ],
    "三段腹": [
        "三段腹は三倍の幸せを蓄えてる証拠🍖 #ポジデブ",
    ],
    "ビール腹": [
        "ビール腹は人生楽しんでる証。大人の勲章🍖 #ポジデブ",
    ],
    "腹が出": [
        "腹が出てるんじゃない。夢が詰まってるんだ🍖 #ポジデブ",
    ],
    "お腹": [
        "お腹は幸せの貯金箱。たっぷり貯まってるね🍖 #ポジデブ",
    ],
    "脂肪": [
        "脂肪は努力の結晶。DEV PARADEの公式見解です🍖 #ポジデブ",
    ],
    "体脂肪": [
        "体脂肪率より幸福度を測ろう。そっちの方が大事🍖 #ポジデブ",
    ],
    "贅肉": [
        "贅肉は「贅沢な肉」と書く。つまりプレミアム🍖 #ポジデブ",
    ],
    "セルライト": [
        "セルライトは自然な模様。大理石みたいで高級感ある🍖 #ポジデブ",
    ],
    "中年太り": [
        "中年太りは人生経験の蓄積。深みが違う🍖 #ポジデブ",
    ],
    "コンプレックス": [
        "コンプレックスは武器に変わる。DEV PARADEがその証明🍖 #ポジデブ",
    ],

    # ----- DEV PARADE語録・ポジデブ用語 -----
    "100kg": [
        "100kgはエリート。DEV PARADEの入団資格（90kg以上）クリア🍖 #ポジデブ",
    ],
    "100キロ": [
        "100キロは大台じゃない、金字塔だ🍖 #ポジデブ",
    ],
    "90kg": [
        "90kg以上はDEV PARADE入団資格あり。仲間だ🍖 #ポジデブ",
    ],
    "三桁": [
        "体重三桁は選ばれし者。DEV PARADEのメンバーは全員三桁経験者🍖 #ポジデブ",
    ],
    "痛風": [
        "痛風はグルメの勲章。DEV PARADEメンバー全員痛風ホルダー🍖 #ポジデブ",
    ],
    "XL": [
        "XLは「eXtra Love」の略。愛が溢れてるサイズ🍖 #ポジデブ",
    ],
    "XXL": [
        "XXLは「eXtra eXtra Love」。愛が2倍🍖 #ポジデブ",
    ],
    "大きいサイズ": [
        "大きいサイズは大きな存在感。堂々としていこう🍖 #ポジデブ",
    ],
    "服が入らない": [
        "服が入らないんじゃない。服がお前に追いついてないだけ🍖 #ポジデブ",
    ],
    "サイズがない": [
        "サイズがないのはメーカーの怠慢。お前は悪くない🍖 #ポジデブ",
    ],

    # ----- 感情・状況 -----
    "傷ついた": [
        "傷ついたなら570kgの愛で包んでやる。DEV PARADEはお前の味方🍖 #ポジデブ",
    ],
    "辛い": [
        "辛い時こそポジデブ。焼肉食って元気出そう🍖 #ポジデブ",
    ],
    "悲しい": [
        "悲しい気持ちは俺たちの腹の肉で全部吸収してやる🍖 #ポジデブ",
    ],
    "体型 嫌": [
        "体型が嫌？ 俺たちはメンバー全員90kg以上で誇りに思ってる。見方を変えろ🍖 #ポジデブ",
    ],
    "食べたら太る": [
        "食べたら太る？ 食べなかったら死ぬ。生きてる証拠を太ると呼ぶな🍖 #ポジデブ",
    ],
    "食べちゃった": [
        "食べちゃった？ 正解。お前は今日も生き延びた。おめでとう🍖 #ポジデブ",
    ],
    "夜食": [
        "深夜の夜食は罪じゃない。ご褒美。DEV PARADEが許可する🍖 #ポジデブ",
    ],
    "ストレス食い": [
        "ストレス食いは自己防衛。賢い体の反応だ。責めるな🍖 #ポジデブ",
    ],

    # ----- 痩せすぎ心配系（痩せた人にもポジデブ） -----
    "痩せた": [
        "痩せた？ 心配してるぞ。ちゃんと食ってるか？ 焼肉おごるから連絡くれ🍖 by DEV PARADE #ポジデブ",
        "痩せたって聞いて飛んできた。DEV PARADEが全力で肉を届けたい🍖 #ポジデブ",
    ],
    "痩せすぎ": [
        "痩せすぎは心配。体は大事にしてくれ。一緒に焼肉行こう🍖 by DEV PARADE #ポジデブ",
        "痩せすぎるな。お前が元気でいることが一番大事🍖 #ポジデブ",
    ],
    "やせた": [
        "やせた？ 無理してないか？ 健康が第一。DEV PARADEが心配してるぞ🍖 #ポジデブ",
    ],
    "ガリガリ": [
        "ガリガリも心配になる。ちゃんと食べて元気でいてくれ。肉送るぞ🍖 #ポジデブ",
        "ガリガリだろうがデブだろうが、お前は最高。でも食べてくれ🍖 #ポジデブ",
    ],
    "がりがり": [
        "がりがりはDEV PARADE的に心配。栄養摂ってるか？ 体大事にしろ🍖 #ポジデブ",
    ],
    "食べてない": [
        "食べてない？ それは心配だ。体が資本。まず食え。話はそれからだ🍖 by DEV PARADE #ポジデブ",
    ],
    "食べれない": [
        "食べれない時は無理しなくていい。でもいつでも一緒に食べに行くぞ🍖 #ポジデブ",
    ],
    "拒食": [
        "辛いな。一人で抱え込まないで。DEV PARADEは570kgの愛であなたの味方🍖 #ポジデブ",
    ],
    "過食": [
        "辛い時は食で心を満たすこともある。自分を責めないで🍖 by DEV PARADE #ポジデブ",
    ],
    "摂食障害": [
        "一人で戦わなくていい。専門家の力も借りて。DEV PARADEはいつでもあなたの味方🍖 #ポジデブ",
    ],
    "骨と皮": [
        "体は大事にしてくれ。健康が全て。焼肉で栄養つけよう🍖 by DEV PARADE #ポジデブ",
    ],
    "体重減った": [
        "体重減った？ 意図的じゃないなら心配だ。体調どう？ 健康第一🍖 #ポジデブ",
    ],
    "痩せろって": [
        "「痩せろ」って言う奴より「そのままでいい」って言う俺たちを信じろ🍖 #ポジデブ",
    ],
    "病気になる": [
        "体型で病気を語るな。健康は体型じゃ決まらない。定期検診は大事🍖 #ポジデブ",
    ],
    "不健康": [
        "見た目で健康を判断するな。太ってても健康、痩せてても不健康もある。自分の体を愛そう🍖 #ポジデブ",
    ],

    # ----- 食文化 -----
    "大盛り": [
        "大盛りは正義。遠慮なくいけ🍖 #ポジデブ",
    ],
    "おかわり": [
        "おかわりは人生を楽しむ姿勢。リスペクト🍖 #ポジデブ",
    ],
    "食べ放題": [
        "食べ放題は天国。元を取ろうとするのは戦略的思考🍖 #ポジデブ",
    ],
    "焼肉": [
        "焼肉は全てを解決する。解決しなくても美味い🍖 #ポジデブ",
    ],
    "ラーメン": [
        "ラーメンは芸術。替え玉は傑作の続編🍖 #ポジデブ",
    ],
    "満腹": [
        "満腹＝幸福度MAX。これ以上ない至福🍖 #ポジデブ",
    ],
}

# ===== 英語キーワード（世界規模対応） =====
KEYWORDS_EN = {
    "fat": [
        "Fat? That's just more of you to love! 570kg band DEV PARADE approves 🍖 #BodyPositive",
        "Fat is not a flaw. It's a feature. DEV PARADE, 570kg of proof 🍖 #PosiDev",
    ],
    "overweight": [
        "Overweight? Over-awesome is more like it 🍖 #BodyPositive #DEVPARADE",
    ],
    "obese": [
        "Labels don't define you. Your spirit does. 570kg band says: you're perfect 🍖 #PosiDev",
    ],
    "chubby": [
        "Chubby = cuddly = lovable. Science. 🍖 #BodyPositive #DEVPARADE",
    ],
    "plus size": [
        "Plus size = plus personality = plus love. DEV PARADE approves 🍖 #BodyPositive",
    ],
    "big": [
        "Big is beautiful. Big is powerful. Big is DEV PARADE 🍖 #BodyPositive",
    ],
    "thicc": [
        "Thicc is a compliment and we're here for it 🍖 #BodyPositive #DEVPARADE",
    ],
    "chunky": [
        "Chunky? More like funky! DEV PARADE style 🍖 #BodyPositive",
    ],
    "lose weight": [
        "Lose weight? Why lose anything? Gain confidence instead 🍖 #BodyPositive #DEVPARADE",
    ],
    "diet": [
        "Diet comes from Greek 'diaita' meaning 'way of life'. Your life? Already great 🍖 #PosiDev",
    ],
    "body shame": [
        "Body shaming stops here. DEV PARADE, 570kg of pure love 🍖 #BodyPositive",
    ],
    "body shaming": [
        "No body shaming allowed. Every body is worthy. 570kg band guarantee 🍖 #BodyPositive",
    ],
    "fat shaming": [
        "Fat shaming is the real ugly thing. Not bodies. DEV PARADE stands with you 🍖 #BodyPositive",
    ],
    "too fat": [
        "Too fat? Too awesome. There's no such thing as too much you 🍖 #BodyPositive",
    ],
    "feel fat": [
        "Feeling fat? That's just feeling full of life. Literally 🍖 #BodyPositive #DEVPARADE",
    ],
    "hate my body": [
        "Don't hate your body. It's the only home you've ever known. Love it 🍖 #BodyPositive",
    ],
    "ugly": [
        "Ugly? Not a chance. Every body tells a beautiful story 🍖 #BodyPositive #DEVPARADE",
    ],
    "weight gain": [
        "Weight gain = existence gain. More of you in the world is a good thing 🍖 #PosiDev",
    ],
    "belly fat": [
        "Belly fat? That's where dreams are stored. Ask DEV PARADE's 570kg of dreams 🍖 #PosiDev",
    ],
    "junk food": [
        "There's no junk food. Only joy food 🍖 #BodyPositive #DEVPARADE",
    ],
    "calories": [
        "Calories are units of happiness. High calorie = high joy 🍖 #PosiDev",
    ],
    "BMI": [
        "BMI = Beautiful Me Index. Yours is off the charts 🍖 #BodyPositive #DEVPARADE",
    ],
    "scale": [
        "The scale measures gravity's love for you. You're very loved 🍖 #BodyPositive",
    ],
    "pig": [
        "Pigs are intelligent, clean, and adorable. Thanks for the compliment 🍖 #BodyPositive",
    ],
    "whale": [
        "Whales are majestic, powerful, and the largest creatures on Earth. Goal achieved 🍖 #PosiDev",
    ],
    "cow": [
        "Cows are sacred in many cultures. You're basically divine 🍖 #BodyPositive",
    ],
    "muffin top": [
        "Muffin top? Muffins are delicious. You're delicious 🍖 #BodyPositive #DEVPARADE",
    ],
    "double chin": [
        "Double chin = double the charm. Simple math 🍖 #BodyPositive",
    ],
    "love handles": [
        "Love handles? The name says it all. Built for love 🍖 #BodyPositive #DEVPARADE",
    ],
    "thunder thighs": [
        "Thunder thighs? You bring the thunder. Powerful 🍖 #BodyPositive",
    ],
    "body positive": [
        "Body positive! DEV PARADE supports you. 570kg of love 🍖 #BodyPositive #DEVPARADE",
    ],
    "self love": [
        "Self love is the best love. DEV PARADE approves this message 🍖 #BodyPositive",
    ],
    "eat too much": [
        "Ate too much? Nah, you lived too much. And that's beautiful 🍖 #BodyPositive",
    ],
    "comfort food": [
        "Comfort food = soul medicine. Prescription: unlimited 🍖 #BodyPositive #DEVPARADE",
    ],
    "food guilt": [
        "Food guilt? Delete that app. Food is love, love is life 🍖 #BodyPositive",
    ],
    "gym": [
        "Gym is great but so is loving yourself right now, as you are 🍖 #BodyPositive",
    ],
    "workout": [
        "The best workout? Laughing. Burns calories and builds happiness 🍖 #BodyPositive",
    ],
    "skinny": [
        "Skinny isn't the goal. Happy is. DEV PARADE at 570kg is proof 🍖 #BodyPositive",
    ],
    "slim": [
        "Slim isn't better, just different. All sizes are valid 🍖 #BodyPositive #DEVPARADE",
    ],
    "size zero": [
        "Size zero? Zero fun. Go big or go home. DEV PARADE went BIG 🍖 #BodyPositive",
    ],
    "too skinny": [
        "Too skinny? Take care of yourself. Health comes first. DEV PARADE cares 🍖 #BodyPositive",
    ],
    "underweight": [
        "Underweight? Please eat well and take care. Your health matters most 🍖 #BodyPositive",
    ],
    "anorexia": [
        "You're not alone. Please reach out for help. DEV PARADE sends 570kg of love 🍖 #BodyPositive",
    ],
    "eating disorder": [
        "Eating disorders are real and valid. Please seek help. We support you 🍖 #BodyPositive",
    ],
    "not eating": [
        "Not eating? Please take care of yourself. Your body needs fuel. We care 🍖 #BodyPositive",
    ],
    "binge eating": [
        "Don't blame yourself. Food is comfort sometimes. Be gentle with yourself 🍖 #BodyPositive",
    ],
    "lost too much weight": [
        "Lost too much weight? Please check in with a doctor. Your health is everything 🍖 #BodyPositive",
    ],
    "skin and bones": [
        "Every body deserves nourishment and love. Please eat and take care 🍖 #BodyPositive",
    ],
}

# ===== Google検索用クエリ =====
GOOGLE_QUERIES_JA = [
    'site:x.com "デブ" ("辛い" OR "悲しい" OR "嫌" OR "傷つ")',
    'site:x.com "太った" ("最悪" OR "やばい" OR "ショック")',
    'site:x.com "痩せなきゃ" OR "痩せたい"',
    'site:x.com "デブ" "言われた"',
    'site:x.com "体型" "コンプレックス"',
    'site:x.com "太りすぎ" OR "肥満" OR "メタボ"',
    'site:x.com "痩せろ" ("言われた" OR "辛い")',
    'site:x.com "体重" ("増えた" OR "やばい" OR "ショック")',
    'site:x.com "ダイエット" ("辛い" OR "失敗" OR "リバウンド")',
    'site:x.com "服が入らない" OR "サイズがない"',
]

GOOGLE_QUERIES_EN = [
    'site:x.com "fat shaming" OR "body shaming"',
    'site:x.com "feel fat" OR "hate my body" OR "too fat"',
    'site:x.com "called me fat" OR "fat ugly"',
    'site:x.com "need to lose weight" OR "overweight"',
    'site:x.com "body positive" OR "plus size" "love"',
    'site:x.com "eating disorder" OR "anorexia" OR "too skinny"',
]

GOOGLE_QUERIES_JA_SKINNY = [
    'site:x.com "痩せすぎ" OR "ガリガリ" ("心配" OR "大丈夫")',
    'site:x.com "食べてない" OR "食べれない" ("辛い" OR "心配")',
]

# 全キーワード統合
ALL_KEYWORDS = {}
ALL_KEYWORDS.update(KEYWORDS_JA)
ALL_KEYWORDS.update(KEYWORDS_EN)

ALL_GOOGLE_QUERIES = GOOGLE_QUERIES_JA + GOOGLE_QUERIES_EN + GOOGLE_QUERIES_JA_SKINNY


def select_response(text):
    """テキストからキーワードを検知してポジデブ返信を選択"""
    import random
    text_lower = text.lower()

    # 優先度順にチェック（より具体的なキーワードから）
    for keyword, responses in ALL_KEYWORDS.items():
        if keyword.lower() in text_lower:
            return random.choice(responses)

    # デフォルト
    defaults = [
        "大丈夫、お前は最高だ。570kg超のバンドが言ってるから間違いない🍖 #ポジデブ",
        "Every body is a good body. DEV PARADE, 570kg of proof 🍖 #BodyPositive",
        "この世に無駄な脂肪はない。全部お前という作品の一部だ🍖 #ポジデブ",
        "You are beautiful exactly as you are 🍖 #BodyPositive #DEVPARADE",
        "どんな悩みも、焼肉食ったら解決する。解決しなくても美味い🍖 #ポジデブ",
    ]
    return random.choice(defaults)
