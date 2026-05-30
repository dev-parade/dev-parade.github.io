import os
import re
import time
import random

def random_gallery_fix_v2():
    html_path = 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get Images
    def get_images(dir_path, prefix='', filter_func=None):
        files = sorted(os.listdir(dir_path))
        imgs = []
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                if filter_func and not filter_func(f):
                    continue
                imgs.append(f'{prefix}{f}')
        return imgs

    yoyogi_imgs = get_images('assets', prefix='assets/', filter_func=lambda x: x.startswith('yoyogi_') or (x.startswith('IMG_') and '4701' <= x[4:8] <= '4909'))
    que_imgs = get_images('assets/que_new', prefix='assets/que_new/')

    # SHUFFLE THEM!
    random.seed(time.time())
    random.shuffle(yoyogi_imgs)
    random.shuffle(que_imgs)

    # 復活ワンマンのフライヤーをClub Queギャラリーの先頭に固定
    que_flyer = 'assets/flyer-20260206.jpg'
    if os.path.exists(que_flyer):
        # もしリストに入っていても一旦削除して先頭に追加
        if que_flyer in que_imgs: que_imgs.remove(que_flyer)
        que_imgs.insert(0, que_flyer)

    def build_grid(images, grid_id, limit=12):
        html = [f'    <div id="{grid_id}" class="gallery-grid reveal">']
        for i, img in enumerate(images):
            hidden = ' hidden-img' if i >= limit else ''
            style = ' style="display:none;"' if i >= limit else ''
            # フライヤーの場合はaltを特別にする
            alt = "復活ワンマン フライヤー" if "flyer-20260206" in img else "Live Photo"
            html.append(f'      <img src="{img}" alt="{alt}" class="gallery-thumb{hidden}" loading="lazy" onclick="openLightbox(this.src)"{style}>')
        html.append('    </div>')
        html.append(f'    <button class="view-more-btn" onclick="toggleGallery(this, \'{grid_id}\')">VIEW MORE</button>')
        return '\n'.join(html)

    yoyogi_section = f"""
  <!-- ===== PHOTO GALLERIES ===== -->
  <section id="gallery">
    <h2 class="section-title reveal">LIVE <span>GALLERY</span></h2>
    <p class="section-sub reveal">2026.05.09 14degrees Japan @ 代々木第二体育館</p>
{build_grid(yoyogi_imgs, 'gallery-grid-yoyogi')}
    
    <p class="section-sub reveal" style="margin-top:4rem;">2026.02.06 復活ワンマン @ 下北沢 Club Que</p>
{build_grid(que_imgs, 'gallery-grid-que')}
  </section>
"""

    # Remove any existing gallery sections
    content = re.sub(r'<!-- ===== PHOTO GALLERIES ===== -->.*?<!-- ===== GOODS ===== -->', '<!-- ===== GOODS ===== -->', content, flags=re.DOTALL)

    # Insert new unified gallery section
    content = content.replace('<!-- ===== GOODS ===== -->', yoyogi_section + '\n\n  <!-- ===== GOODS ===== -->')

    # Update Version for cache busting
    new_ver = f"Ver: {int(time.time()) % 10000}"
    content = re.sub(r'Ver: \d+', new_ver, content)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Gallery updated with Reunion Flyer at top. Version: {new_ver}")

if __name__ == "__main__":
    random_gallery_fix_v2()
