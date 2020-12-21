## Collaborate

### Prerequisites

 - [pipenv](https://github.com/pypa/pipenv)
 - [docker](https://www.docker.com/get-docker)
 - [pipsi](https://github.com/mitsuhiko/pipsi/)



setup local en0 alias

    $ sudo ifconfig en0 alias 192.168.66.66

### Initialize app

   Create a `.env` file in the root folder based on the content for `.env.tpl`

    $ pipenv sync
    $ pipenv shell
    $ ./manage.py init-setup --all
    $ ./manage.py runserver


### How to run tests

Each time Etools data models changes, it's needed to rebuild the datamart models and the sql
needed to run the tests

run `db/update_etools_schema.sh` and follow provided steps
