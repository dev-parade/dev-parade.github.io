"""
COYASS Auto-Posting System - X (Twitter) Publisher
tweepy を使った X API v2 での自動投稿
"""

import os
import logging
from datetime import datetime
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class XPublisher:
    """X (Twitter) API v2 による自動投稿"""

    def __init__(self, config: dict):
        self.config = config.get("x", {})
        self.max_chars = self.config.get("max_chars", 280)
        self.enable_threads = self.config.get("enable_threads", True)
        self.thread_max = self.config.get("thread_max_tweets", 5)
        self.retry_attempts = self.config.get("retry_attempts", 3)
        self.client = None
        self.username = "x"  # デフォルトのユーザー名

    def initialize(self):
        """tweepy クライアントの初期化"""
        try:
            import tweepy

            # 環境変数の読み込み（複数の候補に対応）
            api_key = os.getenv("X_API_KEY") or os.getenv("API_KEY")
            api_secret = os.getenv("X_API_SECRET") or os.getenv("API_SECRET")
            access_token = os.getenv("X_ACCESS_TOKEN") or os.getenv("ACCESS_TOKEN")
            access_secret = os.getenv("X_ACCESS_TOKEN_SECRET") or os.getenv("X_ACCESS_SECRET") or os.getenv("ACCESS_SECRET")
            bearer_token = os.getenv("X_BEARER_TOKEN")

            # API v2 Client (投稿用)
            self.client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_secret
            )

            # API v1.1 (画像アップロード用)
            auth = tweepy.OAuth1UserHandler(
                api_key,
                api_secret,
                access_token,
                access_secret
            )
            self.api_v1 = tweepy.API(auth)

            # 認証テスト
            me = self.client.get_me()
            if me.data:
                self.username = me.data.username
                logger.info(f"✅ X API authenticated as @{self.username}")
            return True

        except Exception as e:
            logger.error(f"❌ X API init failed: {e}")
            return False

    def post_tweet(self, text: str, image_path: str = None,
                    reply_to_id: str = None) -> Optional[dict]:
        """ツイートを投稿する"""
        for attempt in range(self.retry_attempts):
            try:
                media_ids = None

                # 画像があればアップロード
                if image_path and Path(image_path).exists():
                    media = self.api_v1.media_upload(image_path)
                    media_ids = [media.media_id]
                    logger.info(f"📸 Image uploaded: {image_path}")

                # テキストのサニタイズ（最終チェック）
                text = text.replace("★", "-")

                # テキストの文字数チェック
                if len(text) > self.max_chars:
                    logger.warning(f"⚠️ Tweet truncated: {len(text)} -> {self.max_chars} chars")
                    text = text[:self.max_chars - 3] + "..."

                # 投稿
                kwargs = {"text": text}
                if media_ids:
                    kwargs["media_ids"] = media_ids
                if reply_to_id:
                    kwargs["in_reply_to_tweet_id"] = reply_to_id

                response = self.client.create_tweet(user_auth=True, **kwargs)

                if response.data:
                    tweet_id = response.data["id"]
                    logger.info(f"✅ Tweet posted: {tweet_id}")
                    return {
                        "tweet_id": tweet_id,
                        "url": f"https://x.com/{self.username}/status/{tweet_id}",
                        "published_at": datetime.utcnow().isoformat()
                    }

            except Exception as e:
                logger.error(f"❌ Tweet attempt {attempt + 1} failed: {e}")
                if "429" in str(e):
                    # レート制限 → 長めに待機
                    import time
                    wait_time = 60 * (attempt + 1)
                    logger.info(f"⏳ Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                elif attempt >= self.retry_attempts - 1:
                    return None

        return None

    def post_thread(self, texts: List[str], image_paths: List[str] = None) -> List[dict]:
        """スレッド投稿（複数ツイートを連結）"""
        results = []
        previous_id = None

        for i, text in enumerate(texts[:self.thread_max]):
            image = image_paths[i] if image_paths and i < len(image_paths) else None
            result = self.post_tweet(text, image_path=image, reply_to_id=previous_id)

            if result:
                results.append(result)
                previous_id = result["tweet_id"]
                logger.info(f"📝 Thread {i + 1}/{len(texts)} posted")
            else:
                logger.error(f"❌ Thread broken at tweet {i + 1}")
                break

        return results

    def split_for_thread(self, long_text: str) -> List[str]:
        """長いテキストをスレッド用に分割"""
        if len(long_text) <= self.max_chars:
            return [long_text]

        chunks = []
        sentences = long_text.replace("。", "。\n").split("\n")
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # スレッドナンバーの余白を考慮
            max_len = self.max_chars - 10  # "1/5 " 等の余白

            if len(current_chunk) + len(sentence) + 1 <= max_len:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # スレッドナンバーを追加
        total = len(chunks)
        if total > 1:
            chunks = [f"{i + 1}/{total} {chunk}" for i, chunk in enumerate(chunks)]

        return chunks[:self.thread_max]

    def get_rate_limit_status(self) -> dict:
        """レート制限の残り状況を取得"""
        try:
            # v1.1 API でレート制限を確認
            limits = self.api_v1.rate_limit_status()
            tweets_limit = limits.get("resources", {}).get("tweets", {})
            return {
                "status": "ok",
                "limits": tweets_limit
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
