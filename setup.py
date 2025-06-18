from setuptools import setup, find_packages

setup(
    name="ShopEase",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyinstaller",
    ],
    package_data={
        "shopease": ["assets/*"],
    },
    entry_points={
        "console_scripts": [
            "shopease = shopease.app:main",
        ],
    },
)