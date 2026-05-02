import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

def check():
    api_key = os.getenv("X_API_KEY") or os.getenv("API_KEY")
    api_secret = os.getenv("X_API_SECRET") or os.getenv("API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN") or os.getenv("ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_TOKEN_SECRET") or os.getenv("X_ACCESS_SECRET") or os.getenv("ACCESS_SECRET")

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        me = client.get_me()
        if me.data:
            print(f"SUCCESS: Authenticated as @{me.data.username} (ID: {me.data.id})")
        else:
            print("FAILED: Could not get user data")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check()
