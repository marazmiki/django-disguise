test:
	python setup.py test


release:
	python setup.py sdist --format=zip,bztar,gztar register upload
	python setup.py bdist_wheel register upload


flake8:
	flake8 \
		disguise \
		tests.py \
		setup.py


coverage:
	coverage run --rcfile=.coveragerc --include=disguise/*.py setup.py test
	coverage html


coveralls:
	coveralls

clean:
	rm -rf *.egg *.egg-info
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;
