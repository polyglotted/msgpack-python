.DEFAULT_GOAL := test

testdeps:
	pip install -r test-requirements.txt

install:
	python setup.py install

test:
	py.test tests --html=test-report.html
