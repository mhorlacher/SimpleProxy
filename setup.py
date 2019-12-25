import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleProxy",
    version="0.1",
    author="Marc Horlacher",
    author_email="marc.horlacher@gmail.com",
    description="Scraping interface for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhorlacher/PyProxy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

