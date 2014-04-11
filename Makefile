.PHONY: all build test clean clean_pyc
.SILENT: test

all: sdist

clean:
	python setup.py clean_all -a

clean_pyc:
	python setup.py clean_pyc -a

test:
	python setup.py test

sdist:
	python setup.py sdist

build:
	python setup.py bdist

install:
	python setup.py install

