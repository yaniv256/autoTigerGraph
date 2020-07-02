import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoTigerGraph",
    version="0.0.2",
    author="Yaniv Ben-Ami",
    author_email="yaniv256@gmail.com",
    description="A package for automaticaly generating TigerGraph schema and upserting data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yaniv256/autoTigerGraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6',
)
