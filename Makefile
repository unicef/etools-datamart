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


stack:
	PYTHONPATH=./src pipenv run celery worker -A etools_datamart --loglevel=DEBUG --concurrency=4 --purge --pidfile celery.pid &
	PYTHONPATH=./src pipenv run celery beat -A etools_datamart.celery --loglevel=DEBUG --pidfile beat.pid &
#	PYTHONPATH=./src pipenv run gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi --pid gunicorn.pid &
	pipenv run docker run  -d -p 5555:5555 -e CELERY_BROKER_URL=${CELERY_BROKER_URL} --name datamart-flower --rm saxix/flower

demo: stack
	PYTHONPATH=./src pipenv run gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi --pid gunicorn.pid &

demo-stop:
	-kill `cat gunicorn.pid`
	-kill `cat beat.pid`
	-kill `cat celery.pid`
	-docker stop datamart-flower

reset-migrations:
	find src -name '000[1,2,3,4,5,6,7,8,9]*' | xargs rm -f

	psql -h 127.0.0.1 -p 5432 -U postgres -c "DROP DATABASE IF EXISTS test_etools_datamart"
	psql -h 127.0.0.1 -p 5432 -U postgres -c "DROP DATABASE IF EXISTS etools_datamart"
	psql -h 127.0.0.1 -p 5432 -U postgres -c "CREATE DATABASE etools_datamart"

	./manage.py reset-migrations
	./manage.py init-setup --all
