import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="refdict",
    version="3.2.0",
    author="DiscreteTom",
    author_email="discrete_tom@outlook.com",
    description="add reference for dict in python using formatted string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DiscreteTom/refdict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)