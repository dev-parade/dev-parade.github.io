import os
import re
import time
import random

def random_gallery_fix():
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
    random.seed(time.time()) # Use current time as seed for true randomness on each run
    random.shuffle(yoyogi_imgs)
    random.shuffle(que_imgs)

    def build_grid(images, grid_id, limit=12):
        html = [f'    <div id="{grid_id}" class="gallery-grid reveal">']
        for i, img in enumerate(images):
            hidden = ' hidden-img' if i >= limit else ''
            style = ' style="display:none;"' if i >= limit else ''
            html.append(f'      <img src="{img}" alt="Live Photo" class="gallery-thumb{hidden}" loading="lazy" onclick="openLightbox(this.src)"{style}>')
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
    
    print(f"Gallery shuffled and version updated to {new_ver}")

if __name__ == "__main__":
    random_gallery_fix()
