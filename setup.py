import setuptools
import pkg_resources


with open("README.md", "r") as fh:
  long_description = fh.read()


setuptools.setup(
  name="monitoring",
  version='0.1',
  license="MIT",
  author="Ravil Dorozhinskii",
  author_email="ravil.aviva.com@gmail.com",
  description="Performance Monitoring for SeisSol",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  url="https://github.com/ravil-mobile/monitoring/wiki",
  python_requires='>=3.5',
  include_package_data=True,
)