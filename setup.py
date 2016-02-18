from setuptools import setup, find_packages

setup(
    name='msgpack',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    version='1.2.0',
    description='Python implementation of the MessagePack serialization format',
    author='David Haines',
    author_email='david@polyglotted.co',
    url='https://github.com/polyglotted/msgpack-python',
    download_url='https://github.com/polyglotted/msgpack-python/tarball/1.2.0',
    keywords=['msgpack'],
    classifiers=[],
    setup_requires=[
        'nose==1.3.7'
    ],
    tests_require=[
        'coverage==3.7.1',
        'sure==1.2.24'
    ]
)
