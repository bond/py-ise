import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cisco-ise-bond",
    version="0.0.1",
    author="Daniel Bond",
    author_email="db@conscia.com",
    description="Package for interfacing Cisco ISE API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bond/py-ise",
    packages=setuptools.find_packages(),
    keywords="cisco ise",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    py_modules=['ise'],
    scripts=['ise-util.py'],
    install_requires=['requests']
)
