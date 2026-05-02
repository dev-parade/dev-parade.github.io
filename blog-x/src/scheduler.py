"""
COYASS Auto-Posting System - Scheduler
APScheduler による投稿ジョブ管理
"""

import yaml
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

# 曜日マッピング
WEEKDAY_MAP = {
    "monday": 0, "tuesday": 1, "wednesday": 2,
    "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
}
WEEKDAY_NAMES = list(WEEKDAY_MAP.keys())


class PostScheduler:
    """投稿スケジューラ"""

    def __init__(self, config: dict, generator, note_publisher, x_publisher, repository):
        self.config = config
        self.generator = generator
        self.note_pub = note_publisher
        self.x_pub = x_publisher
        self.repo = repository
        self.scheduler = AsyncIOScheduler(timezone=config.get("app", {}).get("timezone", "Asia/Tokyo"))
        self.dry_run = config.get("app", {}).get("dry_run", True)

    def load_schedules(self, schedule_path: str = "config/schedule.yaml"):
        """スケジュール定義を読み込んでジョブを登録"""
        path = Path(schedule_path)
        if not path.exists():
            logger.error(f"Schedule file not found: {schedule_path}")
            return

        with open(path, "r", encoding="utf-8") as f:
            schedule_config = yaml.safe_load(f)

        schedules = schedule_config.get("schedules", {})

        for name, sched in schedules.items():
            cron_parts = sched["cron"].split()
            if len(cron_parts) != 5:
                logger.warning(f"Invalid cron for {name}: {sched['cron']}")
                continue

            trigger = CronTrigger(
                minute=cron_parts[0],
                hour=cron_parts[1],
                day=cron_parts[2],
                month=cron_parts[3],
                day_of_week=cron_parts[4]
            )

            platform = sched.get("platform", "x")

            if platform == "note":
                self.scheduler.add_job(
                    self._execute_note_job,
                    trigger=trigger,
                    id=name,
                    name=sched.get("description", name),
                    kwargs={
                        "schedule_name": name,
                        "category": self._resolve_category(sched),
                        "template": sched.get("template", "note_main"),
                        "role": sched.get("role")
                    }
                )
            elif platform == "monitor":
                self.scheduler.add_job(
                    self._execute_monitor_job,
                    trigger=trigger,
                    id=name,
                    name=sched.get("description", name),
                    kwargs={
                        "schedule_name": name
                    }
                )
            else:
                self.scheduler.add_job(
                    self._execute_x_job,
                    trigger=trigger,
                    id=name,
                    name=sched.get("description", name),
                    kwargs={
                        "schedule_name": name,
                        "category": sched.get("category", "daily_doc"),
                        "template": sched.get("template", "tweet"),
                        "role": sched.get("role")
                    }
                )

            logger.info(f"📅 Scheduled: {name} ({sched['cron']}) -> {platform}")

    def _resolve_category(self, sched: dict) -> str:
        """曜日に応じたカテゴリを解決"""
        if "category_rotation" in sched:
            today = WEEKDAY_NAMES[datetime.now().weekday()]
            return sched["category_rotation"].get(today, "daily_doc")
        return sched.get("category", "daily_doc")

    async def _execute_note_job(self, schedule_name: str, category: str, template: str, role: str = None):

        """Note投稿ジョブの実行"""
        logger.info(f"🚀 Executing Note job: {schedule_name} (category: {category})")

        try:
            # 1. 未使用の入力データを確認
            inputs = self.repo.get_unused_inputs(category=category)
            input_data = inputs[0].body if inputs else None

            # 2. コンテンツ生成
            article = self.generator.generate_note_article(
                category=category,
                input_data=input_data,
                role=role
            )


            if not article:
                logger.error(f"❌ Content generation failed for {schedule_name}")
                return

            # 3. DRY_RUNチェック
            if self.dry_run:
                logger.info(f"🏃 [DRY RUN] Would post to Note:")
                logger.info(f"   Title: {article['title']}")
                logger.info(f"   Length: {article['word_count']} chars")
                logger.info(f"   Category: {article['category']}")
                return

            # 画像の自動生成 (DRY RUNではない場合のみ)
            from src.content.image_generator import ImageGenerator
            image_gen = ImageGenerator(self.config)
            image_path = image_gen.generate_cover_image(article["title"], category)

            # 4. DBに保存
            from src.data.models import Content
            content = Content(
                category=category,
                title=article["title"],
                body=article["body"],
                hashtags=article["hashtags"],
                ai_provider=article["ai_provider"],
                ai_model=article["ai_model"],
                word_count=article["word_count"]
            )
            content = self.repo.save_content(content)

            # 5. Note投稿
            result = await self.note_pub.publish_article(
                title=article["title"],
                body=article["body"],
                hashtags=article["hashtags"],
                image_path=image_path
            )

            # 6. 投稿結果を記録
            if result:
                self.repo.create_post(
                    content_id=content.id,
                    platform="note",
                    scheduled_at=datetime.utcnow()
                )
                self.repo.update_post_status(
                    post_id=content.id,
                    status=result["status"],
                    platform_url=result.get("url"),
                    published_at=datetime.utcnow()
                )
                logger.info(f"✅ Note article posted: {article['title']}")
            else:
                logger.error(f"❌ Note posting failed: {article['title']}")

        except Exception as e:
            logger.error(f"❌ Note job error: {e}", exc_info=True)

    async def _execute_x_job(self, schedule_name: str, category: str, template: str, role: str = None):

        """X投稿ジョブの実行"""
        logger.info(f"🚀 Executing X job: {schedule_name} (category: {category})")

        try:
            # 1. コンテンツ生成
            post = self.generator.generate_x_post(
                category=category,
                role=role
            )


            if not post:
                logger.error(f"❌ X content generation failed for {schedule_name}")
                return

            # 2. DRY_RUNチェック
            if self.dry_run:
                logger.info(f"🏃 [DRY RUN] Would post to X:")
                logger.info(f"   Text: {post['text']}")
                return

            # 3. DBに保存
            from src.data.models import Content
            content = Content(
                category=category,
                title=f"X: {post['text'][:50]}...",
                body=post["text"],
                ai_provider=post["ai_provider"],
                ai_model=post["ai_model"],
                word_count=len(post["text"])
            )
            content = self.repo.save_content(content)

            # 4. X投稿
            result = self.x_pub.post_tweet(text=post["text"])

            # 5. 投稿結果を記録
            if result:
                # DBに記録
                self.repo.create_post(
                    content_id=content.id,
                    platform="x",
                    scheduled_at=datetime.utcnow()
                )
                # JSON履歴にも記録（重複検知用）
                if "hash" in post:
                    self.generator.mark_as_posted(post["hash"])
                
                logger.info(f"✅ X post published: {result['url']}")
            else:
                logger.error(f"❌ X posting failed")

        except Exception as e:
            logger.error(f"❌ X job error: {e}", exc_info=True)

    async def _execute_monitor_job(self, schedule_name: str):
        """SNS監視 & 自動返信ジョブの実行"""
        logger.info(f"📡 Executing Monitor job: {schedule_name}")

        try:
            # 旧スクリプトのロジックを実行
            # (実際には blog-x 内に整理されたロジックとして移管するのが望ましいが、一旦既存スクリプトを呼び出す)
            import subprocess
            script_path = Path(__file__).parent.parent.parent / "scripts/debu-posi-search-free.py"
            
            if not script_path.exists():
                logger.error(f"❌ Monitor script not found: {script_path}")
                return

            if self.dry_run:
                logger.info(f"🏃 [DRY RUN] Would run monitor script: {script_path}")
                return

            process = await asyncio.create_subprocess_exec(
                "python3", str(script_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                logger.info(f"✅ Monitor job completed successfully")
                if stdout:
                    logger.debug(f"Monitor output: {stdout.decode()}")
            else:
                logger.error(f"❌ Monitor job failed with exit code {process.returncode}")
                if stderr:
                    logger.error(f"Monitor error: {stderr.decode()}")

        except Exception as e:
            logger.error(f"❌ Monitor job error: {e}", exc_info=True)

    def start(self):
        """スケジューラを開始"""
        self.scheduler.start()
        logger.info("🟢 Scheduler started!")

    def stop(self):
        """スケジューラを停止"""
        self.scheduler.shutdown()
        logger.info("🔴 Scheduler stopped")

    def get_scheduled_jobs(self) -> list:
        """登録済みジョブ一覧を取得"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run": str(job.next_run_time) if job.next_run_time else "N/A",
                "trigger": str(job.trigger)
            })
        return jobs
