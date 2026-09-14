"""Verify bundled release checksums and ZIP integrity without installing anything."""

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path


def main():
    repository = Path(__file__).resolve().parents[1]
    current = json.loads((repository / "plugins/videocut-chat/plugin.json").read_text())["version"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=current)
    version = parser.parse_args().version
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("Expected a release version such as 0.2.2")
    root = repository / "releases" / f"v{version}"
    expected = {
        f"saycut_tools-{version}-py3-none-any.whl",
        f"videocut-chat-plugin-{version}.zip",
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
