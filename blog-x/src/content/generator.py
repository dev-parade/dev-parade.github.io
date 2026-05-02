"""
COYASS Auto-Posting System - Content Generator
AI-powered content generation with COYASS persona.
"""

import os
import yaml
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
import requests
import json
import re
import hashlib



logger = logging.getLogger(__name__)

# COYASS 共通ガイドライン
COYASS_BASE_GUIDELINES = """
【文体ガイドライン】
1. 専門性と親しみやすさの融合：歯科の専門知識を噛み砕いて伝える
2. ラッパー的なリズム感：要所にパンチラインを入れる
3. 実体験ベース：「今日こうだった」「俺の経験では」というリアルさ
4. 読者への呼びかけ：「みんなも試してみて」的な巻き込み力
5. ポジティブだけど現実的：成功も失敗も正直に語る
6. 医療広告ガイドラインを意識：誇大表現は避ける

【禁止事項】
- AIが書いたとわかるような定型表現（「いかがでしたでしょうか」等）
- 過度に丁寧な敬語（タメ口と敬語を自然にミックス）
- 根拠のない治療効果の断言
- 他の歯科医院的の批判
"""



class ContentGenerator:
    """AI を使ったコンテンツ生成エンジン"""

    def __init__(self, config: dict):
        self.config = config
        self.ai_config = config.get("ai", {})
        self.persona = config.get("persona", {})
        self.templates_dir = Path(__file__).parent.parent.parent / "config/content_templates"
        self.history_file = Path(__file__).parent.parent.parent.parent / "data/posted_tweets.json"
        self._setup_ai_clients()

    def _setup_ai_clients(self):
        """AI クライアントの初期化"""
        self.openai_client = None
        self.gemini_model = None
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key and not self.anthropic_api_key.startswith("sk-xxxx"):
            logger.info("✅ Anthropic (Claude) API Key found in environment")


        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "sk-xxxxxxxxxxxxxxxxxxxx":
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=api_key)
                logger.info("✅ OpenAI client initialized")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI init failed: {e}")

        # Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "AIzaxxxxxxxxxxxxxxxxxxxxxxx":
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model_name = self.ai_config.get("gemini", {}).get("model", "gemini-2.0-flash")
                self.gemini_model = genai.GenerativeModel(model_name)
                logger.info("✅ Gemini client initialized")
            except Exception as e:
                logger.warning(f"⚠️ Gemini init failed: {e}")

    def _load_template(self, category: str) -> str:
        """カテゴリ別テンプレートを読み込む"""
        template_path = self.templates_dir / f"{category}.md"
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
        logger.warning(f"Template not found: {template_path}")
        return ""

    def generate_note_article(self, category: str, topic: str = None,
                               input_data: str = None, role: str = None) -> dict:
        """Note用の長文記事を生成する"""
        role = role or self._get_best_role(category)
        system_prompt = self._get_system_prompt(role)
        
        template = self._load_template(category)
        length_config = self.config.get("note", {}).get("article_length", {})
        min_len = length_config.get("min", 2000)
        max_len = length_config.get("max", 5000)

        user_prompt = self._build_note_prompt(category, topic, input_data, min_len, max_len, template)

        result = self._call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=self.ai_config.get("openai", {}).get("max_tokens", 4000)
        )

        if result:
            # タイトルと本文を分離
            title, body = self._parse_article(result["text"])
            hashtags = self._generate_hashtags(category, role=role)
            return {
                "title": title,
                "body": body,
                "category": category,
                "role": role,
                "hashtags": hashtags,
                "word_count": len(body),
                "ai_provider": result["provider"],
                "ai_model": result["model"]
            }
        return None

    def generate_x_post(self, category: str, topic: str = None,
                         input_data: str = None, note_article: str = None, role: str = None) -> dict:
        """X (Twitter) 用の短文投稿を生成する"""
        role = role or self._get_best_role(category)
        system_prompt = self._get_system_prompt(role)
        max_chars = self.config.get("x", {}).get("max_chars", 280)

        template = self._load_template(category)
        
        # デブパレードのファクトデータを読み込み（posidevカテゴリ用）
        facts = ""
        if category == "posidev":
            facts_path = Path("config/Devparade_facts.yaml")
            if facts_path.exists():
                with open(facts_path, "r", encoding="utf-8") as f:
                    facts = f.read()

        if note_article:
            user_prompt = f"""以下のnote記事を元に、X（Twitter）用の投稿を1つ作成してください。

【記事内容】
{note_article[:1500]}

【条件】
- {max_chars}文字以内（ハッシュタグ含む）
- 記事への興味を引く内容
- note記事へのリンクを貼ることを前提に
- 現在の役割（{role}）にふさわしい口調で
"""
        else:
            user_prompt = f"""X（Twitter）用の投稿を1つ作成してください。

【カテゴリ】{category}
【トピック】{topic or "今日の話題を自由に"}
{f"【参考情報】{input_data}" if input_data else ""}
{f"【デブパレード公認データ】\n{facts}" if facts else ""}
{f"【テンプレート・指示】\n{template}" if template else ""}

【条件】
- {max_chars}文字以内（ハッシュタグ含む）
- 現在の役割（{role}）にふさわしい口調で
- 読んだ人が「いいね」したくなる内容
- AIっぽさを排除し、熱い「ポジデブ」スピリットで
- 歯科医師ネタ、パパネタは【厳禁】
"""

        max_attempts = 3
        for attempt in range(max_attempts):
            result = self._call_ai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=500
            )

            if result:
                text = result["text"].strip().strip('"').strip("'")
                
                # --- 本文の徹底お掃除 ---
                # 1. AIが本文中に勝手に入れたハッシュタグをすべて削除（システム側で付与するため）
                text = re.sub(r'#\S+', '', text).strip()
                
                # 2. X APIで問題になりやすい特殊記号（★）を置換
                text = text.replace("★", "-")
                
                # 3. 連続する改行を1つに整理
                text = re.sub(r'\n{3,}', '\n\n', text)
                # ---------------------

                hashtags = self._generate_hashtags(category, for_x=True, role=role)
                # ハッシュタグを付加（文字数制限内で）
                if len(text) + len(hashtags) + 2 <= max_chars:
                    full_text = f"{text}\n\n{hashtags}"
                else:
                    full_text = text[:max_chars]

                # ガードレールチェック
                if self._is_hallucination_suspected(full_text):
                    logger.warning(f"⚠️ Hallucination suspected (attempt {attempt+1}), retrying...")
                    continue
                
                if self._is_duplicate(full_text):
                    logger.warning(f"🔁 Duplicate content detected (attempt {attempt+1}), retrying...")
                    continue

                return {
                    "text": full_text[:max_chars],
                    "category": category,
                    "role": role,
                    "ai_provider": result["provider"],
                    "ai_model": result["model"],
                    "hash": self._calculate_hash(full_text)
                }
        
        logger.error(f"❌ Failed to generate unique/safe content after {max_attempts} attempts.")
        return None

    def _get_system_prompt(self, role: str) -> str:
        """ロールに基づいたシステムプロンプトを取得"""
        roles = self.persona.get("roles", {})
        role_info = roles.get(role, roles.get("personal", {}))
        
        prompt = f"""あなたはCOYASS（{self.persona.get('real_name', '小安正洋')}）として活動します。
現在の役割は【{role_info.get('title', '個人')}】です。

【フォーカス】
{role_info.get('focus', '日常の気づき')}

【トーン】
{role_info.get('tone', '自然体')}

{COYASS_BASE_GUIDELINES}
"""
        return prompt

    def _get_best_role(self, category: str) -> str:
        """カテゴリから最適なロールを推測"""
        category_map = {
            "dental_tips": "doctor",
            "industry": "doctor",
            "music_review": "artist",
            "posidev": "artist",
            "career": "personal",
            "food_health": "personal",
            "parenting": "personal",
            "daily_doc": "personal"
        }
        return category_map.get(category, "personal")


    def _build_note_prompt(self, category: str, topic: str, input_data: str,
                            min_len: int, max_len: int, template: str) -> str:
        """Note記事生成用のプロンプトを組み立てる"""
        prompt = f"""以下の条件でnote記事を1本書いてください。

【カテゴリ】{category}
【トピック】{topic or "今日の話題を自由に選んでください"}
{f"【参考情報・メモ】{input_data}" if input_data else ""}
【文字数】{min_len}〜{max_len}文字
【形式】
- 最初の1行目にタイトル（## は不要、テキストのみ）
- 2行目以降が本文
- 見出しはMarkdown形式（## ）を使用
- 箇条書きも適宜使用
- 最後に読者への呼びかけで締める

{f"【テンプレート参考】{template}" if template else ""}

重要：AIが書いたとわかる定型文は絶対に使わないでください。
COYASSが実際にキーボードを叩いて書いているように、生きた言葉で書いてください。
"""
        return prompt

    def _call_ai(self, system_prompt: str, user_prompt: str,
                  max_tokens: int = 4000) -> Optional[dict]:
        """AIプロバイダーを呼び出す（プライマリ→フォールバック）"""
        primary = self.ai_config.get("primary_provider", "openai")
        fallback = self.ai_config.get("fallback_provider", "gemini")

        # プライマリプロバイダーで試行
        result = self._call_provider(primary, system_prompt, user_prompt, max_tokens)
        if result:
            return result

        # フォールバック
        logger.warning(f"Primary ({primary}) failed, trying fallback ({fallback})")
        return self._call_provider(fallback, system_prompt, user_prompt, max_tokens)

    def _call_provider(self, provider: str, system_prompt: str,
                        user_prompt: str, max_tokens: int) -> Optional[dict]:
        """特定のAIプロバイダーを呼び出す"""
        try:
            if provider == "openai" and self.openai_client:
                model = self.ai_config.get("openai", {}).get("model", "gpt-4o")
                temp = self.ai_config.get("openai", {}).get("temperature", 0.8)
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temp
                )
                return {
                    "text": response.choices[0].message.content,
                    "provider": "openai",
                    "model": model
                }

            elif provider == "gemini" and self.gemini_model:
                model_name = self.ai_config.get("gemini", {}).get("model", "gemini-2.0-flash")
                combined_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"
                response = self.gemini_model.generate_content(combined_prompt)
                return {
                    "text": response.text,
                    "provider": "gemini",
                    "model": model_name
                }

            elif provider == "anthropic" and self.anthropic_api_key:
                model_name = self.ai_config.get("anthropic", {}).get("model", "claude-3-5-sonnet-20240620")
                headers = {
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                data = {
                    "model": model_name,
                    "max_tokens": max_tokens,
                    "system": system_prompt,
                    "messages": [
                        {"role": "user", "content": user_prompt}
                    ]
                }
                resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
                if resp.status_code == 200:
                    result_json = resp.json()
                    return {
                        "text": result_json["content"][0]["text"],
                        "provider": "anthropic",
                        "model": model_name
                    }
                else:
                    logger.error(f"Anthropic API error: {resp.status_code} - {resp.text}")



        except Exception as e:
            logger.error(f"AI call failed ({provider}): {e}")
        return None

    def _parse_article(self, raw_text: str) -> tuple:
        """生成テキストからタイトルと本文を分離"""
        lines = raw_text.strip().split("\n")
        title = lines[0].strip().lstrip("#").strip() if lines else "無題"
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else raw_text
        return title, body

    def _generate_hashtags(self, category: str, for_x: bool = False, role: str = None) -> str:
        """カテゴリとロールに応じたハッシュタグを生成"""
        role = role or self._get_best_role(category)
        roles = self.persona.get("roles", {})
        tags = list(roles.get(role, {}).get("hashtags", []))

        # ハッシュタグのクリーンアップ（★などの特殊記号を置換）
        cleaned_tags = []
        for tag in tags:
            # X APIで問題になりやすい特殊記号を置換
            cleaned = tag.replace("★", "-")
            cleaned_tags.append(cleaned)

        if for_x:
            # X用は最大3個に絞る
            cleaned_tags = cleaned_tags[:3]

        return " ".join(cleaned_tags)

    def _calculate_hash(self, text: str) -> str:
        """ツイートのハッシュ値を計算（重複検知用）"""
        # 空白と一部の記号を除去して正規化
        normalized = re.sub(r'\s+', '', text.strip())
        normalized = re.sub(r'[!！?？.。🍖#＃]', '', normalized)
        return hashlib.md5(normalized.encode()).hexdigest()[:12]

    def _is_hallucination_suspected(self, text: str) -> bool:
        """ハルシネーション（嘘の逸話）の疑いがあるツイートを検知"""
        suspicious_keywords = [
            "ネットで募集", "インターネットで募集", "結成理由", "結成当初", 
            "アラバキ", "ARABAKI", "出演決定", "応募した", "募集した",
            "解散理由", "入団テスト", "逸話", "事実まとめ",
            "弟子募集中", "メンバー募集", "新メンバー"
        ]
        for kw in suspicious_keywords:
            if kw in text:
                return True
        return False

    def _is_duplicate(self, text: str) -> bool:
        """過去の投稿と重複しているかチェック"""
        if not self.history_file.exists():
            return False
            
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                posted_hashes = set(data.get("posted", []))
                return self._calculate_hash(text) in posted_hashes
        except Exception as e:
            logger.error(f"Error checking history: {e}")
            return False

    def mark_as_posted(self, tweet_hash: str):
        """ツイートを投稿済みとしてマーク（履歴ファイルに保存）"""
        if not self.history_file.exists():
            data = {"posted": [], "scores": {}, "cycle": 1}
        else:
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                logger.error(f"Error loading history for marking: {e}")
                data = {"posted": [], "scores": {}, "cycle": 1}

        if tweet_hash not in data.get("posted", []):
            data.setdefault("posted", []).append(tweet_hash)
            
            # 追加のメタデータ記録
            data.setdefault("scores", {})[tweet_hash] = {
                "score": 100, # 新規生成分は100点として扱う
                "posted_at": datetime.now().isoformat()
            }

            try:
                os.makedirs(self.history_file.parent, exist_ok=True)
                with open(self.history_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                logger.info(f"📝 Marked as posted (hash: {tweet_hash})")
            except Exception as e:
                logger.error(f"Error saving history: {e}")
