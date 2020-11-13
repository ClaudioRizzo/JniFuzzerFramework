import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TaintSaviour-WebApp",
    version="0.0.1",
    author="Claudio Rizzo",
    author_email="claudio.rizzo.90@gmail.com",
    description="TaintSaviour WebApp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ClaudioRizzo/TaintSaviour",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)