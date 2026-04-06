# Devparade サイト - Claude Code プロジェクト設定

## プロジェクト概要
Devparade（デブパレード）のオフィシャルサイト＋自動投稿システム。
- **バンド**: 2006年結成、2008年ソニーよりメジャーデビュー。メンバー全員90kg以上のヘヴィメタボバンド
- **代表曲**: NARUTOエンディング「バッチコイ!!!」
- **コンセプト**: ポジデブ（デブをポジティブに）

## ディレクトリ構成
```
dev-parade-site/
├── index.html              # メインサイト
├── debu-bot.html           # ポジデブBot紹介ページ
├── assets/                 # 画像・ロゴ
├── scripts/                # X（Twitter）自動投稿スクリプト群
│   ├── debu-posi-bot.py        # メンション監視＆リプライBot
│   ├── debu-posi-marketing.py  # マーケティングツイート生成
│   ├── debu-posi-monitor.py    # X監視スクリプト
│   ├── debu-posi-tweet-generator.py  # ツイート生成（1日4回）
│   ├── debu-posi-search-free.py      # 無料検索
│   ├── follower-growth.py      # フォロワー成長エンジン
│   └── posideb_keywords.py     # キーワード一覧（JA/EN）
├── blog-x/                 # COYASS 自動投稿システム（Note & X）
│   ├── src/                # メインコード
│   ├── config/             # 設定ファイル・テンプレート
│   └── README.md
└── .github/workflows/      # GitHub Actions（1日4回自動投稿）
```

## メンバー
- COYASS（Vo.）- 歯科医師 × ラッパー
- ハンサム判治（Gt.）
- ugazin（Gt.）
- ぺー（Ba.）
- TAH（Dr.）

## よく使うコマンド
```bash
# GitHub Actions 手動実行
gh workflow run debu-posi-marketing.yml

# ローカルでツイート生成テスト
python scripts/debu-posi-tweet-generator.py

# blog-x のダッシュボード起動
cd blog-x && python src/main.py dashboard
```

## 開発ルール
- APIキーは絶対にファイルにハードコードしない（`.env` を使う）
- コミット前に `tweet_issue.md` と `bot_log.md` は除外
- 日本語でコミットメッセージOK
- ブランチは基本 `main` で作業
