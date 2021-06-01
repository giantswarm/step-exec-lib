import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="step-exec-lib",
    version="0.0.1",
    author="Łukasz Piątkowski",
    author_email="lukasz@giantswarm.io",
    description="A library that helps execute pipeline of tasks using filters and simple composition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giantswarm/step-exec-lib",
    packages=setuptools.find_packages(where="step_exec_lib/**/*.py"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
