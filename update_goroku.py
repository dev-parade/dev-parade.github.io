import json

with open('/Users/coyass/kaihatsu/dev-parade-site/data/debu_goroku.json', 'r', encoding='utf-8') as f:
    goroku = json.load(f)

# 1. Move GPU from "ka" to "sa"
gpu_item = None
for item in goroku.get('ka', []):
    if 'GPU' in item['word']:
        gpu_item = item
        break
if gpu_item:
    goroku['ka'].remove(gpu_item)
    if 'sa' not in goroku:
        goroku['sa'] = []
    goroku['sa'].append(gpu_item)

# 2. Add fat humor entries to specific sections
new_entries = {
    'na': [
        {
            "word": "二重あご",
            "description": "富と幸福の象徴。あるいは進化の過程で獲得した、衝撃吸収用の予備バンパー。",
            "is_update": True
        },
        {
            "word": "ニク（肉）",
            "description": "全人類を一つにする平和の使者。毎食欠かすことのできない我々のメインヒロイン。",
            "is_update": True
        },
        {
            "word": "眠気",
            "description": "血糖値が最高潮に達したことを知らせる身体からのファンファーレ。",
            "is_update": True
        },
        {
            "word": "飲み物",
            "description": "カレー、麻婆豆腐、ハンバーグなど、固形物に見えるもの全てを指す。噛む時間はロス。",
            "is_update": True
        }
    ],
    'ma': [
        {
            "word": "満腹中枢",
            "description": "デブパレードのメンバーには標準搭載されていない、あるいは遠い昔に物理破壊されたリミッター。",
            "is_update": True
        },
        {
            "word": "無重力",
            "description": "体重100kgを超えた時にのみ感じることができる、お腹の脂肪が勝手に浮いているような感覚。",
            "is_update": True
        },
        {
            "word": "飯テロ",
            "description": "深夜の時間帯に投下される画像爆弾。我々にとってはただの「夜食のメニュー表」である。",
            "is_update": True
        }
    ],
    'ya': [
        {
            "word": "夜食",
            "description": "1日の締めくくりに行われる、自分への甘すぎるご褒美。これを食べないと1日がリセットされない。",
            "is_update": True
        },
        {
            "word": "痩せる",
            "description": "辞書には載っているが、現実世界では観測されない未確認現象。または明日の自分への責任転嫁。",
            "is_update": True
        },
        {
            "word": "やっちまった",
            "description": "深夜2時のラーメン大盛り完食後に発せられる、歓喜とほんの少しの反省が入り混じった魔法の言葉。",
            "is_update": True
        }
    ],
    'ra': [
        {
            "word": "ラーメン",
            "description": "スープ（水分）、麺（炭水化物）、チャーシュー（タンパク質）からなる完全食。基本は1日3杯から。",
            "is_update": True
        },
        {
            "word": "ライス",
            "description": "どんなおかずでも優しく受け止める白いキャンバス。おかずが無くても、ライスでライスが食える。",
            "is_update": True
        },
        {
            "word": "ロース",
            "description": "カルビの相棒。脂と赤身の黄金比を誇る、デブにとってのアイドル的部位。",
            "is_update": True
        }
    ],
    'wa': [
        {
            "word": "割り勘",
            "description": "デブが圧倒的に勝利を収めるゲーム。一般的な食事会では最も経済的効果を発揮するシステム。",
            "is_update": True
        },
        {
            "word": "わんこそば",
            "description": "自分の限界を知るためのスポーツ。100杯からがウォームアップ。",
            "is_update": True
        },
        {
            "word": "輪ゴム",
            "description": "かつてズボンのボタンの代わりに使われた伝説のアイテム。現在は弾け飛ぶため非推奨。",
            "is_update": True
        }
    ]
}

for key, entries in new_entries.items():
    if key not in goroku:
        goroku[key] = []
    goroku[key].extend(entries)

with open('/Users/coyass/kaihatsu/dev-parade-site/data/debu_goroku.json', 'w', encoding='utf-8') as f:
    json.dump(goroku, f, ensure_ascii=False, indent=2)

print("Goroku updated successfully!")
