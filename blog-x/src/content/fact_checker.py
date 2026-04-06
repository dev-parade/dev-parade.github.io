"""
COYASS Auto-Posting System - Fact Checker
デブパレード及びCOYASS関連の事実確認レイヤー
AI生成コンテンツの嘘を防止する
"""

import yaml
import re
import logging
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


class FactChecker:
    """ファクトデータに基づくコンテンツ検証"""

    def __init__(self, facts_path: str = "config/Devparade_facts.yaml"):
        self.facts = {}
        self.member_names = []
        self.load_facts(facts_path)

    def load_facts(self, path: str):
        """ファクトデータを読み込む"""
        p = Path(path)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                self.facts = yaml.safe_load(f) or {}
            # メンバー名リストを作成
            for m in self.facts.get("members", []):
                self.member_names.append(m["name"])
                if "real_name" in m:
                    self.member_names.append(m["real_name"])
            for m in self.facts.get("ex_members", []):
                self.member_names.append(m["name"])
            logger.info(f"✅ Loaded facts: {len(self.member_names)} names registered")
        else:
            logger.warning(f"⚠️ Facts file not found: {path}")

    def check_content(self, text: str) -> Tuple[bool, List[str]]:
        """コンテンツの事実関係をチェック"""
        issues = []
        
        # 1. 体重の捏造チェック
        weight_issues = self._check_weight_claims(text)
        issues.extend(weight_issues)

        # 2. 身長の捏造チェック
        height_issues = self._check_height_claims(text)
        issues.extend(height_issues)

        # 3. 存在しないメンバー名チェック
        fake_member_issues = self._check_fake_members(text)
        issues.extend(fake_member_issues)

        # 4. 曲名・アルバム名の捏造チェック
        music_issues = self._check_music_claims(text)
        issues.extend(music_issues)

        passed = len(issues) == 0
        return passed, issues

    def _check_weight_claims(self, text: str) -> List[str]:
        """体重に関する記述をチェック"""
        issues = []
        known_weights = {}
        for m in self.facts.get("members", []):
            if m.get("weight_2008") and m["weight_2008"] != "不明":
                known_weights[m["name"]] = m["weight_2008"]
        for m in self.facts.get("ex_members", []):
            if m.get("weight_2008") and m["weight_2008"] != "不明":
                known_weights[m["name"]] = m["weight_2008"]

        # テキスト内の体重記述を検出
        for name in self.member_names:
            # "〇〇は XXXkg" パターン
            patterns = [
                rf"{re.escape(name)}[はが]?\s*(\d+)\s*kg",
                rf"{re.escape(name)}.*?体重[はが]?\s*(\d+)",
                rf"{re.escape(name)}.*?(\d+)\s*キロ",
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for weight_str in matches:
                    claimed_weight = weight_str
                    known = known_weights.get(name)
                    if known:
                        known_num = known.replace("kg", "")
                        if claimed_weight != known_num:
                            # 現在の体重として書いている可能性
                            issues.append(
                                f"⚠️ {name}の体重 {claimed_weight}kg："
                                f"2008年の公式データは{known}です。"
                                f"現在の体重は非公開です。"
                            )
                    else:
                        issues.append(
                            f"❌ {name}の体重 {claimed_weight}kg：公式データがありません。"
                            f"捏造の可能性があります。"
                        )
        return issues

    def _check_height_claims(self, text: str) -> List[str]:
        """身長の捏造チェック（全メンバー非公開）"""
        issues = []
        for name in self.member_names:
            patterns = [
                rf"{re.escape(name)}.*?身長[はが]?\s*(\d+)",
                rf"{re.escape(name)}.*?(\d+)\s*cm",
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for height in matches:
                    h = int(height)
                    if 140 <= h <= 210:  # 身長っぽい値
                        issues.append(
                            f"❌ {name}の身長 {height}cm：身長は非公開です。捏造しないでください。"
                        )
        return issues

    def _check_fake_members(self, text: str) -> List[str]:
        """存在しないメンバー名の検出"""
        issues = []
        # "メンバーの〇〇" パターンで知らない名前を検出
        patterns = [
            r"メンバーの(\w+)",
            r"デブパレードの(\w+)",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for name in matches:
                if (name not in self.member_names and
                        name not in ["メンバー", "曲", "ライブ", "復活", "再結成",
                                     "総体重", "結成", "解散", "活動", "デビュー"]):
                    # 既知のメンバーでない場合、警告
                    if len(name) >= 2:  # 1文字は無視
                        issues.append(
                            f"⚠️ '{name}' はデブパレードの既知メンバーではありません。確認してください。"
                        )
        return issues

    def _check_music_claims(self, text: str) -> List[str]:
        """楽曲・アルバム情報の検証"""
        issues = []
        known_songs = ["BODY&SOUL", "cosmic mind"]
        
        # 「新曲」「新アルバム」等の言及チェック
        if re.search(r"(新曲|ニューシングル|新アルバム)「(.+?)」", text):
            matches = re.findall(r"(新曲|ニューシングル|新アルバム)「(.+?)」", text)
            for release_type, title in matches:
                if title not in known_songs:
                    issues.append(
                        f"⚠️ {release_type}「{title}」：確認済みデータにありません。"
                        f"実在するか確認してください。"
                    )
        return issues

    def get_grounding_prompt(self) -> str:
        """AIプロンプトに付加するファクトグラウンディング指示"""
        members_info = []
        for m in self.facts.get("members", []):
            info = f"- {m['name']} ({m['role']})"
            if m.get("weight_2008") and m["weight_2008"] != "不明":
                info += f" / 2008年体重: {m['weight_2008']}"
            if m.get("current_weight"):
                info += f" / 現在体重: {m['current_weight']}"
            members_info.append(info)

        rules = self.facts.get("rules", [])
        rules_text = "\n".join(f"- {r}" for r in rules)

        return f"""
【デブパレード ファクトデータ - 必ず遵守】

バンド名: {self.facts.get('band', {}).get('name', 'デブパレード')}
結成: {self.facts.get('band', {}).get('formed', '不明')}年
レーベル: {self.facts.get('band', {}).get('label', '不明')}
デビュー曲: {self.facts.get('band', {}).get('major_debut', {}).get('single', '不明')}
結成時総体重: {self.facts.get('band', {}).get('total_weight_at_formation', '不明')}
解散: {self.facts.get('band', {}).get('disbanded', '不明')}年（理由: {self.facts.get('band', {}).get('disband_reason', '不明')}）
再結成: {self.facts.get('band', {}).get('reunion', '不明')}年（{self.facts.get('band', {}).get('reunion_rule', '')})

メンバー:
{chr(10).join(members_info)}

【絶対ルール】
{rules_text}
- 上記にない情報は「不明」として扱い、絶対に捏造しない
- 面白いデブネタ・ジョークはOKだが、「事実」として嘘を書かない
- ジョークの場合は明らかに冗談とわかる書き方にすること
"""
