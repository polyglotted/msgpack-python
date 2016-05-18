.DEFAULT_GOAL := test

testdeps:
	pip install -r test-requirements.txt --no-cache-dir

install:
	python setup.py install

test:
	py.test tests -rw --cov=msgpack --cov-report=term --cov-report=html --html=test-report.html
