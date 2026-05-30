import os
import re

def generate_gallery_html():
    html_path = 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Yoyogi Gallery (assets/IMG_4701.JPG to IMG_4909.JPG and yoyogi_*.jpg)
    yoyogi_images = []
    # yoyogi_1 to 4
    for i in range(1, 5):
        yoyogi_images.append(f'assets/yoyogi_{i}.jpg')
    # IMG_4701 to 4909
    assets_files = sorted(os.listdir('assets'))
    for f in assets_files:
        if f.startswith('IMG_') and f.endswith('.JPG') and '4701' <= f[4:8] <= '4909':
            yoyogi_images.append(f'assets/{f}')

    yoyogi_html = '\n'.join([
        f'      <img src="{img}" alt="Live Photo" class="gallery-thumb" loading="lazy" onclick="openLightbox(this.src)">'
        for img in yoyogi_images
    ])

    # 2. Club Que Gallery (assets/que_new/*)
    que_dir = 'assets/que_new'
    que_images = []
    if os.path.exists(que_dir):
        que_files = sorted(os.listdir(que_dir))
        for f in que_files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                que_images.append(f'assets/que_new/{f}')

    que_html = '\n'.join([
        f'      <img src="{img}" alt="Live Photo" class="gallery-thumb" loading="lazy" onclick="openLightbox(this.src)">'
        for img in que_images
    ])

    # Replace the gallery sections in HTML
    # We need to find the start and end markers. 
    # I'll use a more robust way by looking for the section IDs.

    # For Yoyogi (id="gallery")
    yoyogi_section_pattern = r'(<section id="gallery">.*?<div[^>]*?>).*?(</div>\s*</section>)'
    new_yoyogi_content = r'\1\n' + yoyogi_html + r'\n\2'
    content = re.sub(yoyogi_section_pattern, f'\\1\n{yoyogi_html}\n\\2', content, flags=re.DOTALL)

    # For Club Que (We might need to add a specific section if it doesn't exist or replace existing)
    # Looking for "2026.02.06 復活ワンマン"
    que_pattern = r'(<p class="section-sub reveal">2026.02.06 復活ワンマン @ 下北沢 Club Que</p>\s*<div[^>]*?>).*?(</div>)'
    content = re.sub(que_pattern, f'\\1\n{que_html}\n\\2', content, flags=re.DOTALL)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {len(yoyogi_images)} Yoyogi photos and {len(que_images)} Club Que photos.")

if __name__ == "__main__":
    generate_gallery_html()
