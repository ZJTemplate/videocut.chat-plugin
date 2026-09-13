"""Verify bundled release checksums and ZIP integrity without installing anything."""

import hashlib
import re
import zipfile
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1] / "releases/v0.2.1"
    expected = {
        "saycut_tools-0.2.1-py3-none-any.whl",
        "videocut-chat-plugin-0.2.1.zip",
    }
    seen = set()
    for line in (root / "SHA256SUMS").read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        if name not in expected or name in seen or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("Unexpected checksum entry")
        seen.add(name)
        path = root / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("Checksum mismatch: " + name)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError("Invalid archive: " + name)
        print("Verified: " + name)
    if seen != expected:
        raise ValueError("Missing checksum entries")


if __name__ == "__main__":
    main()
