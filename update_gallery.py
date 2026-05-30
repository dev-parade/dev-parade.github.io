import glob

html_file = "index.html"
with open(html_file, "r") as f:
    content = f.read()

images = sorted(glob.glob("assets/IMG_*.JPG"))
img_tags = []
for idx, img in enumerate(images):
    img_tags.append(f"""      <img src="{img}" alt="Devparade at 代々木第二体育館 {idx+5}" loading="lazy" style="width:100%; aspect-ratio:3/2; object-fit:cover; cursor:pointer; filter:grayscale(10%); transition:filter 0.3s;" onmouseover="this.style.filter='grayscale(0)'" onmouseout="this.style.filter='grayscale(10%)'">""")

# Find the injection point inside the Yoyogi gallery grid
target_str = """<img src="assets/yoyogi_4.jpg" alt="Devparade at 代々木第二体育館 4" onerror="this.src='https://placehold.co/600x400/222/555?text=Yoyogi+Photo+4'" style="width:100%; aspect-ratio:3/2; object-fit:cover; cursor:pointer; filter:grayscale(10%); transition:filter 0.3s;" onmouseover="this.style.filter='grayscale(0)'" onmouseout="this.style.filter='grayscale(10%)'">"""

if target_str in content:
    new_content = content.replace(target_str, target_str + "\n" + "\n".join(img_tags))
    with open(html_file, "w") as f:
        f.write(new_content)
    print("Successfully updated index.html with 114 photos.")
else:
    print("Could not find the target string in index.html")
