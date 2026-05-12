import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("X_API_KEY")
API_SECRET = os.getenv("X_API_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET)

media_ids = []
for i in range(1, 5):
    img_path = f"assets/yoyogi_{i}.jpg"
    if os.path.exists(img_path):
        print(f"Uploading {img_path}...")
        media = api.media_upload(img_path)
        media_ids.append(media.media_id)
        
tweet_text = """2026.05.09
14degrees Japan @ 代々木第二体育館
最高のステージだったぜ🍖 バッチコイ！！！
集まってくれたみんな、ありがとう！

📸 Photos by YUZU PHOTO (@yuzunet_photo)
ギャラリーも公式サイトに追加したから見てくれよな！
👉 https://devparade.jp/#gallery

#Devparade #デブパレード #ポジデブ #14degreesJapan"""

if media_ids:
    print("Posting tweet with photos...")
    response = client.create_tweet(text=tweet_text, media_ids=media_ids)
    print("✅ Successfully posted to X!")
    print(f"Tweet URL: https://x.com/user/status/{response.data['id']}")
else:
    print("❌ Photos not found in assets/ directory.")
