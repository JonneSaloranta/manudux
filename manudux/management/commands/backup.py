import shutil
import sqlite3
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Back up the SQLite database and media files into a single archive."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            default=str(settings.BASE_DIR / "backups"),
            help="Directory to write the backup archive to (default: BASE_DIR/backups)",
        )

    def handle(self, *args, **options):
        output_dir = Path(options["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        work_dir = output_dir / f".backup-{timestamp}"
        work_dir.mkdir()

        try:
            db_backup_path = work_dir / "db.sqlite3"
            self._backup_database(db_backup_path)

            archive_path = output_dir / f"manudux-backup-{timestamp}.tar.gz"
            media_root = Path(settings.MEDIA_ROOT)
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(db_backup_path, arcname="db.sqlite3")
                if media_root.exists():
                    tar.add(media_root, arcname="media")
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

        self.stdout.write(self.style.SUCCESS(f"Backup written to {archive_path}"))

    def _backup_database(self, db_backup_path):
        # Use SQLite's own backup API for a consistent snapshot even while
        # the app is writing to the database, instead of copying the file.
        # Read the path off the live connection rather than settings.DATABASES
        # directly, since the test runner points the connection at a
        # different file than what's statically configured.
        db_path = connections["default"].settings_dict["NAME"]
        source = sqlite3.connect(str(db_path))
        try:
            dest = sqlite3.connect(str(db_backup_path))
            try:
                source.backup(dest)
            finally:
                dest.close()
        finally:
            source.close()
