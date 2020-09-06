from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="minecraft-remapper",
    version="1.0.0",
    author="Nearata",
    author_email="williamdicicco@protonmail.com",
    description="A Minecraft remapper for already deobfuscated source code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nearata/minecraft-remapper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console"
    ],
    python_requires=">=3.8",
    install_requires=[
        "click==7.1.2",
        "colorama==0.4.3"
    ]
)
