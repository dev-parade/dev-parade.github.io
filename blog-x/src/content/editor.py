"""
COYASS Auto-Posting System - Content Editor
品質チェックとCOYASS語調の最終調整
"""

import re
import logging

logger = logging.getLogger(__name__)

# AI生成っぽい定型表現のブラックリスト
AI_PATTERNS = [
    r"いかがでしたでしょうか",
    r"いかがでしたか",
    r"最後までお読みいただき",
    r"ありがとうございました。",
    r"参考になれば幸いです",
    r"お役に立てれば",
    r"以上、.*でした",
    r"それでは、また",
    r"まとめると、",
    r"今回は.*について.*ました",
    r"皆さん、こんにちは[。！]",
]

# COYASS語調チェックポイント
COYASS_MARKERS = [
    "俺",
    "マジで",
    "ヤバい",
    "ぶっちゃけ",
    "リアルに",
]


class ContentEditor:
    """コンテンツの品質チェックと調整"""

    def check_quality(self, text: str, platform: str = "note") -> dict:
        """記事の品質をチェックする"""
        issues = []
        score = 100

        # 1. AI定型表現チェック
        for pattern in AI_PATTERNS:
            if re.search(pattern, text):
                issues.append(f"⚠️ AI定型表現を検出: '{pattern}'")
                score -= 10

        # 2. 文字数チェック
        char_count = len(text)
        if platform == "note":
            if char_count < 1500:
                issues.append(f"⚠️ 文字数が少なすぎます ({char_count}文字, 推奨2000+)")
                score -= 15
            elif char_count > 6000:
                issues.append(f"⚠️ 文字数が多すぎます ({char_count}文字, 推奨5000以下)")
                score -= 5
        elif platform == "x":
            if char_count > 280:
                issues.append(f"❌ X投稿の文字数制限超過 ({char_count}/280文字)")
                score -= 30

        # 3. COYASS語調チェック
        coyass_count = sum(1 for marker in COYASS_MARKERS if marker in text)
        if platform == "note" and coyass_count < 2:
            issues.append("💡 COYASS語調が薄い可能性があります。もっと砕けた表現を追加推奨")
            score -= 5

        # 4. 見出し構造チェック (note)
        if platform == "note":
            headings = re.findall(r"^##\s", text, re.MULTILINE)
            if len(headings) < 2:
                issues.append("💡 見出し（##）を増やすと読みやすくなります")
                score -= 5

        # 5. 禁止表現チェック
        forbidden = ["確実に治ります", "絶対に", "100%", "必ず治る"]
        for word in forbidden:
            if word in text:
                issues.append(f"❌ 医療広告ガイドライン違反の可能性: '{word}'")
                score -= 20

        return {
            "score": max(0, score),
            "issues": issues,
            "char_count": char_count,
            "passed": score >= 60
        }

    def remove_ai_patterns(self, text: str) -> str:
        """AI定型表現を除去する"""
        for pattern in AI_PATTERNS:
            text = re.sub(pattern, "", text)
        # 空行の連続を整理
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def add_coyass_footer(self, text: str, category: str) -> str:
        """COYASS風のフッターを追加する"""
        footers = {
            "dental_tips": "\n\n---\n\n🦷 歯のことで気になることがあったら、いつでも中目黒コヤス歯科に来てくれ。\n待ってるぜ！ ✌️",
            "music_review": "\n\n---\n\n🎤 音楽は最高の薬だ。今日も良い音楽と共に。\nPeace. 🎵",
            "food_health": "\n\n---\n\n🍽️ 食べることは生きること、そして歯はその入り口。\n大事にしような！ 💪",
            "career": "\n\n---\n\n💪 歯科医もラッパーも、どっちも本気でやるから面白い。\n人生は一度きり、全力で行こうぜ。 🔥",
            "parenting": "\n\n---\n\n👨‍👧‍👦 子供たちの笑顔が、俺の最高のモチベーション。\nパパ頑張るぜ！ 🌟",
            "posidev": "\n\n---\n\n🍖 デブは才能。脂肪は努力の結晶。\nDevparadeの「バッチコイ!!!」聴いて元気出してくれよな！ 🤘",
            "daily_doc": "\n\n---\n\n🔥 今日も全力で生きた。明日もよろしく。\nCOYASS 🤘",
        }
        footer = footers.get(category, "\n\n---\n\n🔥 COYASS 🤘")
        return text + footer
