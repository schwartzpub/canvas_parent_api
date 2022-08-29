import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="canvas_parent_api",
    version="0.0.10",
    author="Jacob Schwartz",
    author_email="jake@schwartzpub.com",
    description="",
    long_description=long_description,
    license="MIT",
    package_dir={"canvas_parent_api":"src"},
    packages=["canvas_parent_api"],
    install_requires=[
        "aiohttp",
        "pydantic>=1.8.2,<1.10.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)