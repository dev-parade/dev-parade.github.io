#!/bin/bash
# デブポジツイート即投稿スクリプト
# 使い方: bash scripts/tweet-now.sh
# ランダムなデブポジツイートを生成してブラウザで投稿画面を開く

TWEETS=(
"🍖【世界初】ポジデブBot、爆誕。SNS上の全ての「デブ」をポジティブに変換！全員90kg超のバンド Devparadeが全力で肯定します。試してみて👇 https://devparade.jp/debu-bot.html #ポジデブBot #Devparade"
"デブは才能。脂肪は努力の結晶。俺たちDevparade、メンバー全員90kg以上でメジャーデビューした。体重と才能は比例する。🍖 #ポジデブBot #Devparade https://devparade.jp/debu-bot.html"
"「太った」→「成長した」「デブ」→「存在感がある」「メタボ」→「ロックな体型」全部ポジティブに変換するBot作った🍖 https://devparade.jp/debu-bot.html #ポジデブBot #Devparade"
"体重と幸福度は比例する。（Devparade調べ）source: 俺たちメンバー全員90kg超で幸せ🍖 #ポジデブBot #Devparade https://devparade.jp/debu-bot.html"
"NARUTOのエンディング歌ってたメンバー全員90kg以上のバンドが15年ぶりに復活して「デブをポジティブにするBot」を作った。全部事実です🍖 https://devparade.jp/ #Devparade #バッチコイ"
)

INDEX=$((RANDOM % ${#TWEETS[@]}))
TWEET="${TWEETS[$INDEX]}"

echo "🍖 デブポジツイート:"
echo ""
echo "$TWEET"
echo ""
echo "ブラウザで投稿画面を開きます..."

ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$TWEET'''))")
open "https://twitter.com/intent/tweet?text=$ENCODED"
