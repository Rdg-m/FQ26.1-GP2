import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_command(args, cwd=PROJECT_ROOT, env=None):
    env = env or os.environ.copy()
    result = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"Command failed: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}\n"
        )
    return result


def test_build_package_wheel(tmp_path):
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()

    run_command([
        sys.executable,
        "-m",
        "pip",
        "wheel",
        ".",
        "-w",
        str(wheel_dir),
        "--no-deps",
    ])

    wheels = list(wheel_dir.glob("*back_da_dev-*.whl"))
    assert len(wheels) == 1, f"Expected one wheel file, found: {wheels}"
    assert wheels[0].is_file()

    target_dir = tmp_path / "installed"
    run_command([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--target",
        str(target_dir),
        "--no-deps",
        str(wheels[0]),
    ])

    env = os.environ.copy()
    env["PYTHONPATH"] = str(target_dir)

    result = run_command([
        sys.executable,
        "-c",
        "import back_da_dev; print(back_da_dev.__version__)",
    ], env=env)
    assert "0.0.2" in result.stdout.strip()

    result = run_command([
        sys.executable,
        "-m",
        "back_da_dev",
        "--help",
    ], env=env)
    assert "back_da_dev" in result.stdout or result.returncode == 0


def test_import_package_from_src_layout():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

    result = run_command(
        [
            sys.executable,
            "-c",
            "import back_da_dev; print(back_da_dev.__version__)"
        ],
        env=env,
    )
    assert "0.0.2" in result.stdout.strip()