from setuptools import setup, find_packages

setup(
    name='msgpack',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    version='1.3.1',
    description='Python implementation of the MessagePack serialization format',
    author='David Haines',
    author_email='david@polyglotted.co',
    url='https://github.com/polyglotted/msgpack-python',
    download_url='https://github.com/polyglotted/msgpack-python/tarball/1.3.1',
    keywords=['msgpack'],
    classifiers=[],
    setup_requires=[
        'pytest-runner>=2.0,<3dev'
    ],
    tests_require=[
        'coverage==4.1b2',
        'pytest==2.9.1',
        'pytest-html==1.8.0'
    ]
)
