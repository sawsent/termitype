from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
readme = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="termitype",
    version="0.0.2",
    description="A minimalist terminal typing speed test with extensible architecture.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="sawsent",
    license="Apache-2.0",

    packages=find_packages(where="src"),
    package_dir={"": "src"},

    package_data={
        "termitype": [
            "static/*.json",
            "static/languages/*.json",
        ]
    },
    include_package_data=True,

    install_requires=[
        "platformdirs>=3.0.0"
    ],

    entry_points={
        "console_scripts": [
            "termitype = termitype.cli.bootstrap:bootstrap",
        ]
    },

    python_requires=">=3.9",
)

