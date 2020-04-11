.PHONY: runserver
runserver:
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=example_project.settings django-admin runserver

.PHONY: shell
shell:
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=example_project.settings django-admin shell

.PHONY: i18n
i18n:
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=example_project.settings django-admin makemessages -l ru --keep-pot
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=example_project.settings django-admin compilemessages

.PHONY: deploy
deploy:
	git push heroku master

.PHONY: sphinx
sphinx:
	cd docs && make livehtml

.PHONY: test
test:
	echo

release:
	python setup.py sdist --format=zip,bztar,gztar register upload
	python setup.py bdist_wheel register upload

