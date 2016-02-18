.DEFAULT_GOAL := test

install:
	python setup.py install

test:
	python setup.py nosetests -v --with-coverage --cover-package=msgpack --cover-html
