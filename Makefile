test:
	python setup.py test

release:
	python setup.py sdist --format=zip,bztar,gztar register upload


flake8:
	flake8 --ignore=E501 disguise
	flake8 --ignore=E501 tests.py
	flake8 --ignore=E501 setup.py


coverage:
	coverage run --include=disguise/*.py setup.py test
	coverage html


coveralls:
	coveralls --config_file=coverage.rc

clean:
	rm -rf *.egg *.egg-info
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;
