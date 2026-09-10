import shutil
import tarfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = (
        "Restore the SQLite database and media files from an archive created "
        "by the backup command. Overwrites the current database and media."
    )

    def add_arguments(self, parser):
        parser.add_argument("archive", help="Path to a manudux-backup-*.tar.gz file")
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip the confirmation prompt (needed for non-interactive use)",
        )

    def handle(self, *args, **options):
        archive_path = Path(options["archive"])
        if not archive_path.exists():
            raise CommandError(f"No such file: {archive_path}")

        if not options["yes"]:
            confirm = input(
                "This overwrites the current database and media files. Continue? [y/N] "
            )
            if confirm.lower() != "y":
                self.stdout.write("Aborted.")
                return

        db_path = Path(connections["default"].settings_dict["NAME"])
        media_root = Path(settings.MEDIA_ROOT)

        extract_dir = archive_path.parent / f".restore-{archive_path.stem}"
        extract_dir.mkdir(parents=True, exist_ok=True)
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(extract_dir, filter="data")

            # Close the open connection before replacing the file it points
            # at; restart the app afterwards so it reconnects cleanly.
            connections["default"].close()

            db_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(extract_dir / "db.sqlite3", db_path)

            extracted_media = extract_dir / "media"
            if extracted_media.exists():
                if media_root.exists():
                    shutil.rmtree(media_root)
                shutil.copytree(extracted_media, media_root)
        finally:
            shutil.rmtree(extract_dir, ignore_errors=True)

        self.stdout.write(
            self.style.SUCCESS("Restore complete. Restart the app to pick it up.")
        )
