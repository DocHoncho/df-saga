import os
import sys

from setuptools import setup
sys.path.append('./src')

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = 'saga',
        version = '0.1',
        author = 'Joel Madigan',
        author_email = 'dochoncho@gmail.com',
        description = ("Dwarf Fortress data file tool, useful for working with the legends xml dump"),
        license = 'BSD',
        keywords = 'dwarffortress xml python',
        url = '',
        packages = ['saga'],

        long_description = read('README'),
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "Liscense :: OSI Approved :: BSD Liscense",
            ],
        )

