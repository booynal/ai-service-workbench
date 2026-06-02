from pathlib import Path
import os
import shutil
import stat
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "tools" / "install_lead_engine.sh"
REMOVE = ROOT / "tools" / "remove_lead_engine.sh"
PLIST_NAME = "com.booynal.ai-service-workbench.plist"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(INSTALL.exists(), "missing tools/install_lead_engine.sh")
    require(REMOVE.exists(), "missing tools/remove_lead_engine.sh")
    INSTALL.chmod(INSTALL.stat().st_mode | stat.S_IXUSR)
    REMOVE.chmod(REMOVE.stat().st_mode | stat.S_IXUSR)

    fake_home = Path(tempfile.mkdtemp(prefix="lead-engine-home-"))
    try:
      env = os.environ.copy()
      env["HOME"] = str(fake_home)
      env["DRY_RUN"] = "1"

      install = subprocess.run(
          [str(INSTALL)],
          cwd=ROOT,
          env=env,
          capture_output=True,
          text=True,
      )
      require(install.returncode == 0, f"install failed: {install.stderr or install.stdout}")

      target = fake_home / "Library" / "LaunchAgents" / PLIST_NAME
      require(target.exists(), "install should copy launch agent plist to fake HOME")

      remove = subprocess.run(
          [str(REMOVE)],
          cwd=ROOT,
          env=env,
          capture_output=True,
          text=True,
      )
      require(remove.returncode == 0, f"remove failed: {remove.stderr or remove.stdout}")
      require(not target.exists(), "remove should delete launch agent plist from fake HOME")
    finally:
      shutil.rmtree(fake_home)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
