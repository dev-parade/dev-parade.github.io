import json
import os
from bs4 import BeautifulSoup

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, '..', 'lyrics', 'index.html')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'lyrics_database.json')

def extract_lyrics():
    if not os.path.exists(HTML_PATH):
        print(f"Error: Could not find HTML file at {HTML_PATH}")
        return

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    song_cards = soup.find_all('div', class_='song-card')

    database = []

    for card in song_cards:
        # Extract title
        title_elem = card.find('div', class_='song-title')
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)

        # Extract meta (album/track info)
        meta_elem = card.find('div', class_='song-meta')
        meta = meta_elem.get_text(strip=True) if meta_elem else ""

        # Extract track number
        num_elem = card.find('div', class_='song-num')
        track_num = num_elem.get_text(strip=True) if num_elem else ""

        # Extract audio URL (SoundCloud / Demo link)
        demo_btn = card.find('a', class_='stream-btn demo')
        audio_url = demo_btn.get('href') if demo_btn else ""

        # Extract lyrics
        lyrics_elem = card.find('div', class_='lyrics-text')
        if lyrics_elem:
            # We want to preserve newlines but clean up extra spaces
            lyrics = lyrics_elem.get_text(separator='\n').strip()
        else:
            lyrics = ""

        # Only add songs that actually have lyrics
        if lyrics:
            database.append({
                "id": f"{track_num}_{title.replace(' ', '_')}" if track_num else title.replace(' ', '_'),
                "title": title,
                "meta": meta,
                "track_num": track_num,
                "audio_url": audio_url,
                "lyrics": lyrics
            })

    # Save to JSON
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully extracted {len(database)} songs and saved to {OUTPUT_PATH}")

if __name__ == '__main__':
    extract_lyrics()
