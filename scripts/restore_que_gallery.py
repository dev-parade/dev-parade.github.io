import os

def restore_que_gallery():
    html_path = 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate Club Que Grid
    que_images = []
    que_dir = 'assets/que_new'
    if os.path.exists(que_dir):
        que_files = sorted(os.listdir(que_dir))
        for f in que_files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                que_images.append(f'assets/que_new/{f}')

    limit = 12
    html_list = []
    for i, img in enumerate(que_images):
        hidden_class = ' hidden-img' if i >= limit else ''
        style = ' style="display:none;"' if i >= limit else ''
        html_list.append(f'      <img src="{img}" alt="Live Photo" class="gallery-thumb{hidden_class}" loading="lazy" onclick="openLightbox(this.src)"{style}>')
    
    que_grid_html = '\n'.join(html_list)

    que_section = f"""
  <!-- ===== PHOTO GALLERY (QUE) ===== -->
  <section id="gallery-que" style="border-top: 1px solid #222; padding-top: 0;">
    <p class="section-sub reveal">2026.02.06 復活ワンマン @ 下北沢 Club Que</p>
    <div id="gallery-grid-que" class="gallery-grid reveal">
{que_grid_html}
    </div>
    <button class="view-more-btn" onclick="toggleGallery(this, 'gallery-grid-que')">VIEW MORE</button>
  </section>
"""

    # Insert after the Yoyogi gallery section
    if '</section>' in content:
        # Find the end of id="gallery"
        marker = '<!-- ===== GOODS ===== -->'
        if marker in content:
            content = content.replace(marker, que_section + '\n  ' + marker)
        else:
            # Fallback: after id="gallery"
            content = content.replace('</section>\n\n  <!-- ===== PHOTO GALLERY (QUE) ===== -->', '') # Clean up if partially exists
            content = content.replace('id="gallery">', 'id="gallery-yoyogi">') # Rename for clarity
            content = content.replace('<!-- ===== PHOTO GALLERY (YOYOGI) ===== -->', '<!-- ===== PHOTO GALLERIES ===== -->')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Restored Club Que gallery with {len(que_images)} photos.")

if __name__ == "__main__":
    restore_que_gallery()
