import back_da_dev


def test_package_imports():
    assert hasattr(back_da_dev, "__version__")
    assert back_da_dev.__version__ == "0.0.1"
    assert hasattr(back_da_dev, "main")
