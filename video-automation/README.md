# Devparade Video Automation

MVやTikTok・YouTube Shorts用のリリックビデオを自動生成するシステムです。
公式サイトの歌詞データ（`lyrics/index.html`）を解析し、AI（OpenAI Whisper）を用いて音源と歌詞のタイミングを自動同期させ、動画を書き出します。

## 📁 フォルダ構成
- `data/`: 抽出した歌詞のデータベースファイル（JSON）が保存されます。
- `assets/`: 処理する音源（.mp3）と背景画像（.jpg）を配置してください。（※GitHubにはアップロードされません）
- `output/`: 完成した動画ファイル（.mp4）が出力されます。

## ⚙️ セットアップ方法

1. **Python環境の準備**
   Python 3.8以上がインストールされていることを確認し、必要なライブラリをインストールします。
   （※初回のみ、または仮想環境を作成して実行してください）
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   > ⚠️ 注意: Whisperの動作には `ffmpeg` がPCにインストールされている必要があります。Macの場合は `brew install ffmpeg` を実行してください。

2. **歌詞データベースの更新**
   公式サイトの歌詞が追加・修正された場合は、以下のスクリプトを実行してデータベースを最新化します。
   ```bash
   python extract_lyrics.py
   ```
   実行後、`data/lyrics_database.json` に全曲の歌詞データが格納されます。

## 🎬 動画の自動生成手順

1. **素材の準備**
   `assets/` フォルダ内に、使用したい音源ファイル（例：`parfait.mp3`）と、背景にしたい画像ファイル（例：`parfait_bg.jpg`）を配置します。

2. **動画生成コマンドの実行**
   以下のコマンドで動画生成を開始します。
   ```bash
   python generate_video.py --song-id "03_パルフェ" --audio assets/parfait.mp3 --image assets/parfait_bg.jpg --output parfait_tiktok.mp4
   ```
   
   - `--song-id`: `lyrics_database.json` に記載されている `id` を指定します。
   - `--audio`: 音源ファイルへのパス。
   - `--image`: 背景画像へのパス（自動でTikTokサイズの縦長9:16に切り抜かれます）。
   - `--output`: 出力する動画のファイル名。

3. **完成！**
   AIが音声を解析し、処理が完了すると `output/` フォルダに動画が生成されます。（※AIの解析と動画エンコードには数分かかる場合があります）
