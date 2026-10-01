"""Build two standalone Windows applications from the current Python installation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from importlib.util import find_spec


PROJECT = Path(__file__).resolve().parent


def build(name: str, entry: str, *, assistant: bool) -> None:
    command = [
        # Use the console bootloader but hide a console created by Explorer.
        # Some Windows installs fail to start PyInstaller's windowed bootloader
        # with "ordinal 380 not found" (ComCtl32 v6 / manifest loading).
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
        "--console", "--hide-console", "hide-early",
        "--name", name, "--distpath", str(PROJECT / "dist"),
        "--workpath", str(PROJECT / "build"),
        "--specpath", str(PROJECT / "build"),
        "--paths", str(PROJECT),
        "--icon", str(PROJECT / "icon.ico"),
        "--add-data", f"{PROJECT / 'icon.ico'};.",
        "--add-data", f"{PROJECT / 'config.toml'};.",
        "--collect-all", "edge_tts", "--collect-data", "certifi",
    ]
    # Vosk can also transcribe full commands when selected in settings.
    if find_spec("vosk") is not None:
        command.extend(["--collect-all", "vosk"])
    if find_spec("piper") is not None:
        command.extend(["--collect-all", "piper"])
    if find_spec("espeakng_loader") is not None:
        command.extend(["--collect-all", "espeakng_loader"])
    command.append(str(PROJECT / entry))
    print("Building", name, flush=True)
    subprocess.run(command, cwd=PROJECT, check=True)


def main() -> None:
    if sys.platform != "win32":
        raise SystemExit("Windows is required to build .exe files")
    try:
        import PyInstaller  # noqa: F401
    except ImportError as exc:
        raise SystemExit("Install the builder: python -m pip install pyinstaller") from exc
    # Both ensurepip and PyInstaller's module discovery need to launch another
    # python.exe. Detect Windows access denial before the multi-minute build.
    try:
        subprocess.run([sys.executable, "-I", "-c", "pass"], cwd=PROJECT,
                       stdin=subprocess.DEVNULL, check=True, timeout=15)
    except PermissionError as exc:
        raise SystemExit(
            "Windows denied launching a child python.exe (WinError 5). "
            "Check Windows Security protection history, or use "
            ".github/workflows/build-windows.yml to build in GitHub Actions."
        ) from exc
    try:
        build("Orbit Assistant", "assistant_app.py", assistant=True)
        build("Orbit Settings", "settings_app.py", assistant=False)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            "PyInstaller failed. If the log shows WinError 5 from subprocess.Popen "
            "or CreateProcess, Windows blocked a child process. Check Windows "
            "Security protection history or build with GitHub Actions."
        ) from exc
    print("Done: dist\\Orbit Assistant.exe and dist\\Orbit Settings.exe", flush=True)


if __name__ == "__main__":
    main()
