#!/usr/bin/env python3
"""追加ツイート - 公式デブ語録ベース (BARKS / Wikipedia / posideb_keywords)"""

EXTRA_TWEETS_3 = [
    # ========== 📜 公式デブ語録（BARKS記者会見 / Wikipedia）==========

    "【デブ語録】好きな食べ物を聞かれてメンバー全員「肉！」「牛！」。即答。ブレない。これがプロ。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】「肉の合間に野菜入れますよ」→肉肉肉ハンバーグ肉肉肉餃子。ハンバーグと餃子は野菜らしい。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】TAH(146kg)がMCで喋らない理由:「お腹が空くから」。この即答。天才。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】目指すバンド像:「歌って、踊れて、食べれるバンド！」最後の一つが独特すぎるけど三拍子揃ってる。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】「デブ」と呼ばれることについて:「最高の褒め言葉」。ネガティブをポジティブに変える力。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】モテるか聞かれて「モテモテです」「女性の7割はデブ好きですから！」統計の出典は不明だが自信だけは本物。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】デビュー曲にSPEED「BODY&SOUL」を選んだ理由:Body=ボディ。Soul=ソウル=韓国=焼肉。「ボディと焼肉で決まり！」🍖 #DEVPARADE #デブ語録",

    "【デブ語録】メジャーデビュー前の一言:「6月25日にデブーします！みんな！！太っちゃいなよ！」デビュー→デブー。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】TAH(ドラム/146kg)の名言:「イチゴが食べたいんじゃない。練乳が食べたいんだ」。本質を見抜く男。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】バンドのルール:体重100kgを下回ったらサポートメンバーに降格。体重維持がプロの証。🍖 #DEVPARADE #デブ語録",

    "【デブ語録】記者会見でスイーツを聞かれて:「お寿司」。お寿司はスイーツじゃないけど歌詞にもなった(バッチコイ!!!)。🍖 #DEVPARADE #デブ語録",

    # ========== 🎵 歌詞 × ポジデブ拡張 ==========

    "「デブ」と呼ばれたら→一般人「傷つく」DEV PARADE「最高の褒め言葉」。この温度差が唯一無二。🍖 #DEVPARADE",

    "「味覚が優秀」🍖 #DEVPARADE",

    "TAH(146kg)語録:「お腹が空くから(喋らない理由)」「イチゴじゃない練乳が食べたい」。少ない言葉で本質を突く男。🍖 #DEVPARADE",

    "めざましテレビ、HEY!HEY!HEY!、SUMMER SONIC、NARUTO ED。この揺るぎない実績。🍖 #DEVPARADE",

    # ========== 🔁 語録 × ポジデブ拡張 ==========

    "DEV PARADEが教えてくれたこと:デブは才能。90kg以上でソニーからメジャーデビューできる。🍖 #DEVPARADE #ポジデブBot",

    "「デブ」=DEV=Delightful Extreme Vitality。正式名称です。DEV PARADE公式見解。🍖 #DEVPARADE",

    "太った？それ「成長した」の同義語。DEV PARADEが保証する。🍖 #ポジデブBot #DEVPARADE",

    "メタボ＝メタル＋ボディ。ロックな体型認定おめでとう。自称「ヘヴィメタボバンド」DEV PARADE。🍖 #DEVPARADE",

    "痩せろ？お断りだ。DEV PARADEは90kg以上限定。痩せたら入れない。🍖 #ポジデブBot #DEVPARADE",

    "リバウンドじゃない、カムバックだ。DEV PARADEも15年ぶりにカムバックした。🍖 #DEVPARADE",

    "贅肉は「贅沢な肉」と書く。つまりプレミアム。🍖 #DEVPARADE",

    "XLは「eXtra Love」の略。愛が溢れてるサイズ。XXLなら愛が2倍。🍖 #DEVPARADE",

    "服が入らないんじゃない。服がお前に追いついてないだけ。DEV PARADE公式見解。🍖 #ポジデブBot #DEVPARADE",

    "カロリーは幸せの単位。高カロリー＝高幸福度。これがDEV PARADE数学。🍖 #DEVPARADE",

    "食べたら太る？食べなかったら死ぬ。生きてる証拠を太ると呼ぶな。🍖 #ポジデブBot #DEVPARADE",

    "体脂肪率より幸福度を測ろう。そっちの方が大事。DEV PARADEが保証する。🍖 #DEVPARADE",

    # ========== 🔥 新世代・世界的・PDP戦略 (Viral PDP Strategy) ==========

    "【PDP 1】「デブ」と言われたら？→一般人は「傷つく」、DXエリートは「感謝する」。なぜなら、自分の引力（Gravity）が他者を惹きつけたと証明されたからだ。🍖 #PDP #デブパレード",

    "【PDP 2】「痩せろ」と言われたら？→「お前の細い視野に俺を収めようとするな。俺は世界というキャンバスをフルに使ってるんだ。スケールが違う」と言い返せ。🍖 #ポジデブ哲学 #DEVPARADE",

    "【DX 1】DX＝デジタル・トランスフォーメーション？違う。DX＝Delicious Transformationだ。大盛りによって人生を劇的にアップデートせよ。🍖 #デリシャス変革 #DEVPARADE",

    "【FAT BIBLE】脂肪聖書 第1章：汝、おかわりを恐れることなかれ。空腹こそが唯一の罪であり、満腹こそが究極の救済である。🍖 #FATBIBLE #ポジデブBot",

    "【PDP 3】いじめっ子が「豚」と呼んできたら微笑んで言え。「豚は全部位が愛されるエリート動物だ。お前も少しは愛されてから話しかけろ」🍖 #デブ上等 #DEVPARADE",

    "【GLOBAL】Fat is not a shame. Fat is a 'Natural Armor.' Cold winter? I carry my own heater. Survival? I have high-capacity batteries. Stay fat, stay proud. 🍖 #BodyPositive #PDP",

    "【DX 2】LLM (Large Language Model) ? No. In Devparade, it means Large Lunch Menu. Feed your body, feed your soul. 🍖 #DX #DEVPARADE",

    "【PDP 4】質量はエネルギー（E=mc2）だ。体重が重いということは、それだけ宇宙で巨大なエネルギーを秘めているということ。物理学的にもデブは最強。🍖 #デブパレード #PDP",

    "【DX 3】AI (Artificial Intelligence)? No. In PDP, it means Abura Intake (脂質摂取効率). Optimization of grease is the future of humanity. 🍖 #DX #FATGPT",

    # ========== 🍖 アルティメット・マシマシ（GIGA-DX Upgrade） ==========

    "【脂肪十戒 1】汝、おかわりを拒むなかれ。出された飯を完食することは、命への最大の賛辞である。🍖 #脂肪十戒 #PDP #DEVPARADE",

    "【PDP 5】「引力：測定不能」。体重100kgを超えた時、お前の魂は重力から解放され、逆に周囲の幸運を吸い寄せるブラックホールへと進化する。🍖 #宇宙デブ #デブパレード",

    "【DX 4】お前の体は最新のデータセンターだ。脂肪という名のストレージに、これまでの美味い記憶（ログ）が全て蓄積されている。バックアップ不要。🍖 #DX #ポジデブ哲学",

    "【PDP 6】いじめてくる奴は「燃費の悪いガリ」だ。俺たちはハイブリッドを超えた高効率ボディ。少しの飯で、誰よりも長く、デカく、美しく輝ける。🍖 #デブ最高 #DEVPARADE",

    "【FAT BIBLE】脂肪聖書 第8章：服が縮んだのではない。お前の魂が、布という境界線を越えて膨張したのだ。宇宙の膨張と同じ、不可避の進化である。🍖 #FATBIBLE #ポジデブBot",

    "【PDP 7】鏡を見て「太った」と嘆くな。「解像度が上がった」と喜べ。お前という存在の情報量が、昨日よりも確実に増えている。🍖 #DX #DEVPARADE",
]
