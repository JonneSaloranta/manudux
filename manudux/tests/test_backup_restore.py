import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TransactionTestCase, override_settings, tag

from manudux.models import PropertyType


class BackupRestoreTestCase(TransactionTestCase):

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp_dir, ignore_errors=True)

        self.media_root = self.tmp_dir / "media"
        self.media_root.mkdir()
        (self.media_root / "properties").mkdir()
        (self.media_root / "properties" / "photo.png").write_bytes(b"fake-image")

        self.backup_dir = self.tmp_dir / "backups"

    @tag("management", "backup")
    def test_backup_then_restore_round_trip(self):
        PropertyType.objects.create(name="Residential", description="A home")

        with override_settings(MEDIA_ROOT=str(self.media_root)):
            call_command("backup", output_dir=str(self.backup_dir))

        archives = list(self.backup_dir.glob("manudux-backup-*.tar.gz"))
        self.assertEqual(len(archives), 1, msg="Expected exactly one backup archive")

        # Simulate data loss: delete the row and the uploaded file.
        PropertyType.objects.all().delete()
        shutil.rmtree(self.media_root)
        self.media_root.mkdir()
        self.assertFalse((self.media_root / "properties" / "photo.png").exists())

        with override_settings(MEDIA_ROOT=str(self.media_root)):
            call_command("restore", str(archives[0]), yes=True)

        self.assertTrue(
            PropertyType.objects.filter(name="Residential").exists(),
            msg="Database row was not restored",
        )
        self.assertTrue(
            (self.media_root / "properties" / "photo.png").exists(),
            msg="Media file was not restored",
        )
