import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()


setuptools.setup(
  name='py-aquael',
  version='0.0.3',
  scripts=['aquael.py'],
  author="Christopher Haglund",
  description="A python library for the Aquael Leddy link unofficial API",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/choffah/py-aquael",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: BSD License",
      "Operating System :: OS Independent",
  ],
 )