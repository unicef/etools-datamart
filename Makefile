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
	pipenv sync --dev

test:
	pipenv run py.test -v --create-db

lint:
	pipenv run flake8 *; exit 0;
	pipenv run isort . --check-only; exit 0;

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

run:
	docker-compose up
