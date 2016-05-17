from setuptools import setup, find_packages

with open('test-requirements.txt') as f:
    test_requirements = f.read().splitlines()

setup(
    name='msgpack',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    version='1.3.0',
    description='Python implementation of the MessagePack serialization format',
    author='David Haines',
    author_email='david@polyglotted.io',
    url='https://github.com/polyglotted/msgpack-python',
    download_url='https://github.com/polyglotted/msgpack-python/tarball/1.3.0',
    keywords=['msgpack'],
    classifiers=[],
    tests_require=test_requirements
)
