import json
import yaml
from pathlib import Path

def merge_goroku():
    goroku_path = Path("data/debu_goroku.json")
    facts_path = Path("blog-x/config/Devparade_facts.yaml")
    
    if not goroku_path.exists():
        print("debu_goroku.json not found.")
        return
        
    with open(goroku_path, "r", encoding="utf-8") as f:
        goroku = json.load(f)
    
    # 語録をテキスト形式にまとめる
    goroku_text = "\n【デブ語録・ポジデブ変換辞書】\n"
    for cat in goroku.values():
        for item in cat:
            goroku_text += f"- {item['word']}: {item['description']}\n"
    
    if facts_path.exists():
        with open(facts_path, "r", encoding="utf-8") as f:
            facts = f.read()
    else:
        facts = "Devparade Facts:\n"
    
    if "【デブ語録・ポジデブ変換辞書】" not in facts:
        new_facts = facts + "\n" + goroku_text
        with open(facts_path, "w", encoding="utf-8") as f:
            f.write(new_facts)
        print("Merged debu_goroku.json into Devparade_facts.yaml")
    else:
        print("Goroku already merged.")

if __name__ == "__main__":
    merge_goroku()
