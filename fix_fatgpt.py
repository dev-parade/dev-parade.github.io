import re

file_path = '/Users/coyass/kaihatsu/dev-parade-site/lyrics/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace FAT GPTwo with FAT GPT
new_html = html.replace('FAT GPTwo', 'FAT GPT')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Replaced FAT GPTwo with FAT GPT")
