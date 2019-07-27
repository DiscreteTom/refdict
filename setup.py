import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="refdict",
    version="3.3.0",
    author="DiscreteTom",
    author_email="discrete_tom@outlook.com",
    description="Using string as chain keys to realize chain access and reference access of dict in python",
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