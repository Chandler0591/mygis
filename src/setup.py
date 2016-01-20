from setuptools import setup, find_packages
setup(
    name = "arccore",
    version = "0.1",
    packages = find_packages(),
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],
    # metadata for upload to PyPI
    author = "zhoufl3",
    author_email = "zhoufl3@asiainfo.com",
    description = "This is core arcgis service for gis-platform",
    license = "PSF",
    keywords = "core arcgis service gis-platform",
    url = "http://example.com/CoreService/",
)