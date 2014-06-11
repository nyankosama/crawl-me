import json, os, codecs

os.system("pandoc README.md -f markdown -t rst -o README.txt")
os.system("pandoc CHANGELOG.md -f markdown -t rst -o CHANGELOG.txt")

os.system("python setup.py register")

os.remove("README.txt")
os.remove("CHANGELOG.txt")
