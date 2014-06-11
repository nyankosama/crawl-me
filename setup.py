PROJECT_METADATA = "project.json"

import json, os, codecs
here = os.path.abspath(os.path.dirname(__file__))
proj_conf = json.loads(open(os.path.join(here, PROJECT_METADATA)).read())

long_description = proj_conf["short_description"]
if os.path.exists("README.txt") or os.path.exists("CHANGELOG.txt"):
    README = codecs.open(os.path.join(here, 'README.txt'), "w", "utf8")
    CHANGELOG = codecs.open(os.path.join(here, 'CHANGELOG.txt'), "w", "utf8")
    long_description = README + "\n\n" + CHANGELOG

from setuptools import setup, find_packages

setup(
    name = proj_conf["name"],
    version = proj_conf["version"],

    packages = find_packages(),
    install_requires = ['pyquery>=1.2.5'],

    author = proj_conf["author"],
    author_email = proj_conf["author_email"],
    url = proj_conf["url"],
    license = proj_conf["license"],

    description = proj_conf["description"],
    classifiers = proj_conf["classifiers"],
    keywords = proj_conf["keywords"],

    long_description = long_description,

    platforms = 'any',
    include_package_data = True,

    entry_points = {
        'console_scripts': proj_conf["console_scripts"]
    }
)
