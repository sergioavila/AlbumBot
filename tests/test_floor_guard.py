import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("COV_CORE_") and key != "COVERAGE_PROCESS_START"
    }
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_floor_guard_blocks_new_suppression(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    guard = scripts / "floor_guard.py"
    shutil.copy(Path("scripts/floor_guard.py"), guard)

    run("git", "init", "-b", "main", cwd=tmp_path)
    run("git", "config", "user.name", "AlbumBot Test", cwd=tmp_path)
    run("git", "config", "user.email", "test@albumbot.invalid", cwd=tmp_path)
    run("git", "add", ".", cwd=tmp_path)
    baseline = run("git", "commit", "-m", "baseline", cwd=tmp_path)
    assert baseline.returncode == 0

    clean = run(sys.executable, str(guard), cwd=tmp_path)
    assert clean.returncode == 0

    forbidden_comment = "# no" + "qa\n"
    (tmp_path / "unsafe.py").write_text(forbidden_comment, encoding="utf-8")

    blocked = run(sys.executable, str(guard), cwd=tmp_path)
    assert blocked.returncode == 1
    assert "[silenced-checker] unsafe.py" in blocked.stderr
