import os
import re

def generate_gallery_html():
    html_path = 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define Image Sources
    # 1. Yoyogi
    yoyogi_images = []
    for i in range(1, 5): yoyogi_images.append(f'assets/yoyogi_{i}.jpg')
    assets_files = sorted(os.listdir('assets'))
    for f in assets_files:
        if f.startswith('IMG_') and f.endswith('.JPG') and '4701' <= f[4:8] <= '4909':
            yoyogi_images.append(f'assets/{f}')

    # 2. Club Que
    que_images = []
    que_dir = 'assets/que_new'
    if os.path.exists(que_dir):
        que_files = sorted(os.listdir(que_dir))
        for f in que_files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                que_images.append(f'assets/que_new/{f}')

    def build_grid_html(images, limit=12):
        html = []
        for i, img in enumerate(images):
            hidden_class = ' hidden-img' if i >= limit else ''
            style = ' style="display:none;"' if i >= limit else ''
            html.append(f'      <img src="{img}" alt="Live Photo" class="gallery-thumb{hidden_class}" loading="lazy" onclick="openLightbox(this.src)"{style}>')
        return '\n'.join(html)

    yoyogi_grid = build_grid_html(yoyogi_images)
    que_grid = build_grid_html(que_images)

    # Inject CSS for Gallery
    gallery_css = """
    .gallery-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 0.5rem;
      margin-top: 1rem;
    }
    .gallery-thumb {
      width: 100%;
      aspect-ratio: 1/1;
      object-fit: cover;
      cursor: pointer;
      transition: transform 0.3s ease, filter 0.3s ease, box-shadow 0.3s ease;
      filter: grayscale(30%);
      border-radius: 4px;
    }
    .gallery-thumb:hover {
      transform: scale(1.05);
      filter: grayscale(0%);
      z-index: 10;
      box-shadow: 0 10px 20px rgba(227, 30, 36, 0.4);
    }
    #lightbox {
      display: none;
      position: fixed;
      z-index: 3000;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.95);
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    #lightbox img {
      max-width: 95%;
      max-height: 95%;
      object-fit: contain;
      animation: zoomIn 0.3s ease;
    }
    @keyframes zoomIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    .view-more-btn {
      display: block;
      margin: 2rem auto;
      padding: 0.8rem 2.5rem;
      background: var(--red);
      color: white;
      border: none;
      cursor: pointer;
      font-family: 'Oswald', sans-serif;
      font-weight: 700;
      letter-spacing: 0.2em;
      transition: 0.3s;
    }
    .view-more-btn:hover { background: var(--white); color: var(--red); }
    """

    # Add CSS to style tag
    if '</style>' in content:
        content = content.replace('</style>', f'{gallery_css}\n  </style>')

    # Update Sections
    # Yoyogi
    yoyogi_pattern = r'(<section id="gallery">.*?<div[^>]*?>).*?(</div>)'
    content = re.sub(yoyogi_pattern, f'\\1\n{yoyogi_grid}\n\\2\n    <button class="view-more-btn" onclick="toggleGallery(this, \'gallery-grid-yoyogi\')">VIEW MORE</button>', content, flags=re.DOTALL)
    content = content.replace('<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:0.5rem; margin-bottom: 0.5rem;" class="reveal">', '<div id="gallery-grid-yoyogi" class="gallery-grid reveal">')

    # Club Que
    que_pattern = r'(2026.02.06 復活ワンマン @ 下北沢 Club Que</p>\s*<div[^>]*?>).*?(</div>)'
    content = re.sub(que_pattern, f'\\1\n{que_grid}\n\\2\n    <button class="view-more-btn" onclick="toggleGallery(this, \'gallery-grid-que\')">VIEW MORE</button>', content, flags=re.DOTALL)
    content = content.replace('2026.02.06 復活ワンマン @ 下北沢 Club Que</p>\n    <div class="reveal" style="display:grid; grid-template-columns:repeat(4, 1fr); gap:0.5rem;">', '2026.02.06 復活ワンマン @ 下北沢 Club Que</p>\n    <div id="gallery-grid-que" class="gallery-grid reveal">')

    # Add JS and Lightbox HTML
    js_and_modal = """
    <!-- Lightbox Modal -->
    <div id="lightbox" onclick="this.style.display='none'">
      <img src="" alt="Full Size Photo">
    </div>

    <script>
    function openLightbox(src) {
      const lb = document.getElementById('lightbox');
      lb.querySelector('img').src = src;
      lb.style.display = 'flex';
    }

    function toggleGallery(btn, sectionId) {
      const container = document.getElementById(sectionId);
      const hiddenImages = container.querySelectorAll('.gallery-thumb.hidden-img');
      const isHidden = hiddenImages[0].style.display === 'none';
      
      hiddenImages.forEach(img => {
        img.style.display = isHidden ? 'block' : 'none';
      });
      
      btn.textContent = isHidden ? 'SHOW LESS' : 'VIEW MORE';
    }
    </script>
    """
    content = content.replace('</body>', f'{js_and_modal}\n</body>')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Gallery structure updated with Lightbox and View More features.")

if __name__ == "__main__":
    generate_gallery_html()
