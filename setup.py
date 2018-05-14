from setuptools import setup

import satoricore

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=satoricore.__name__,
    description=satoricore.__desc__,
    version=satoricore.__version__,

    author="Satori-NG org",
    author_email=satoricore.__email__,

    packages=["satoricore"],

    entry_points={
        "console_scripts": [
            "satori-file=satoricore.file.__main__:main",
        ],
    },
    install_requires=requirements,

)


