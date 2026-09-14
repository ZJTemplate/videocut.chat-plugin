"""Install a trusted Saycut wheel into a plugin-owned environment, never the user's site-packages."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import venv
import zipfile
from email.parser import Parser
from pathlib import Path


def owned_root(path):
    path = path.expanduser().absolute()
    marker = path / ".saycut-plugin-runtime"
    if path.is_symlink() or marker.is_symlink():
        raise ValueError("Plugin runtime paths cannot be symbolic links")
    if path.exists() and (not marker.is_file() or marker.read_text() != "saycut-runtime-v1\n"):
        raise ValueError("Refusing to reuse a directory not owned by this installer")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)
    if not marker.exists():
        marker.write_text("saycut-runtime-v1\n")
    return path


def install(args):
    if sys.version_info < (3, 11):  # noqa: UP036 - standalone installer may run before the package exists
        raise ValueError("Python 3.11 or later is required")
    wheel = args.wheel.expanduser().resolve(strict=True)
    if wheel.suffix != ".whl":
        raise ValueError("Expected a built Saycut wheel")
    with zipfile.ZipFile(wheel) as archive:
        metadata_files = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(metadata_files) != 1:
            raise ValueError("Invalid wheel metadata")
        metadata = Parser().parsestr(archive.read(metadata_files[0]).decode())
        if metadata.get("Name") != "saycut-tools":
            raise ValueError("This installer only accepts saycut-tools wheels")
    plugin = args.plugin_source.expanduser().resolve(strict=True)
    if not (plugin / ".codex-plugin/plugin.json").is_file():
        raise ValueError("Provide the unpacked videocut.chat plugin directory")
    roots = [path.expanduser().resolve(strict=True) for path in args.allow_root]
    if not all(path.is_dir() for path in roots):
        raise ValueError("Allowed media roots must be directories")
    constraint = getattr(args, "constraint", None)
    if constraint:
        constraint = constraint.expanduser().resolve(strict=True)
        if not constraint.is_file():
            raise ValueError("Constraints must be a file")
    runtime = args.runtime_dir.expanduser().resolve(strict=True) if args.runtime_dir else None
    if runtime and not runtime.is_dir():
        raise ValueError("Native runtime must be a directory containing skymedia")
    root = owned_root(args.root)
    config = root / "saycut.json"
    if config.is_symlink():
        raise ValueError("The private configuration cannot be a symbolic link")
    if config.exists():
        existing = json.loads(config.read_text())
        if not isinstance(existing, dict) or existing.get("account_enabled") is not True:
            raise ValueError("Existing private configuration must explicitly enable account authorization")
    wheel_hash = hashlib.sha256(wheel.read_bytes()).hexdigest()
    environment = root / ("python-" + wheel_hash[:12] + ("-asr" if args.asr else ""))
    if environment.is_symlink():
        raise ValueError("The private Python environment cannot be a symbolic link")
    venv.EnvBuilder(with_pip=True).create(environment)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("PYTHON", "PIP_", "SAYCUT_")) and key != "VIRTUAL_ENV"
    }
    env["PIP_CONFIG_FILE"] = os.devnull
    extras = "native,asr" if args.asr else "native"
    subprocess.run(
        [
            str(python),
            "-I",
            "-m",
            "pip",
            "--isolated",
            "install",
            "--require-virtualenv",
            "--no-input",
            "--prefix",
            str(environment),
            *(["--constraint", str(constraint)] if constraint else []),
            str(wheel) + "[" + extras + "]",
        ],
        env=env,
        check=True,
    )
    subprocess.run(
        [str(python), "-I", "-m", "pip", "--isolated", "check"],
        env=env,
        check=True,
    )
    settings = existing if config.exists() else {
            "account_enabled": True,
            "data_dir": str(root / "data"),
            "allowed_roots": [str(path) for path in roots],
            "asr_backend": "faster_whisper" if args.asr else "disabled",
            "asr_allow_model_download": False,
        }
    settings['allowed_roots'] = list(dict.fromkeys([*settings.get('allowed_roots', []), *(str(path) for path in roots)]))
    if runtime:
        settings['runtime_dir'] = str(runtime)
    if args.asr and settings.get('asr_backend', 'disabled') == 'disabled':
        settings['asr_backend'] = 'faster_whisper'
    temporary = config.with_suffix('.installing.json')
    with temporary.open('x', encoding='utf-8') as stream:
        os.chmod(temporary, 0o600)
        json.dump(settings, stream, indent=2)
    os.replace(temporary, config)
    if getattr(args, 'download_resources', False):
        subprocess.run([str(python), '-I', '-m', 'saycut_tools.cli', '--config', str(config), 'setup-resources'], env=env, check=True)
    if getattr(args, 'download_model', False):
        if not args.asr:
            raise ValueError('--download-model requires --asr')
        subprocess.run([str(python), '-I', '-m', 'saycut_tools.cli', '--config', str(config),
                        'configure-asr', '--backend', 'faster_whisper', '--model', 'small', '--download-model'], env=env, check=True)
    subprocess.run(
        [
            str(python),
            "-I",
            "-m",
            "saycut_tools.cli",
            "--config",
            str(config),
            "export-integrations",
            "--plugin-source",
            str(plugin),
            "--output",
            str(root / "integrations"),
        ],
        env=env,
        check=True,
    )
    return {
        "python": str(python),
        "config": str(config),
        "integrations": str(root / "integrations"),
        "wheel_sha256": wheel_hash,
        "global_python_modified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument(
        "--plugin-source", type=Path, default=Path(__file__).resolve().parents[2] / "plugins/videocut-chat"
    )
    parser.add_argument("--root", type=Path, default=Path.home() / ".local/share/saycut-plugin")
    parser.add_argument("--allow-root", type=Path, action="append", required=True)
    parser.add_argument("--runtime-dir", type=Path)
    parser.add_argument("--asr", action="store_true")
    parser.add_argument('--download-resources', action='store_true', help='Explicitly download native binaries and install bundled effects')
    parser.add_argument('--download-model', action='store_true', help='Explicitly download the local ASR model (requires --asr)')
    parser.add_argument(
        "--constraint", type=Path, help="Tested pip constraints for this OS and Python version"
    )
    args = parser.parse_args()
    try:
        print(json.dumps(install(args), indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
