import fq26gp2


def test_package_imports():
    assert hasattr(fq26gp2, "__version__")
    assert fq26gp2.__version__ == "0.1.0"
    assert hasattr(fq26gp2, "main")
