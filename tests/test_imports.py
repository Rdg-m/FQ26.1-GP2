import importlib
import sys
from pathlib import Path

import back_da_dev

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"


def test_package_imports():
    assert hasattr(back_da_dev, "__version__")
    assert back_da_dev.__version__ == "0.0.2"
    assert hasattr(back_da_dev, "main")
    assert hasattr(back_da_dev, "run_standard_backtest")
    assert hasattr(back_da_dev, "generate_backtest_report")
    assert hasattr(back_da_dev, "list_strategies")


def collect_src_modules():
    modules = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        if path.name == "__init__.py" and path.parent == SRC_ROOT:
            continue

        module_name = ".".join(path.relative_to(SRC_ROOT).with_suffix("").parts)
        modules.append(module_name)
    return modules


def test_src_modules_are_importable():
    sys.path.insert(0, str(SRC_ROOT))
    try:
        for module_name in collect_src_modules():
            importlib.import_module(module_name)
    finally:
        sys.path.pop(0)
