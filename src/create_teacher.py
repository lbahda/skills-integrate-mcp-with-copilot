"""Create or update a local teacher account for the activities API."""

import getpass
import json
import os

from app import hash_teacher_password, teacher_credentials_file


def main():
    username = input("Teacher username: ").strip()
    if not username:
        raise SystemExit("Teacher username cannot be empty.")

    password = getpass.getpass("Teacher password (at least 12 characters): ")
    if len(password) < 12:
        raise SystemExit("Teacher password must be at least 12 characters.")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("Passwords do not match.")

    if teacher_credentials_file.exists():
        try:
            configuration = json.loads(teacher_credentials_file.read_text())
            teachers = configuration["teachers"]
            if not isinstance(teachers, dict):
                raise ValueError
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            raise SystemExit("Teacher credentials file is invalid; refusing to overwrite it.") from None
    else:
        teachers = {}

    teachers[username] = hash_teacher_password(password)
    teacher_credentials_file.write_text(
        json.dumps({"teachers": teachers}, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(teacher_credentials_file, 0o600)
    print(f"Teacher account '{username}' saved to {teacher_credentials_file}.")


if __name__ == "__main__":
    main()