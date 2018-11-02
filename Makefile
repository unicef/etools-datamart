VERSION=2.0.0
BUILDDIR='~build'
PYTHONPATH:=${PWD}/tests/:${PWD}
DBENGINE?=pg
DJANGO?='last'
PG_ETOOLS_PARAMS=-U postgres -p 15432 -h 127.0.0.1

.mkbuilddir:
	mkdir -p ${BUILDDIR}

help:
	echo ""


develop:
	@pipenv sync --dev
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type pre-push.
	$(MAKE) .init-db


.init-db:
	psql -h 127.0.0.1 -c 'DROP DATABASE IF EXISTS etools_datamart;' -U postgres
	psql -h 127.0.0.1 -c 'CREATE DATABASE etools_datamart;' -U postgres

test:
	pipenv run py.test -v --create-db

lint:
	pipenv run pre-commit run --all-files
	pipenv run pre-commit run --all-files --hook-stage push
	pipenv run pre-commit run --all-files --hook-stage manual
#	pipenv run flake8 src/ tests/
#	pipenv run isort -rc src/ --check-only
#	pipenv run check-manifest

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml .eggs
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find src/concurrency/locale -name django.mo | xargs rm -f
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


urf:
	pipenv run pytest tests/urf --cov-config tests/urf/.coveragerc
