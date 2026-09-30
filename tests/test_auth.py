import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from src.app import hash_teacher_password, require_teacher


class TeacherAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.credentials_file = Path(self.directory.name) / "teachers.json"
        credentials_patch = patch("src.app.teacher_credentials_file", self.credentials_file)
        credentials_patch.start()
        self.addCleanup(credentials_patch.stop)

    def save_teacher(self, username="teacher", password="correct horse battery staple"):
        self.credentials_file.write_text(
            json.dumps({"teachers": {username: hash_teacher_password(password)}}),
            encoding="utf-8",
        )

    def test_missing_credentials_file_disables_teacher_access(self):
        with self.assertRaises(HTTPException) as raised:
            require_teacher(None)
        self.assertEqual(raised.exception.status_code, 503)

    def test_anonymous_request_is_rejected(self):
        self.save_teacher()
        with self.assertRaises(HTTPException) as raised:
            require_teacher(None)
        self.assertEqual(raised.exception.status_code, 401)

    def test_valid_teacher_password_is_accepted(self):
        self.save_teacher()
        credentials = HTTPBasicCredentials(
            username="teacher", password="correct horse battery staple"
        )
        self.assertEqual(require_teacher(credentials), "teacher")

    def test_invalid_teacher_password_is_rejected(self):
        self.save_teacher()
        credentials = HTTPBasicCredentials(username="teacher", password="incorrect")
        with self.assertRaises(HTTPException) as raised:
            require_teacher(credentials)
        self.assertEqual(raised.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main()