BUILDDIR?='build'
PG_ETOOLS_PARAMS?=-U postgres -p 15432 -h 127.0.0.1

.mkbuilddir:
	mkdir -p ${BUILDDIR}

help:
	@echo ""
	@echo "Usage:"
	@echo "   make develop                    build dev environment "
	@echo "   make test                       run tests "
	@echo "   make lint                       run lint checks "
	@echo "   make clean                      remove generated files "
	@echo "   make fullclean                  clean + remove cache "
	@echo "   make docs                       generate docs "
	@echo "   make run                        run app "


develop:
	@poetry run
	poetry run pre-commit install
	poetry run pre-commit install --hook-type pre-push.

test:
	poetry run py.test -v --create-db

lint:
	poetry run pre-commit run --all-files
	poetry run pre-commit run --all-files --hook-stage push
	poetry run pre-commit run --all-files --hook-stage manual

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml .eggs
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	rm -f db/clean.sql db/etools.dump db/public.sqldump db/tenant.sql

fullclean:
	rm -fr .cache .pytest_cache
	$(MAKE) clean

sync-etools:
	sh src/etools_datamart/apps/multitenant/postgresql/dump.sh ${PG_ETOOLS_PARAMS}

docs:
	.mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/ ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif

run:
	docker-compose up
