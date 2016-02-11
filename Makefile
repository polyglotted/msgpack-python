.DEFAULT_GOAL := test

install:
	python setup.py install

test:
	nosetests -v --with-coverage --cover-package=msgpack --cover-html
