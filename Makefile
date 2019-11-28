VERSION=2.0.0
BUILDDIR?='~build'
PYTHONPATH:=${PWD}/tests/:${PWD}
PG_ETOOLS_PARAMS?=-U postgres -p 15432 -h 127.0.0.1
PGHOST=127.0.0.1
PGUSER=postgres

.mkbuilddir:
	mkdir -p ${BUILDDIR}

help:
	echo ""


develop:
	@poetry run
	poetry run pre-commit install
	poetry run pre-commit install --hook-type pre-push.
	$(MAKE) .init-db


.init-db:
	psql -h ${PGHOST} -c 'DROP DATABASE IF EXISTS etools_datamart;' -U ${PGUSER}
	psql -h ${PGHOST} -c 'CREATE DATABASE etools_datamart;' -U $PGUSER

test:
	pipenv run py.test -v --create-db

lint:
	pipenv run pre-commit run --all-files
	pipenv run pre-commit run --all-files --hook-stage push
	pipenv run pre-commit run --all-files --hook-stage manual

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml .eggs
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	rm -f db/clean.sql db/etools.dump db/public.sqldump db/tenant.sql

fullclean:
	rm -fr .tox .cache .pytest_cache .venv
	$(MAKE) clean

sync-etools:
	sh src/etools_datamart/apps/multitenant/postgresql/dump.sh ${PG_ETOOLS_PARAMS}

docs: .mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/ ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif

stack:
	PYTHONPATH=./src poetry run celery worker -A etools_datamart --loglevel=DEBUG --concurrency=4 --purge --pidfile celery.pid &
	PYTHONPATH=./src poetry run celery beat -A etools_datamart.celery --loglevel=DEBUG --pidfile beat.pid &
#	PYTHONPATH=./src pipenv run gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi --pid gunicorn.pid &
	poetry run docker run  -d -p 5555:5555 -e CELERY_BROKER_URL=${CELERY_BROKER_URL} --name datamart-flower --rm saxix/flower

